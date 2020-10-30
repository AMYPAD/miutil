from pytest import importorskip


def test_matlab():
    engine = importorskip("matlab.engine")
    from miutil.mlab import get_engine

    assert not engine.find_matlab()
    eng = get_engine()

    matrix = eng.eval("eye(3)")
    assert matrix.size == (3, 3)

    assert engine.find_matlab()
    eng2 = get_engine()
    assert eng == eng2
