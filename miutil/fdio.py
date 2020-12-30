import logging
from collections import Iterable
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
            log.warning("cannot create:%s:%s" % (pth, exc))


def is_iter(x):
    return isinstance(x, Iterable) and not isinstance(x, (str, bytes))


def hasext(fname, ext):
    if not is_iter(ext):
        ext = (ext,)
    ext = (("" if i[0] == "." else ".") + i.lower() for i in ext)
    return fspath(fname).lower().endswith(tuple(ext))


@contextmanager
def tmpdir(*args, **kwargs):
    d = mkdtemp(*args, **kwargs)
    yield d
    rmtree(d)
