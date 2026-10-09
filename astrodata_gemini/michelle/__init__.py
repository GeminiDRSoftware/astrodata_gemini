"""AstroData class for Michelle data."""

__all__ = ["AstroDataMichelle"]

from astrodata import factory

from .adclass import AstroDataMichelle

factory.add_class(AstroDataMichelle)
