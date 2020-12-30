import logging
from contextlib import contextmanager
from os import makedirs
from shutil import rmtree
from tempfile import mkdtemp

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
try:
    from os import fspath
except ImportError:
    fspath = str
try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

log = logging.getLogger(__name__)


def create_dir(pth):
    """Equivalent of `mkdir -p`"""
    pth = Path(pth)
    if not pth.is_dir():
        try:
            makedirs(fspath(pth))
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
