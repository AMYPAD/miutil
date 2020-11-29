#!/usr/bin/env python
"""Usage:
  mbeautify <mfile>...

Arguments:
  <mfile>  : Path to `*.m` file
"""
import logging
from functools import lru_cache, wraps
from os import path
from zipfile import ZipFile

from argopt import argopt
from tqdm.contrib import tmap

from ..web import get_file
from . import get_engine

log = logging.getLogger(__name__)
MBEAUTIFIER_REV = "73bc3da7df39a60aab859a2cb86dd82b4d284312"


@lru_cache()
@wraps(get_engine)
def ensure_mbeautifier(*args, **kwargs):
    eng = get_engine(*args, **kwargs)
    fn = get_file(
        "MBeautifier-%s.zip" % MBEAUTIFIER_REV[:7],
        "https://github.com/AMYPAD/MBeautifier/archive/%s.zip" % MBEAUTIFIER_REV,
    )
    outpath = path.join(path.dirname(fn), "MBeautifier-%s" % MBEAUTIFIER_REV)
    if not path.exists(outpath):
        with ZipFile(fn) as fd:
            fd.extractall(path=path.dirname(outpath))
    assert path.exists(outpath), "Error extracting"
    log.debug("adding wrappers (%s) to MATLAB path", outpath)
    eng.addpath(outpath, nargout=0)
    return eng


def main(*args, **kwargs):
    args = argopt(__doc__).parse_args(*args, **kwargs)
    logging.basicConfig(level=logging.INFO)
    eng = ensure_mbeautifier()
    formatter = eng.MBeautify.formatFileNoEditor

    for fn in tmap(path.abspath, args.mfile):
        log.debug("file:%s", fn)
        formatter(fn, fn, nargout=0)


if __name__ == "__main__":  # pragma: no cover
    main()
