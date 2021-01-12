from pytest import fixture, importorskip, skip


@fixture
def eng():
    get_engine = importorskip("miutil.mlab").get_engine
    try:
        from matlab import engine
    except ImportError:
        engine = None
    else:
        assert not engine.find_matlab()

    try:
        res = get_engine()
    except Exception as exc:
        skip("MATLAB not found:\n%s" % exc)

    if engine is None:
        from matlab import engine
    assert engine.find_matlab()
    return res


def test_engine(eng):
    from miutil.mlab import get_engine

    matrix = eng.eval("eye(3)")
    assert matrix.size == (3, 3)

    eng2 = get_engine()
    assert eng == eng2


def test_beautify(eng):
    beautify = importorskip("miutil.mlab.beautify")

    eng = beautify.ensure_mbeautifier()
    assert eng.MBeautify.formatFileNoEditor
