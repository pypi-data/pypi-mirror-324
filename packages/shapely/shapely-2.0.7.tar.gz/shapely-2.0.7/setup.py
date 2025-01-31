import builtins
import logging
import os
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext

# ensure the current directory is on sys.path so versioneer can be imported
# when pip uses PEP 517/518 build rules.
# https://github.com/python-versioneer/python-versioneer/issues/193
sys.path.insert(0, os.path.dirname(__file__))
import versioneer

# Skip Cython build if not available
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None


log = logging.getLogger(__name__)
ch = logging.StreamHandler()
log.addHandler(ch)

MIN_GEOS_VERSION = "3.5"

if "all" in sys.warnoptions:
    # show GEOS messages in console with: python -W all
    log.setLevel(logging.DEBUG)


def get_geos_config(option):
    """Get configuration option from the `geos-config` development utility

    The PATH environment variable should include the path where geos-config is
    located, or the GEOS_CONFIG environment variable should point to the
    executable.
    """
    cmd = os.environ.get("GEOS_CONFIG", "geos-config")
    try:
        proc = subprocess.run([cmd, option], capture_output=True, text=True)
    except OSError:
        return
    if proc.stderr and not proc.stdout:
        log.warning("geos-config %s returned '%s'", option, proc.stderr.strip())
        return
    result = proc.stdout.strip()
    log.debug("geos-config %s returned '%s'", option, result)
    return result


def get_geos_paths():
    """Obtain the paths for compiling and linking with the GEOS C-API

    First the presence of the GEOS_INCLUDE_PATH and GEOS_INCLUDE_PATH environment
    variables is checked. If they are both present, these are taken.

    If one of the two paths was not present, geos-config is called (it should be on the
    PATH variable). geos-config provides all the paths.

    If geos-config was not found, no additional paths are provided to the extension. It is
    still possible to compile in this case using custom arguments to setup.py.
    """
    include_dir = os.environ.get("GEOS_INCLUDE_PATH")
    library_dir = os.environ.get("GEOS_LIBRARY_PATH")
    if include_dir and library_dir:
        return {
            "include_dirs": ["./src", include_dir],
            "library_dirs": [library_dir],
            "libraries": ["geos_c"],
        }

    geos_version = get_geos_config("--version")
    if not geos_version:
        log.warning(
            "Could not find geos-config executable. Either append the path to geos-config"
            " to PATH or manually provide the include_dirs, library_dirs, libraries and "
            "other link args for compiling against a GEOS version >=%s.",
            MIN_GEOS_VERSION,
        )
        return {}

    def version_tuple(ver):
        return tuple(int(itm) if itm.isnumeric() else itm for itm in ver.split("."))

    if version_tuple(geos_version) < version_tuple(MIN_GEOS_VERSION):
        raise ImportError(
            f"GEOS version should be >={MIN_GEOS_VERSION}, found {geos_version}"
        )

    libraries = []
    library_dirs = []
    include_dirs = ["./src"]
    extra_link_args = []
    for item in get_geos_config("--cflags").split():
        if item.startswith("-I"):
            include_dirs.extend(item[2:].split(":"))

    for item in get_geos_config("--clibs").split():
        if item.startswith("-L"):
            library_dirs.extend(item[2:].split(":"))
        elif item.startswith("-l"):
            libraries.append(item[2:])
        else:
            extra_link_args.append(item)

    return {
        "include_dirs": include_dirs,
        "library_dirs": library_dirs,
        "libraries": libraries,
        "extra_link_args": extra_link_args,
    }


class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)

        # Add numpy include dirs without importing numpy on module level.
        # derived from scikit-hep:
        # https://github.com/scikit-hep/root_numpy/pull/292

        # Prevent numpy from thinking it is still in its setup process:
        try:
            del builtins.__NUMPY_SETUP__
        except AttributeError:
            pass

        import numpy

        self.include_dirs.insert(0, numpy.get_include())


ext_modules = []

if "clean" in sys.argv:
    # delete any previously Cythonized or compiled files in pygeos
    p = Path(".")
    for pattern in [
        "build/lib.*/shapely/*.so",
        "shapely/*.c",
        "shapely/*.so",
        "shapely/*.pyd",
    ]:
        for filename in p.glob(pattern):
            print(f"removing '{filename}'")
            filename.unlink()
elif "sdist" in sys.argv:
    if Path("LICENSE_GEOS").exists() or Path("LICENSE_win32").exists():
        raise FileExistsError(
            "Source distributions should not pack LICENSE_GEOS or LICENSE_win32. Please remove the files."
        )
else:
    ext_options = get_geos_paths()

    ext_modules = [
        Extension(
            "shapely.lib",
            sources=[
                "src/c_api.c",
                "src/coords.c",
                "src/geos.c",
                "src/lib.c",
                "src/pygeom.c",
                "src/strtree.c",
                "src/ufuncs.c",
                "src/vector.c",
            ],
            **ext_options,
        )
    ]

    # Cython is required
    if not cythonize:
        sys.exit("ERROR: Cython is required to build shapely from source.")

    cython_modules = [
        Extension(
            "shapely._geometry_helpers",
            [
                "shapely/_geometry_helpers.pyx",
            ],
            **ext_options,
        ),
        Extension(
            "shapely._geos",
            [
                "shapely/_geos.pyx",
            ],
            **ext_options,
        ),
    ]

    ext_modules += cythonize(
        cython_modules,
        compiler_directives={"language_level": "3"},
        # enable once Cython >= 0.3 is released
        # define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )


cmdclass = versioneer.get_cmdclass()
cmdclass["build_ext"] = build_ext


# see pyproject.toml for static project metadata
setup(
    version=versioneer.get_version(),
    ext_modules=ext_modules,
    cmdclass=cmdclass,
)
