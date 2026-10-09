"""AstroData class for SkyCam data."""

__all__ = ["AstroDataSkyCam"]

from astrodata import factory

from .adclass import AstroDataSkyCam

factory.add_class(AstroDataSkyCam)
