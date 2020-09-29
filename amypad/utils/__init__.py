from os import makedirs, path


def create_dir(pth):
    """Equivalent of `mkdir -p`"""
    if not path.exists(pth):
        makedirs(pth)
