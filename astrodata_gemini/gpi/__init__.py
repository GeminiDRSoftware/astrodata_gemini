"""AstroData class for GPI data."""

__all__ = ["AstroDataGpi"]

from astrodata import factory

from .adclass import AstroDataGpi

factory.add_class(AstroDataGpi)
