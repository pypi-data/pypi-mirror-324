from contextlib import contextmanager
from lagoon.program import NOEOL
from pathlib import Path
import os, re, sys

def stderr(obj):
    sys.stderr.write(str(obj))
    sys.stderr.write(os.linesep)

class Excludes:

    def __init__(self, globs):
        def disjunction():
            sep = re.escape(os.sep)
            star = f"[^{sep}]*"
            def components():
                for word in glob.split('/'):
                    if '**' == word:
                        yield f"(?:{star}{sep})*"
                    else:
                        yield star.join(re.escape(part) for part in word.split('*'))
                        yield sep
            for glob in globs:
                concat = ''.join(components())
                assert concat.endswith(sep)
                yield concat[:-len(sep)]
        self.pattern = re.compile(f"^{'|'.join(disjunction())}$")

    def __contains__(self, relpath):
        return self.pattern.search(relpath) is not None

class Seek:

    @classmethod
    def seek(cls, dirpath, name):
        dirpath = Path(dirpath)
        while True:
            path = dirpath / name
            if path.exists():
                seek = cls()
                seek.path = path
                seek.parent = dirpath
                return seek
            parent = dirpath / '..'
            if os.path.abspath(parent) == os.path.abspath(dirpath):
                break
            dirpath = parent

@contextmanager
def bgcontainer(*dockerrunargs):
    from lagoon.text import docker
    container = docker.run._d[NOEOL](*dockerrunargs, 'sleep', 'inf')
    try:
        yield container
    finally:
        docker.rm._f[print](container)

def initapt(dockerexec):
    dockerexec('mkdir', '-pv', '/etc/apt/keyrings')
    dockerexec('curl', '-fsSL', 'https://download.docker.com/linux/debian/gpg', '-o', '/etc/apt/keyrings/docker.asc')
    dockerexec('sh', '-c', 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list')
