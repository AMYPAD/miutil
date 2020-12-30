import logging
from os import path
from shutil import rmtree

from miutil import fdio


def test_create_dir(tmp_path, caplog):
    tmpdir = tmp_path / "create_dir"
    assert not tmpdir.exists()
    fdio.create_dir(tmpdir)
    assert tmpdir.exists() and tmpdir.is_dir()
    rmtree(fdio.fspath(tmpdir), True)

    with open(fdio.fspath(tmpdir), "w") as fd:
        fd.write("dummy file")
    with caplog.at_level(logging.INFO):
        assert "cannot create" not in caplog.text
        fdio.create_dir(tmpdir)
        assert "cannot create" in caplog.text

    assert tmpdir.exists()


def test_hasext():
    for fname, ext in [
        (".baz", ".baz"),
        ("foo.bar", ".bar"),
        ("foo.bar", "bar"),
        ("foo.bar.baz", "bar.baz"),
        ("foo/bar.baz", "baz"),
        ("foo.bar.baz", "baz"),
    ]:
        assert fdio.hasext(fname, ext)

    for fname, ext in [
        ("foo.bar", "baz"),
        ("foo", "foo"),
    ]:
        assert not fdio.hasext(fname, ext)


def test_tmpdir():
    with fdio.tmpdir() as tmpdir:
        assert path.exists(tmpdir)
        res = tmpdir
    assert not path.exists(res)
