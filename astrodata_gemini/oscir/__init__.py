"""AstroData class for OSCIR data."""

__all__ = ["AstroDataOscir"]

from astrodata import factory

from .adclass import AstroDataOscir

factory.add_class(AstroDataOscir)
