from pytest import importorskip

from miutil.fdio import fspath
from miutil.imio import imread

np = importorskip("numpy")


def test_imread(tmp_path):
    x = np.random.randint(10, size=(9, 9))
    fname = tmp_path / "test_imread.npy"
    np.save(fname, x)
    assert (imread(fname) == x).all()

    fname = tmp_path / "test_imread.npz"
    np.savez(fname, x)
    assert (imread(fname) == x).all()

    np.savez(fname, x, x)
    assert (imread(fname)["arr_0"] == x).all()


def test_nii(tmp_path):
    nii = importorskip("miutil.imio.nii")

    x = np.arange(2 * 2 * 3).reshape(2, 2, 3)
    fname = tmp_path / "test_nii.nii"
    nii.array2nii(x, np.eye(4), fname, flip=(1, 1, 1))
    nii.nii_gzip(fname)
    assert (imread(fspath(fname) + ".gz") == x).all()
