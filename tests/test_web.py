from miutil import web


def test_get_file(tmp_path):
    tmpdir = tmp_path / "get_file"
    assert not tmpdir.exists()
    web.get_file(
        "README.rst",
        "https://github.com/AMYPAD/miutil/raw/master/README.rst",
        cache_dir=tmpdir,
    )
    assert (tmpdir / "README.rst").is_file()


def test_urlopen_cached(tmp_path):
    tmpdir = tmp_path / "urlopen_cached"
    assert not tmpdir.exists()
    url = "https://github.com/AMYPAD/miutil/raw/master/README.rst"
    with web.urlopen_cached(url, tmpdir, mode="r") as fd:
        assert "Medical imaging utilities" in fd.read()

    assert (tmpdir / "README.rst").is_file()
    assert (tmpdir / "README.rst.url").read_text() == url
