"""AstroData class for NICI data."""

__all__ = ["AstroDataNici"]

from astrodata import factory

from .adclass import AstroDataNici

factory.add_class(AstroDataNici)
