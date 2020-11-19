from os import path

from miutil import fdio


def test_create_dir(tmp_path):
    tmpdir = str(tmp_path / "create_dir")
    assert not path.exists(tmpdir)
    fdio.create_dir(tmpdir)
    assert path.exists(tmpdir)


def test_hasext():
    for fname, ext in [
        ("foo.bar", ".bar"),
        ("foo.bar", "bar"),
        ("foo.bar.baz", "baz"),
        ("foo/bar.baz", "baz"),
    ]:
        assert fdio.hasext(fname, ext)

    for fname, ext in [
        ("foo.bar", "baz"),
        ("foo.bar.baz", "bar.baz"),
        ("foo", "foo"),
    ]:
        assert not fdio.hasext(fname, ext)


def test_tmpdir():
    with fdio.tmpdir() as tmpdir:
        assert path.exists(tmpdir)
        res = tmpdir
    assert not path.exists(res)
