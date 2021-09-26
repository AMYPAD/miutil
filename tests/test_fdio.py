import logging
from os import path
from shutil import rmtree

from pytest import importorskip

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
    for fname, ext in [(".baz", ".baz"), ("foo.bar", ".bar"), ("foo.bar", "bar"),
                       ("foo.bar.baz", "bar.baz"), ("foo/bar.baz", "baz"), ("foo.bar.baz", "baz")]:
        assert fdio.hasext(fname, ext)

    for fname, ext in [("foo.bar", "baz"), ("foo", "foo")]:
        assert not fdio.hasext(fname, ext)


def test_tmpdir():
    with fdio.tmpdir() as tmpdir:
        assert path.exists(tmpdir)
        res = tmpdir
    assert not path.exists(res)


def test_extractall(tmp_path):
    web = importorskip("miutil.web")
    tmpdir = tmp_path / "extractall"
    assert not tmpdir.exists()
    url = "https://github.com/AMYPAD/miutil/archive/v0.6.0.zip"
    with web.urlopen_cached(url, tmpdir) as fd:
        fdio.extractall(fd, tmpdir)

    assert (tmpdir / "miutil-0.6.0" / "README.rst").is_file()
    assert ("Medical imaging utilities." in (tmpdir / "miutil-0.6.0" / "README.rst").read_text())


def test_nsort():
    fnames = ["foo1_bar_21.nii.gz", "foo1_bar_1.2.nii.gz", "foo1_bar_1.nii.gz"]
    assert fdio.nsort(fnames) == fnames[::-1]
    fnames = [i[9:] for i in fnames]
    assert fdio.nsort(fnames) == fnames[::-1]
