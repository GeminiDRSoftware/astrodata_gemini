"""AstroData class for IGRINS-2 data."""

__all__ = ["AstroDataIgrins2"]

from astrodata import factory

from .adclass import AstroDataIgrins2

factory.add_class(AstroDataIgrins2)
