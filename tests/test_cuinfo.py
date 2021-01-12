from pytest import importorskip, raises

cuinfo = importorskip("miutil.cuinfo")


def test_num_devices():
    devices = cuinfo.num_devices()
    assert isinstance(devices, int)


def test_compute_capability():
    cc = cuinfo.compute_capability()
    if cc:
        assert len(cc) == 2, cc
        assert all(isinstance(i, int) for i in cc), cc


def test_memory():
    mem = cuinfo.memory()
    if mem:
        assert len(mem) == 3, mem
        assert all(isinstance(i, int) for i in mem), mem


def test_cuinfo_cli(capsys):
    cuinfo.main(["--num-devices"])
    out, _ = capsys.readouterr()
    devices = int(out)
    assert devices >= 0

    # individual dev_id
    for dev_id in range(devices):
        cuinfo.main(["--dev-id", str(dev_id)])
    out, _ = capsys.readouterr()
    assert out.count("Device ") == devices

    # all dev_ids
    cuinfo.main()
    out, _ = capsys.readouterr()
    assert out.count("Device ") == devices

    # dev_id one too much
    with raises(IndexError):
        cuinfo.main(["--dev-id", str(devices)])

    cuinfo.main(["--nvcc-flags"])
    out, _ = capsys.readouterr()
    assert not devices or out.startswith("-gencode=")

    cuinfo.main(["--compute"])
    out, _ = capsys.readouterr()
    assert not devices or all(map(int, out.split(" ")))
