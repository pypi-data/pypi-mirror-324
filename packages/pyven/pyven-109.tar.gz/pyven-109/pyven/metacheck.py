from .checks import Container, skip
from .pipify import pipify, setupcommand, setuptoolsreq
from .projectinfo import ProjectInfo
from .util import bgcontainer
from contextlib import contextmanager
from lagoon.text import diff
from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory

@contextmanager
def egginfodir(projectdir, version, dockerenabled):
    with TemporaryDirectory() as tempdir:
        copy2(projectdir / ProjectInfo.projectaridname, tempdir)
        for glob in 'README.md', 'LICEN[CS]E*', 'COPYING*', 'NOTICE*', 'AUTHORS*':
            for p in projectdir.glob(glob):
                copy2(p, tempdir)
        copyinfo = ProjectInfo.seek(tempdir)
        pipify(copyinfo, version)
        if dockerenabled and {'setuptools', 'wheel'} != set(copyinfo.allbuildrequires):
            with bgcontainer('-v', f"{tempdir}:{Container.workdir}", f"python:{copyinfo.pyversiontags[0]}") as container:
                container = Container(container)
                container.inituser()
                for command in ['apt-get', 'update'], ['apt-get', 'install', '-y', 'sudo']:
                    container.call(command, check = True, root = True)
                container.call(['pip', 'install', *copyinfo.allbuildrequires, setuptoolsreq], check = True, root = True)
                container.call(['python', 'setup.py', 'egg_info'], check = True)
        else:
            setupcommand(copyinfo, False, 'egg_info')
        d, = Path(tempdir).glob('*.egg-info')
        yield tempdir, d

def metacheck(projectdir, version, dockerenabled):
    if not (projectdir / ProjectInfo.projectaridname).exists():
        return skip
    with egginfodir(projectdir, version, dockerenabled) as (tempdir, d):
        p = d / 'requires.txt'
        q = projectdir / p.relative_to(tempdir)
        if p.exists():
            diff[print](p, q)
        else:
            assert not q.exists()
        p = d / 'PKG-INFO'
        diff[print](p, projectdir / p.relative_to(tempdir))
