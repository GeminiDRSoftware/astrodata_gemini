"""AstroData class for GHOST data."""

__all__ = ["AstroDataGhost"]

from astrodata import factory

from .adclass import AstroDataGhost

factory.add_class(AstroDataGhost)
