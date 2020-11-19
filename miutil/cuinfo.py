"""CUDA helpers
Usage:
  miutil.cuinfo [options]

Options:
  -f, --nvcc-flags  : print out flags for use nvcc compilation
"""
import pynvml

__all__ = ["get_cc", "get_nvcc_flags"]


def nvmlDeviceGetCudaComputeCapability(handle):
    major = pynvml.c_int()
    minor = pynvml.c_int()
    fn = pynvml.get_func_pointer("nvmlDeviceGetCudaComputeCapability")
    ret = fn(handle, pynvml.byref(major), pynvml.byref(minor))
    pynvml.check_return(ret)
    return [major.value, minor.value]


def get_cc(dev_id=0):
    """returns get compute capability [major, minor]"""
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(dev_id)
    return tuple(nvmlDeviceGetCudaComputeCapability(handle))


def get_nvcc_flags(dev_id=0):
    return "-gencode=arch=compute_{0:d}{1:d},code=compute_{0:d}{1:d}".format(*get_cc())


if __name__ == "__main__":
    from argopt import argopt

    args = argopt(__doc__).parse_args()
    if args.nvcc_flags:
        print(get_nvcc_flags())
    else:
        print("Compute capability: {:d}.{:d}".format(*get_cc()))
