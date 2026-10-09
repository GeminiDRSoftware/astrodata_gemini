"""AstroData class for IGRINS data."""

__all__ = ["AstroDataIgrins"]

from astrodata import factory

from .adclass import AstroDataIgrins

factory.add_class(AstroDataIgrins)
