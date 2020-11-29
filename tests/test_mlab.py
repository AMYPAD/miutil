from pytest import importorskip

engine = importorskip("matlab.engine")


def test_matlab():
    from miutil.mlab import beautify, get_engine

    assert not engine.find_matlab()
    eng = get_engine()

    matrix = eng.eval("eye(3)")
    assert matrix.size == (3, 3)

    assert engine.find_matlab()
    eng2 = get_engine()
    assert eng == eng2

    eng = beautify.ensure_mbeautifier()
    assert eng.MBeautify.formatFileNoEditor
