"""Tags and descriptors for Michelle data."""

from astrodata import (
    TagSet,
    astro_data_descriptor,
    astro_data_tag,
    returns_list,
)

from ..gemini import AstroDataGemini


class AstroDataMichelle(AstroDataGemini):
    """AstroData class for Michelle data."""
    
    __keyword_dict = dict(
        central_wavelength="GRATPOS",
        coadds="NUMEXPOS",
        disperser="GRATNAME",
        dispersion="GRATDISP",
        exposure_time="EXPOSURE",
        filter_name="FILTER",
        focal_plane_mask="SLITNAME",
        read_mode="MODE",
    )

    @staticmethod
    def _matches_data(source):
        return source[0].header.get("INSTRUME", "").upper() == "MICHELLE"

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet({"MICHELLE"}, ())

    @astro_data_tag
    def _tag_mode(self):
        camera = self.phu.get("CAMERA")
        if camera == "imaging":
            return TagSet({"IMAGE"}, ())
        elif camera == "spectroscopy":
            return TagSet({"SPECT", "LS"}, ())

    @astro_data_descriptor
    def exposure_time(self):
        """
        Return the exposure time in seconds.

        Returns
        -------
        float
            Exposure time.
        """
        exposure_time = self.phu.get(self._keyword_for("exposure_time"), -1)
        num_ext = self.phu.get("NUMEXT", 1)
        if exposure_time < 0:
            return None
        return exposure_time * num_ext * self.coadds()

    @astro_data_descriptor
    def filter_name(self, stripID=False, pretty=False):
        """
        Return the name of the filter(s) used.

        Since MICHELLE was not originally a Gemini instrument, its filters
        don't have componentIDs and so pretty and stripID do nothing.

        Parameters
        ----------
        stripID : bool
            Does nothing
        pretty : bool
            Does nothing

        Returns
        -------
        str
            The name of the filter
        """
        filter_name = self.phu.get("FILTER")
        return "blank" if filter_name == "NBlock" else filter_name

    @returns_list
    @astro_data_descriptor
    def pixel_scale(self):
        """
        Return the image scale in arcseconds per pixel.

        One value per extension is returned unless called on a
        single-extension slice. For Michelle, this comes from the PIXELSIZ PHU
        keyword.

        Returns
        -------
        float/list of floats
            the pixel scale
        """
        return self.phu.get("PIXELSIZ")

    @astro_data_descriptor
    def slit(self):
        """
        Return the name of the slit used.

        Returns
        -------
        str
            the slit name
        """
        return self.phu.get("SLITNAME") if "SPECT" in self.tags else None

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
        if slit_name is not None and "pixels" in slit_name:
            return float(slit_name.split("_")[0]) * self.pixel_scale()[0]
        return None
