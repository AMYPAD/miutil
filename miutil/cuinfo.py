"""CUDA helpers
Usage:
  miutil.cuinfo [options]

Options:
  -c, --dev-count      : print number of devices (ignores `-d`)
  -f, --nvcc-flags     : print out flags for use nvcc compilation
  -d ID, --dev-id ID   : select device ID [default: None:int] for all
"""
from argopt import argopt
import pynvml

__all__ = ["get_cc", "get_nvcc_flags", "get_device_count"]


def nvmlDeviceGetCudaComputeCapability(handle):
    major = pynvml.c_int()
    minor = pynvml.c_int()
    fn = pynvml.get_func_pointer("nvmlDeviceGetCudaComputeCapability")
    ret = fn(handle, pynvml.byref(major), pynvml.byref(minor))
    pynvml.check_return(ret)
    return [major.value, minor.value]


def get_device_count():
    pynvml.nvmlInit()
    return pynvml.nvmlDeviceGetCount()


def get_cc(dev_id=-1):
    """returns get compute capability [major, minor]"""
    pynvml.nvmlInit()
    if dev_id < 0:
        dev_id = get_device_count() + dev_id
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(dev_id)
    except pynvml.NVMLError:
        raise IndexError("invalid dev_id")
    return tuple(nvmlDeviceGetCudaComputeCapability(handle))


def get_nvcc_flags(dev_id=-1):
    return "-gencode=arch=compute_{0:d}{1:d},code=compute_{0:d}{1:d}".format(
        *get_cc(dev_id)
    )


def main(*args, **kwargs):
    args = argopt(__doc__).parse_args(*args, **kwargs)
    noargs = True
    devices = range(get_device_count()) if args.dev_id is None else [args.dev_id]

    if args.dev_count:
        print(get_device_count())
        noargs = False
    if args.nvcc_flags:
        print(" ".join(sorted(set(map(get_nvcc_flags, devices)))[::-1]))
        noargs = False
    if noargs:
        for dev_id in devices:
            print(
                "Device {:2d}:compute capability:{:d}.{:d}".format(
                    dev_id, *get_cc(dev_id)
                )
            )


if __name__ == "__main__":
    main()
