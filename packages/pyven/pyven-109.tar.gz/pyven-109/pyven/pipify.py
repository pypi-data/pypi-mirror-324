'Generate setuptools files for a project.arid project.'
from .projectinfo import ProjectInfo, Req, SimpleInstallDeps
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from aridity.util import solo
from diapyr.util import bfs
from email.parser import Parser
from lagoon.program import Program
from lagoon.text import git
from pathlib import Path
from pkg_resources import resource_filename
from shutil import rmtree
from tempfile import mkdtemp
from venvpool import initlogging, Pool
import logging, os

log = logging.getLogger(__name__)
setuptoolsreq = 'setuptools>=69.3,<75.8'

def pipify(info, version):
    # Allow release of project without origin:
    if info.config.github.participant:
        _, url = info.descriptionandurl()
    elif info.config.pypi.participant:
        url = f"https://pypi.org/project/{info.config.name}/"
    else:
        url = None
    cc = ConfigCtrl()
    cc.execute('''py_modules := $list()
install_requires := $list()
console_scripts := $list()
''')
    cc.w.name = info.config.name
    cc.w.tagline = info.config.tagline
    for t in info.config.resource.types:
        cc.w.resource.types += t
    cc.w.version = version
    cc.w.description = info.config.tagline
    cc.w.url = url
    if info.config.pypi.participant:
        cc.w.author = info.config.author
        cc.w.author_email = info.config.author_email
    else:
        cc.w.author = cc.w.author_email = None
    for m in info.py_modules():
        cc.w.py_modules += m
    for r in info.allrequires:
        cc.w.install_requires += r
    for s in info.console_scripts():
        cc.w.console_scripts += s
    # XXX: Use soak to generate these?
    tasks = [
        ['setup.py', 'setup.py.aridt', 'pystr'],
    ]
    @bfs(info.allbuildrequires)
    def proc(bfsinfo, name):
        cc.w.build_requires += name
    if proc.donekeys != {'setuptools', 'wheel'}:
        tasks.append(['pyproject.toml', 'pyproject.toml.aridt', 'tomlquote'])
    for name, template, quote in tasks:
        cc.printf('" = $(%s)', quote)
        cc.processtemplate(
                resource_filename(__name__, template), # TODO LATER: Make aridity get the resource.
                os.path.abspath(info.projectdir / name))

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('--transient', action = 'store_true')
    parser.add_argument('projectdir', nargs = '?', type = Path) # FIXME: When projectdir is passed in its console_scripts are not populated!
    args = parser.parse_args()
    info = ProjectInfo.seek('.') if args.projectdir is None else ProjectInfo(args.projectdir, args.projectdir / ProjectInfo.projectaridname)
    pipify(info, info.devversion())
    setupcommand(info, args.transient, 'egg_info')

def setupcommand(info, transient, *command):
    with Pool(3).readonlyortransient[transient](SimpleInstallDeps([*info.allbuildrequires, setuptoolsreq])) as venv:
        Program.text(venv.programpath('python'))[print]('setup.py', *command, cwd = info.projectdir)

def _metaversion(info):
    with solo(info.projectdir.glob('*.egg-info/PKG-INFO')).open(encoding = 'utf-8') as f:
        return Parser().parse(f)['Version']

class VolatileReq:

    @property
    def namepart(self):
        return self.info.config.name

    def __init__(self, info):
        self.versionstr = _metaversion(info)
        self.info = info

    def acceptversion(self, versionstr):
        return self.versionstr == versionstr

class InstallDeps:

    @property
    def pypireqs(self):
        return [VolatileReq(i) for i in self.volatileprojects] + self.fetchreqs

    def __init__(self, info, siblings, localrepo):
        self.info = info
        self.siblings = siblings
        self.localrepo = localrepo

    def __enter__(self):
        self.workspace = mkdtemp()
        editableprojects = {}
        volatileprojects = {}
        pypireqs = []
        def adddeps(i, root):
            for r in i.parsedrequires():
                name = r.namepart
                if name in editableprojects or name in volatileprojects:
                    continue
                if self.siblings:
                    siblingpath = r.siblingpath(i.contextworkspace())
                    if siblingpath.exists():
                        editableprojects[name] = j = ProjectInfo.seek(siblingpath)
                        yield j, True
                        continue
                if self.localrepo is not None:
                    repopath = os.path.join(self.localrepo, f"{name}.git")
                    if os.path.exists(repopath):
                        if self.siblings:
                            log.warning("Not a sibling, install from repo: %s", name)
                        clonepath = os.path.join(self.workspace, name)
                        git.clone[print]('--depth', 1, f"file://{repopath}", clonepath)
                        git.fetch.__tags[print](cwd = clonepath)
                        volatileprojects[name] = j = ProjectInfo.seek(clonepath)
                        yield j, False
                        continue
                if root: # Otherwise pip will handle it.
                    pypireqs.append(r.reqstr)
        @bfs([(self.info, True)])
        class Proc:
            def newdepth(self):
                log.debug("Examine deps of: %s", ', '.join(i.config.name for i, _ in self.currentkeys))
            def process(self, t):
                return adddeps(*t)
        for i in volatileprojects.values(): # Assume editables already pipified.
            pipify(i, _metaversion(i))
        self.localreqs = [str(i.projectdir) for i in editableprojects.values()]
        self.volatileprojects = volatileprojects.values()
        self.fetchreqs = list(Req.published(pypireqs))
        return self

    def add(self, *requires):
        self.fetchreqs.extend(Req.parselines(requires))

    def invoke(self, venv):
        venv.install([str(i.projectdir) for i in self.volatileprojects] + [r.reqstr for r in self.fetchreqs])

    def cinvoke(self, container):
        container.install([f"/installdeps/{os.path.relpath(i.projectdir, self.workspace).replace(os.sep, '/')}" for i in self.volatileprojects] + [r.reqstr for r in self.fetchreqs])

    def __exit__(self, *exc_info):
        rmtree(self.workspace)

if '__main__' == __name__:
    main()
