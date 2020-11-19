from pytest import importorskip


def test_get_cc():
    importorskip("pynvml")
    from miutil.cuinfo import get_cc

    cc = get_cc()
    assert len(cc) == 2, cc
    assert all(isinstance(i, int) for i in cc), cc
