import logging
from os import path
from shutil import rmtree

from miutil import fdio


def test_create_dir(tmp_path, caplog):
    tmpdir = tmp_path / "create_dir"
    assert not path.exists(fdio.fspath(tmpdir))
    fdio.create_dir(tmpdir)
    tmpdir = fdio.fspath(tmpdir)
    assert path.exists(tmpdir)
    rmtree(tmpdir, True)

    with open(tmpdir, "w") as fd:
        fd.write("dummy file")
    with caplog.at_level(logging.INFO):
        assert "cannot create" not in caplog.text
        fdio.create_dir(tmpdir)
        assert "cannot create" in caplog.text

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
