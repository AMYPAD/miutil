from os import path

from pytest import importorskip

from miutil import fspath

web = importorskip("miutil.web")


def test_get_file(tmp_path):
    tmpdir = tmp_path / "get_file"
    assert not path.exists(fspath(tmpdir))
    web.get_file(
        "README.rst",
        "https://github.com/AMYPAD/miutil/raw/master/README.rst",
        cache_dir=tmpdir,
    )
    assert path.exists(fspath(tmpdir / "README.rst"))
