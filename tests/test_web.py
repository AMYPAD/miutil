from os import path

from pytest import importorskip

web = importorskip("miutil.web")


def test_get_file(tmp_path):
    tmpdir = str(tmp_path / "get_file")
    assert not path.exists(tmpdir)
    web.get_file(
        "README.rst",
        "https://github.com/AMYPAD/miutil/raw/master/README.rst",
        cache_dir=tmpdir,
    )
    assert path.exists(path.join(tmpdir, "README.rst"))
