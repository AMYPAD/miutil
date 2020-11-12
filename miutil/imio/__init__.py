import re

RE_NII_GZ = re.compile(r"^(.+)(\.nii(?:\.gz)?)$", flags=re.I)
RE_NPYZ = re.compile(r"^(.+)(\.np[yz])$", flags=re.I)


def imread(fname):
    """Read any supported filename"""
    if RE_NII_GZ.search(fname):
        from .nii import getnii

        return getnii(fname)
    elif RE_NPYZ.search(fname):
        import numpy as np

        res = np.load(fname)
        if hasattr(res, "keys") and len(res.keys()) == 1:
            res = res[list(res.keys())[0]]
        return res
    raise ValueError("Unknown image type: " + fname)
