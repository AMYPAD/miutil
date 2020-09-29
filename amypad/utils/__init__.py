from os import makedirs, path


def create_dir(pth):
    """Equivalent of `mkdir -p`"""
    if not path.exists(pth):
        makedirs(pth)


def hasext(fname, ext):
    if ext[0] != ".":
        ext = "." + ext
    return path.splitext(fname)[1].lower() == ext.lower()
