"""Tags and descriptors for GRACES data."""

from astrodata import TagSet, astro_data_descriptor, astro_data_tag

from .. import gmu
from ..gemini import AstroDataGemini


class AstroDataGraces(AstroDataGemini):
    """AstroData class for GRACES data."""

    __keyword_dict = dict(detector = 'DETECTOR')

    @staticmethod
    def _matches_data(source):
        return source[0].header.get('INSTRUME', '').upper() == 'GRACES'

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(['GRACES'])

    @astro_data_tag
    def _tag_spect(self):
        return TagSet(['SPECT'])

    @astro_data_tag
    def _tag_arc(self):
        if self.phu.get('OBSTYPE') == 'ARC':
            return TagSet(['ARC', 'CAL'])

    @astro_data_tag
    def _tag_flat(self):
        if self.phu.get('OBSTYPE') == 'FLAT':
            return TagSet(['FLAT', 'CAL'])

    @astro_data_tag
    def _tag_bias(self):
        if self.phu.get('OBSTYPE') == 'BIAS':
            return TagSet(['BIAS', 'CAL'])

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
        return 700

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

        For GRACES, this is always "GRACES".

        Parameters
        ----------
        stripID : bool
            Does nothing.
        pretty : bool
            Also does nothing.

        Returns
        -------
        str
            The name of the disperser, "GRACES".

        """
        return 'GRACES'

    @astro_data_descriptor
    def position_angle(self):
        """GRACES does not have a position angle, so this returns None."""
        return None

    @astro_data_descriptor
    def slit_width(self):
        """Return None. There are no slits in GRACES."""
        return None

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
