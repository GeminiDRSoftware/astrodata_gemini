"""Tags and descriptors for CIRPASS data."""

from astrodata import TagSet, astro_data_descriptor, astro_data_tag

from ..gemini import AstroDataGemini


class AstroDataCirpass(AstroDataGemini):
    """AstroData class for CIRPASS data."""

    __keyword_dict = dict(
        ra = "TEL_RA",
        dec = "TEL_DEC",
    )
    @staticmethod
    def _matches_data(source):
        return source[0].header.get("INSTRUME", "") == "CIRPASS"

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(["CIRPASS"])

    @astro_data_tag
    def _tag_image(self):
        return TagSet(["IMAGE"])

    @astro_data_tag
    def _tag_dark(self):
        if "dark" in self.phu.get("OBSTYPE", "").lower():
            return TagSet(["DARK", "CAL"], blocks=["IMAGE"])

    @astro_data_tag
    def _tag_flat(self):
        if "flat" in self.phu.get("OBSTYPE", "").lower():
            return TagSet(["FLAT", "CAL"])

    @astro_data_tag
    def _tag_bias(self):
        if "bias" in self.phu.get("OBSTYPE", "").lower():
            return TagSet(["BIAS", "CAL"], blocks=["IMAGE"])

    @astro_data_descriptor
    def ra(self):
        """
        Return the name of the.

        Returns
        -------
        <str>:
            right ascension

        """
        return self.target_ra()

    @astro_data_descriptor
    def dec(self):
        """
        Return the name of the.

        Returns
        -------
        <str>:
            declination

        """
        return self.target_dec()

    @astro_data_descriptor
    def target_ra(self):
        """Return the Right Ascension of the target, in degrees."""
        return self._ra()

    @astro_data_descriptor
    def target_dec(self):
        """Return the Declination of the target, in degrees."""
        return self._dec()
