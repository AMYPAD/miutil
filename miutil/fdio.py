import logging
from contextlib import contextmanager
from os import makedirs, path
from shutil import rmtree
from tempfile import mkdtemp

try:
    from os import fspath
except ImportError:
    fspath = str

log = logging.getLogger(__name__)


def create_dir(pth):
    """Equivalent of `mkdir -p`"""
    pth = fspath(pth)
    if not path.isdir(pth):
        try:
            makedirs(pth)
        except Exception as exc:
            log.warn("cannot create:%s:%s" % (pth, exc))


def hasext(fname, ext):
    if ext[0] != ".":
        ext = "." + ext
    return path.splitext(fspath(fname))[1].lower() == ext.lower()


@contextmanager
def tmpdir(*args, **kwargs):
    d = mkdtemp(*args, **kwargs)
    yield d
    rmtree(d)
