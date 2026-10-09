"""AstroData class for FLAMINGOS data."""

__all__ = ["AstroDataFlamingos"]

from astrodata import factory

from .adclass import AstroDataFlamingos

factory.add_class(AstroDataFlamingos)
