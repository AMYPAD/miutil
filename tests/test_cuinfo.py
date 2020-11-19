from pytest import importorskip

importorskip("pynvml")


def test_get_cc():
    from miutil.cuinfo import get_cc

    cc = get_cc()
    assert len(cc) == 2, cc
    assert all(isinstance(i, int) for i in cc), cc


def test_cuinfo_cli(capsys):
    from miutil.cuinfo import main

    main()
    out, err = capsys.readouterr()
    assert out.startswith("Compute capability:")

    main(["--nvcc-flags"])
    out, err = capsys.readouterr()
    assert out.startswith("-gencode=")
