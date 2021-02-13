import logging
import os
import re
import sys
from ast import literal_eval
from os import getenv, path
from platform import system
from subprocess import STDOUT, CalledProcessError, check_output
from textwrap import dedent

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError


from ..fdio import Path, extractall, fspath, tmpdir

__all__ = ["get_engine"]
IS_WIN = any(sys.platform.startswith(i) for i in ["win32", "cygwin"])
MATLAB_RUN = "matlab -nodesktop -nosplash -nojvm".split()
if IS_WIN:
    MATLAB_RUN += ["-wait", "-log"]
log = logging.getLogger(__name__)
_MCR_URL = (
    "https://ssd.mathworks.com/supportfiles/downloads/R2020b/Release/4"
    "/deployment_files/installer/complete/"
)
MCR_ARCH = {"Windows": "win64", "Linux": "glnxa64", "Darwin": "maci64"}[system()]
MCR_URL = {
    "Windows": _MCR_URL + "win64/MATLAB_Runtime_R2020b_Update_4_win64.zip",
    "Linux": _MCR_URL + "glnxa64/MATLAB_Runtime_R2020b_Update_4_glnxa64.zip",
    "Darwin": _MCR_URL + "maci64/MATLAB_Runtime_R2020b_Update_4_maci64.dmg.zip",
}[system()]


class VersionError(ValueError):
    pass


def check_output_u8(*args, **kwargs):
    return check_output(*args, **kwargs).decode("utf-8").strip()


def env_prefix(key, dir):
    os.environ[key] = "%s%s%s" % (os.environ[key], os.pathsep, fspath(dir))


@lru_cache()
def get_engine(name=None):
    try:
        from matlab import engine
    except ImportError:
        try:
            log.warning(
                dedent(
                    """\
                Python could not find the MATLAB engine.
                Attempting to install automatically."""
                )
            )
            log.debug(_install_engine())
            log.info("installed MATLAB engine for Python")
            from matlab import engine
        except CalledProcessError:
            raise ImportError(
                dedent(
                    """\
                Please install MATLAB and its Python module.
                See https://www.mathworks.com/help/matlab/matlab_external/\
install-the-matlab-engine-for-python.html
                or
                https://www.mathworks.com/help/matlab/matlab_external/\
install-matlab-engine-api-for-python-in-nondefault-locations.html
                It's likely you need to do:

                cd "{matlabroot}\\extern\\engines\\python"
                {exe} setup.py build --build-base="BUILDDIR" install

                - Fill in any temporary directory name for BUILDDIR
                  (e.g. /tmp/builddir).
                - If installation fails due to write permissions, try appending `--user`
                  to the above command.

                Alternatively, use `get_runtime()` instead of `get_engine()`.
                """
                ).format(
                    matlabroot=matlabroot(default="matlabroot"), exe=sys.executable
                )
            )
    started = engine.find_matlab()
    notify = False
    if not started or (name and name not in started):
        notify = True
        log.debug("Starting MATLAB")
    eng = engine.connect_matlab(name=name or getenv("SPM12_MATLAB_ENGINE", None))
    if notify:
        log.debug("MATLAB started")
    return eng


def _matlab_run(command, jvm=False, auto_exit=True):
    if auto_exit and not command.endswith("exit"):
        command = command + ", exit"
    return check_output_u8(
        MATLAB_RUN + ([] if jvm else ["-nojvm"]) + ["-r", command], stderr=STDOUT
    )


def matlabroot(default=None):
    if IS_WIN:
        try:
            res = _matlab_run("display(matlabroot);")
        except (CalledProcessError, FileNotFoundError):
            if default:
                return default
            raise
        return re.search(r"^([A-Z]:\\.*)\s*$", res, flags=re.M).group(1)

    try:
        res = check_output_u8(["matlab", "-n"])
    except (CalledProcessError, FileNotFoundError):
        if default:
            return default
        raise
    return re.search(r"MATLAB\s+=\s+(\S+)\s*$", res, flags=re.M).group(1)


def _install_engine():
    src = path.join(matlabroot(), "extern", "engines", "python")
    with open(path.join(src, "setup.py")) as fd:  # check version support
        supported = literal_eval(
            re.search(r"supported_version.*?=\s*(.*?)$", fd.read(), flags=re.M).group(1)
        )
        if ".".join(map(str, sys.version_info[:2])) not in map(str, supported):
            raise VersionError(
                dedent(
                    """\
                Python version is {info[0]}.{info[1]},
                but the installed MATLAB only supports Python versions: [{supported}]
                """.format(
                        info=sys.version_info[:2], supported=", ".join(supported)
                    )
                )
            )
    with tmpdir() as td:
        cmd = [sys.executable, "setup.py", "build", "--build-base", td, "install"]
        try:
            return check_output_u8(cmd, cwd=src)
        except CalledProcessError:
            log.warning("Normal install failed. Attempting `--user` install.")
            return check_output_u8(cmd + ["--user"], cwd=src)


@lru_cache()
def get_runtime(cache="~/.mcr"):
    cache = Path(cache).expanduser()
    mcr_root = cache
    try:
        mcr_root = max(i for i in mcr_root.glob("v*") if i.is_dir())
    except ValueError:
        from miutil.web import urlopen_cached

        log.info("Downloading to %s", cache)
        with tmpdir() as td:
            with urlopen_cached(MCR_URL, cache) as fd:
                extractall(fd, td)
            inst_opts = [
                "-mode",
                "silent",
                "-agreeToLicense",
                "yes",
                "-destinationFolder",
                fspath(mcr_root),
            ]
            check_output_u8(
                [fspath(Path(td) / ("setup" if system() == "Windows" else "install"))]
                + inst_opts
            )
    # bin
    if not (mcr_root / "bin" / MCR_ARCH).is_dir():
        log.warning("Cannot find MCR bin")
    env_prefix("PATH", mcr_root / "bin" / MCR_ARCH)

    # libs
    env_var = {
        "Linux": "LD_LIBRARY_PATH",
        "Windows": "PATH",
        "Darwin": "DYLD_LIBRARY_PATH",
    }[system()]
    if not (mcr_root / "runtime" / MCR_ARCH).is_dir():
        log.warning("Cannot find MCR libs")
    env_prefix(env_var, mcr_root / "runtime" / MCR_ARCH)

    # python module
    pydist = mcr_root / "extern" / "engines" / "python" / "dist"
    if not pydist.is_dir():
        log.warning("Cannot find MCR Python dist")
    if fspath(pydist) not in sys.path:
        sys.path.insert(1, fspath(pydist))

    log.info("Installed")

    return mcr_root
