import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.9`
    from importlib.metadata import (  # pragma: no cover
        PackageNotFoundError,
        version,
    )
else:
    from importlib_metadata import (  # pragma: no cover
        PackageNotFoundError,
        version,
    )

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "pyPrediktorMapClient"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
