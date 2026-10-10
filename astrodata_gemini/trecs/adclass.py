"""Tags and descriptors for T-ReCS data."""

from astrodata import (
    TagSet,
    astro_data_descriptor,
    astro_data_tag,
    returns_list,
)

from .. import gmu
from ..gemini import AstroDataGemini


class AstroDataTrecs(AstroDataGemini):
    """AstroData class for T-ReCS data."""

    __keyword_dict = dict(camera = 'OBSMODE',
                          disperser = 'GRATING',
                          exposure_time = 'OBJTIME',
                          focal_plane_mask = 'SLIT',
                          pupil_mask = 'PUPILIMA')

    @staticmethod
    def _matches_data(source):
        return source[0].header.get('INSTRUME', '').upper() == 'TRECS'

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(['TRECS'])

    # override gemini-level "type_mode" because OBSMODE is used for something
    # else in TReCS.
    @astro_data_tag
    def _type_mode(self):
        if 'MIRROR' in self.phu.get('GRATING', '').upper():
            return TagSet(['IMAGE'])
        else:
            return TagSet(['SPECT'])

    @astro_data_descriptor
    @gmu.return_requested_units(input_units="um")
    def central_wavelength(self):
        """
        Return the central wavelength in microns.

        Returns
        -------
        float
            The central wavelength setting
        """
        disperser = self.disperser()
        if disperser is None:
            return None
        if disperser == 'LowRes-10':
            wave_in_microns = 10.5
        elif disperser == 'LowRes-20':
            wave_in_microns = 20.0
        elif disperser.startswith('HighRes-10'):
            wave_in_microns = self.phu.get('HRCENWL')
        else:
            return None
        return wave_in_microns

    @astro_data_descriptor
    def detector_x_offset(self):
        """
        Return the offset along the positive x-direction of the detector.

        The offset is measured from the reference position, in pixels.

        Returns
        -------
        float
            The offset in pixels
        """
        try:
            return self.phu.get('POFFSET') / self.pixel_scale()
        except TypeError:  # either is None
            return None

    @astro_data_descriptor
    def detector_y_offset(self):
        """
        Return the offset along the positive y-direction of the detector.

        The offset is measured from the reference position, in pixels.

        Returns
        -------
        float
            The offset in pixels
        """
        try:
            return -self.phu.get('QOFFSET') / self.pixel_scale()
        except TypeError:  # either is None
            return None

    @astro_data_descriptor
    @gmu.return_requested_units(input_units="um")
    def dispersion(self):
        """
        Return the dispersion in microns per pixel.

        A list (one value per extension) is returned, or a float if used on a
        single-extension slice. It is possible to control the units of
        wavelength using the input arguments.

        Returns
        -------
        list/float
            The dispersion(s)
        """
        disperser = self.disperser()
        if disperser == 'LowRes-10':
            dispersion = 0.022
        elif disperser == 'LowRes-20':
            dispersion = 0.033
        elif disperser.startswith('HighRes-10'):
            dispersion = 0.0019
        else:
            return None
        return dispersion

    @returns_list
    @astro_data_descriptor
    def gain(self):
        """
        Return the gain (electrons/ADU) for each extension.

        Returns
        -------
        list of floats/float
            Gains used for the observation
        """
        bias_level = self.phu.get('BIASLEVL', '')
        if bias_level == '2':
            return 214.0
        elif bias_level == '1':
            return 718.0

    @astro_data_descriptor
    def pixel_scale(self):
        """
        Return the image scale in arcseconds per pixel.

        Returns
        -------
        float
            the pixel scale
        """
        return 0.089

    @astro_data_descriptor
    def slit_width(self):
        """
        Return the width of the slit in arcseconds.

        Returns
        -------
        float
            the slit width in arcseconds
        """
        slit_name = self.slit()
        if 'Open' not in slit_name:
            return float(slit_name.replace('"', ''))
        return None
