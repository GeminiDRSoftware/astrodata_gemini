"""AstroData class for NIFS data."""

__all__ = ["AstroDataNifs"]

from astrodata import factory

from .adclass import AstroDataNifs

factory.add_class(AstroDataNifs)
