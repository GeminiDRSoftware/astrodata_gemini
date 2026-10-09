"""Parent AstroData class for the Gemini instruments."""

__all__ = [
    "AstroDataGemini",
    "addInstrumentFilterWavelengths",
    "use_keyword_if_prepared",
    "get_specphot_name",
]

from astrodata import factory

from .adclass import (
    AstroDataGemini,
    get_specphot_name,
    use_keyword_if_prepared,
)
from .lookup import filter_wavelengths


def addInstrumentFilterWavelengths(instrument, wl):
    """Add filter wavelengths for a given instrument."""
    update_dict = {
        (instrument, fltname): value for (fltname, value) in wl.items()
    }
    filter_wavelengths.update(update_dict)


factory.add_class(AstroDataGemini)
