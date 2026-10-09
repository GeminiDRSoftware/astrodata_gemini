"""AstroData class for HRWFS data."""

__all__ = ["AstroDataHrwfs"]

from astrodata import factory

from .adclass import AstroDataHrwfs

factory.add_class(AstroDataHrwfs)
