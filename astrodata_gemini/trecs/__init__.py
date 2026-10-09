"""AstroData class for T-ReCS data."""

__all__ = ["AstroDataTrecs"]

from astrodata import factory

from .adclass import AstroDataTrecs

factory.add_class(AstroDataTrecs)
