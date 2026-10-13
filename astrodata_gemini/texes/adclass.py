"""Tags and descriptors for TEXES data."""

from astrodata import TagSet, astro_data_descriptor, astro_data_tag

from ..gemini import AstroDataGemini


class AstroDataTexes(AstroDataGemini):
    """AstroData class for TEXES data."""

    __keyword_dict = dict(
        ra="RA",
        dec="DEC",
        target_ra="TARGRA",
        target_dec="TARGDEC",
        exposure_time="OBSTIME",
        observation_type="OBSTYPE",
    )

    @classmethod
    def read(cls, source):
        """Read the source, renaming the extensions as AstroData expects."""
        def texes_parser(hdu):
            xnam, xver = hdu.header.get("EXTNAME"), hdu.header.get("EXTVER")
            if "RAWFRAME" in [xnam] and xver:
                hdu.header.set(
                    "EXTNAME0",
                    xnam,
                    "EXTNAME Orig (AstroData)",
                    before="EXTNAME"
                )
                hdu.header.set("EXTNAME", "SCI", "Renamed by AstroData")
            elif "SCAN-FRAME" in [xnam] and xver:
                hdu.header.set(
                    "EXTNAME0",
                    xnam,
                    "EXTNAME Orig (AstroData)",
                    before="EXTNAME"
                )
                hdu.header.set("EXTNAME", "SCI", "Renamed by AstroData")
            elif xnam and not xver:
                hdu.header.set(
                    "EXTVER", 1, "Versioned by AstroData", after="EXTNAME"
                )

        return super().read(source, extname_parser=texes_parser)

    @staticmethod
    def _matches_data(source):
        return source[0].header.get("INSTRUME", "") == "TEXES"

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(["TEXES"])

    @astro_data_tag
    def _tag_image(self):
        return TagSet(["SPECT"])

    @astro_data_tag
    def _tag_dark(self):
        if "dark" in self.phu.get("OBSTYPE").lower():
            return TagSet(["DARK", "CAL"], blocks=["SPECT"])

    @astro_data_tag
    def _tag_flat(self):
        if "flat" in self.phu.get("OBSTYPE").lower():
            return TagSet(["FLAT", "CAL"])

    @astro_data_tag
    def _tag_bias(self):
        if "bias" in self.phu.get("OBSTYPE").lower():
            return TagSet(["BIAS", "CAL"], blocks=["SPECT"])

    @astro_data_descriptor
    def exposure_time(self):
        """
        Return the exposure time.

        Returns
        -------
        float
            Exposure time.
        """
        return self.phu.get(self._keyword_for("exposure_time"))

    @astro_data_descriptor
    def observation_type(self):
        """Return the observation type, in upper case."""
        return self.phu.get("OBSTYPE").upper()

    @astro_data_descriptor
    def ra(self):
        """Return the Right Ascension of the field center, in degrees."""
        return self._ra()

    @astro_data_descriptor
    def dec(self):
        """Return the Declination of the field center, in degrees."""
        return self._dec()
