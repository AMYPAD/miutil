from pytest import importorskip

from miutil.imio import imread


def test_imread(tmp_path):
    np = importorskip("numpy")

    x = np.random.randint(10, size=(9, 9))
    fname = tmp_path / "test_imread.npy"
    np.save(fname, x)
    assert (imread(str(fname)) == x).all()

    fname = tmp_path / "test_imread.npz"
    np.savez(fname, x)
    assert (imread(str(fname)) == x).all()

    np.savez(fname, x, x)
    assert (imread(str(fname))["arr_0"] == x).all()
