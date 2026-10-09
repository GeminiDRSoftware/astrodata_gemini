"""AstroData class for Hokupa'a+QUIRC data."""

__all__ = ["AstroDataHokupaaQUIRC"]

from astrodata import factory

from .adclass import AstroDataHokupaaQUIRC

factory.add_class(AstroDataHokupaaQUIRC)
