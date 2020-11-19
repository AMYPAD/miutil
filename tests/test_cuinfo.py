from pytest import importorskip, raises

importorskip("pynvml")
from miutil.cuinfo import get_cc, get_device_count  # NOQA: E402


def test_get_cc():
    cc = get_cc()
    assert len(cc) == 2, cc
    assert all(isinstance(i, int) for i in cc), cc


def test_get_device_count():
    devices = get_device_count()
    assert isinstance(devices, int)


def test_cuinfo_cli(capsys):
    from miutil.cuinfo import main

    main(["--dev-count"])
    out, _ = capsys.readouterr()
    devices = int(out)
    assert devices >= 0

    # individual dev_id
    for dev_id in range(devices):
        main(["--dev-id", str(dev_id)])
        out, _ = capsys.readouterr()
        assert len(out.split("Device ")) == devices + 1

    # all dev_ids
    main()
    out, _ = capsys.readouterr()
    assert len(out.split("Device ")) == devices + 1

    # dev_id one too much
    with raises(IndexError):
        main(["--dev-id", str(devices)])

    main(["--nvcc-flags"])
    out, _ = capsys.readouterr()
    assert not devices or out.startswith("-gencode=")
