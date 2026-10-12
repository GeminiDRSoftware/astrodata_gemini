"""Tags and descriptors for OSCIR data."""

from astrodata import TagSet, astro_data_descriptor, astro_data_tag

from ..gemini import AstroDataGemini


class AstroDataOscir(AstroDataGemini):
    """AstroData class for OSCIR data."""

    @staticmethod
    def _matches_data(source):
        return source[0].header.get('INSTRUME', '').upper() == 'OSCIR'

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(['OSCIR'])

    @astro_data_descriptor
    def airmass(self):
        """Return the airmass, from the AIRMASS1 keyword."""
        return float(self.phu.get('AIRMASS1'))

    @astro_data_descriptor
    def exposure_time(self):
        """Return the exposure time, from the EXPTIME keyword."""
        return float(self.phu.get('EXPTIME'))

    @astro_data_descriptor
    def dec(self):
        """
        Return the Declination of the center of the field, in degrees.

        Returns
        -------
        float
            declination in degrees
        """
        return self._dec()

    @astro_data_descriptor
    def ra(self):
        """
        Return the Right Ascension of the center of the field, in degrees.

        Returns
        -------
        float
            right ascension in degrees
        """
        return self._ra()
