"""Tags and descriptors for FLAMINGOS data."""

from astrodata import TagSet, astro_data_descriptor, astro_data_tag

from .. import gmu
from ..gemini import AstroDataGemini


class AstroDataFlamingos(AstroDataGemini):
    """AstroData class for FLAMINGOS data."""

    __keyword_dict = dict(
        detector = 'DETECTOR',
        filter_name = 'FILTER',
        disperser = 'GRISM',
        exposure_time = 'EXP_TIME',
    )

    @staticmethod
    def _matches_data(source):
        return source[0].header.get('INSTRUME', '').upper() == 'FLAMINGOS'

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(['FLAMINGOS'])

    @astro_data_tag
    def _tag_spect(self):
        if self.phu.get('BIAS') == 1.0:
            return TagSet(['IMAGE'])
        else:
            return TagSet(['SPECT'])

    @astro_data_tag
    def _tag_flat(self):
        if 'flat' in self.phu.get('OBJECT', '').lower():
            return TagSet(['FLAT', 'CAL'])

    @astro_data_tag
    def _tag_twilight(self):
        if 'twilight' in self.phu.get('OBJECT', '').lower():
            return TagSet(['TWILIGHT', 'CAL'])    

    @astro_data_tag
    def _tag_dark(self):
        if 'dark' in self.phu.get('OBJECT', '').lower():
            return TagSet(['DARK', 'CAL'])

    @astro_data_descriptor
    @gmu.return_requested_units()
    def central_wavelength(self):
        """
        Return the central wavelength.

        Returns
        -------
        float
            The central wavelength setting
        """
        return 1500.0

    @astro_data_descriptor
    def dec(self):
        """
        Return the Declination of the center of field in degrees.

        Since a fiber is used it coincides with the position of the target. For
        code re-used, use target_dec() if you really want the position of the
        target rather than the center of the field.

        Returns
        -------
        float
            declination in degrees
        """
        return self.target_dec()

    @astro_data_descriptor
    def detector(self):
        """Return the name of the detector."""
        return self.phu.get(self._keyword_for('detector'))

    @astro_data_descriptor
    def disperser(self, stripID=False, pretty=False):
        """
        Return the name of the disperser.

        Parameters
        ----------
        stripID : <bool>
            Does nothing.

        pretty : <bool>
            Also does nothing.

        Returns
        -------
        <str>:
            Name of the disperser.

        """
        dispr = self.phu.get(self._keyword_for('disperser'))
        if 'open' not in dispr and 'dark' not in dispr:
            return dispr
        else:
            return None
        return

    @astro_data_descriptor
    def exposure_time(self):
        """
        Return the exposure time in seconds.

        Returns
        -------
        float
            Exposure time.
        """
        return self.phu.get(self._keyword_for('exposure_time'), None)

    @astro_data_descriptor
    def filter_name(self, stripID=False, pretty=False):
        """Return the filter name; stripID and pretty have no effect."""
        return self.phu.get(self._keyword_for('filter_name'))    

    @astro_data_descriptor
    def ra(self):
        """
        Return the Right Ascension of the center of field in degrees.

        Since a fiber is used it coincides with the position of the target. For
        code re-used, use target_ra() if you really want the position of the
        target rather than the center of the field.

        Returns
        -------
        float
            right ascension in degrees
        """
        return self.target_ra()
