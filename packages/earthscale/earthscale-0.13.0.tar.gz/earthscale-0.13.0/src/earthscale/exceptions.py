from rasterio import RasterioIOError


class EarthscaleError(Exception):
    """Base class for exceptions in this module."""

    pass


class RasterFileNotFoundError(EarthscaleError):
    """Raised when a file is not found"""

    pass


class RasterAccessDeniedError(EarthscaleError):
    """Raised when the user does not have access to the dataset,
    or if the dataset is not found"""

    pass


class UnsupportedRasterFormatError(EarthscaleError):
    """Raised when the user tries to open a raster file that is not supported"""

    pass


class NoDataInSelectionError(EarthscaleError):
    """
    Raised by .to_xarray if no data was found for the requested bbox/dimensions
    """

    pass


class NoSTACItemsError(NoDataInSelectionError):
    """Raised when no STAC items are found (for a given spatial and temporal extent)"""

    pass


class MemoryLimitExceededError(EarthscaleError):
    """Raised when the memory limit is exceeded"""

    def __init__(
        self,
        required_megabytes: float,
        limit_megabytes: float,
        message: str | None = None,
    ) -> None:
        self.required_megabytes = required_megabytes
        self.limit_megabytes = limit_megabytes
        if message is None:
            message = (
                f"Operation would require {required_megabytes:.2f} MB but limit "
                f"is {limit_megabytes:.2f} MB"
            )
        super().__init__(message)


def convert_rasterio_to_earthscale(
    e: RasterioIOError,
) -> RasterioIOError | EarthscaleError:
    """Handle rasterio IO errors."""
    if "No such file or directory" in e.args[0]:
        return RasterFileNotFoundError(e.args[0])
    if "Access Denied" in e.args[0]:
        return RasterAccessDeniedError(
            f"{e.args[0]} This could be due to insufficient permissions, "
            "the file not existing, or the file not being readable by rasterio. "
            "Please check that the file exists and you have the necessary "
            "access rights."
        )
    return e


class NoFilesForGlobError(EarthscaleError):
    """Raised when no files are found for a given glob pattern"""

    pass


class NoGeoboxError(EarthscaleError):
    """Raised when a dataset does not have a geobox set"""

    pass


class CannotConvertEarthEngineToXarrayError(EarthscaleError):
    """Raised when a user tries to call `.to_xarray()` for an earth engine dataset"""

    pass
