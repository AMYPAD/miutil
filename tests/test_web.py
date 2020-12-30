from pytest import importorskip

web = importorskip("miutil.web")


def test_get_file(tmp_path):
    tmpdir = tmp_path / "get_file"
    assert not tmpdir.exists()
    web.get_file(
        "README.rst",
        "https://github.com/AMYPAD/miutil/raw/master/README.rst",
        cache_dir=tmpdir,
    )
    assert (tmpdir / "README.rst").is_file()
