"""Tags and descriptors for Hokupa'a+QUIRC data."""

from astrodata import TagSet, astro_data_descriptor, astro_data_tag

from ..gemini import AstroDataGemini


class AstroDataHokupaaQUIRC(AstroDataGemini):
    """AstroData class for Hokupa'a+QUIRC data."""

    __keyword_dict = dict(
        airmass="AMEND", wavelength_band="FILTER", observation_type="IMAGETYP"
    )

    @staticmethod
    def _matches_data(source):
        return source[0].header.get("INSTRUME", "") == "Hokupaa+QUIRC"

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(["HOKUPAAQUIRC"])

    @astro_data_tag
    def _tag_image(self):
        return TagSet(["IMAGE"])

    @astro_data_tag
    def _tag_dark(self):
        if "dark" in self.phu.get("OBJECT", "").lower():
            return TagSet(["DARK"], blocks=["IMAGE", "SPECT"])

    @astro_data_tag
    def _tag_flat(self):
        if "flat" in self.phu.get("OBJECT", "").lower():
            return TagSet(["FLAT", "CAL"])

    @astro_data_descriptor
    def airmass(self):
        """Return the airmass of the observation."""
        return self.phu.get(self._keyword_for("airmass"))

    @astro_data_descriptor
    def detector_name(self, pretty=False):
        """
        Return the name of the detector.

        For HOKUPAA+QUIRC, this is always 'QUIRC'.

        Returns
        -------
        <str>:
            Detector name

        """
        return "QUIRC"

    @astro_data_descriptor
    def filter_name(self, pretty=False):
        """
        Return the wavelength band, to display 'WaveBand' in the archive.

        Parameters
        ----------
        pretty: <bool>
            This keyword parameter is present for API purposes.
            It has no effect for this descriptor.

        Returns
        -------
        <str>:
             wavelength band substituting for filter_name(pretty=True)
        """
        return self.wavelength_band()

    @astro_data_descriptor
    def instrument(self, generic=False):
        """
        Return the name of the instrument making the observation.

        Parameters
        ----------
        generic: <bool>
            Request the generic instrument name, if applicable.

        Returns
        -------
        <str>: 
            instrument name

        """
        return self.phu.get(self._keyword_for("instrument"))


    @astro_data_descriptor
    def observation_type(self):
        """
        Return 'type' the observation.

        Returns
        -------
        <str>: 
            observation type.

        """
        return self.phu.get(self._keyword_for("observation_type"))

    @astro_data_descriptor
    def ra(self):
        """
        Return the name of the.

        Returns
        -------
        <str>:
            right ascension

        """
        return self._ra()

    @astro_data_descriptor
    def dec(self):
        """
        Return the name of the.

        Returns
        -------
        <str>:
            declination

        """
        return self._dec()

    @astro_data_descriptor
    def wavelength_band(self):
        """
        Return the name of the bandpass of the observation.

        Returns
        -------
        <str>:
            Name of the bandpass.

        """
        return self.phu.get(self._keyword_for("wavelength_band"))

    @astro_data_descriptor
    def target_ra(self):
        """Return the Right Ascension of the target, from the WCS."""
        return self.wcs_ra()

    @astro_data_descriptor
    def target_dec(self):
        """Return the Declination of the target, from the WCS."""
        return self.wcs_dec()
