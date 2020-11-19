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

__all__ = ["get_device_count", "get_cc", "get_mem", "get_name", "get_nvcc_flags"]


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


def get_handle(dev_id=-1):
    """allows negative indexing"""
    pynvml.nvmlInit()
    dev_id = get_device_count() + dev_id if dev_id < 0 else dev_id
    try:
        return pynvml.nvmlDeviceGetHandleByIndex(dev_id)
    except pynvml.NVMLError:
        raise IndexError("invalid dev_id")


def get_cc(dev_id=-1):
    """returns compute capability (major, minor)"""
    return tuple(nvmlDeviceGetCudaComputeCapability(get_handle(dev_id)))


def get_mem(dev_id=-1):
    """returns memory (total, free, used)"""
    mem = pynvml.nvmlDeviceGetMemoryInfo(get_handle(dev_id))
    return (mem.total, mem.free, mem.used)


def get_name(dev_id=-1):
    """returns device name"""
    return pynvml.nvmlDeviceGetName(get_handle(dev_id)).decode("U8")


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
