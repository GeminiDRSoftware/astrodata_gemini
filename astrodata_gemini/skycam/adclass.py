"""Tags and descriptors for SkyCam data."""

from astrodata import TagSet, astro_data_descriptor, astro_data_tag

from ..gemini import AstroDataGemini


class AstroDataSkyCam(AstroDataGemini):
    """AstroData class for SkyCam data."""

    @staticmethod
    def _matches_data(source):
        # remove "s because they added them, but this will also work if the
        # fix it
        match = (
            source[0].header.get('TELESCOP', '').strip('"')
            == 'GS_ALLSKYCAMERA'
        )
        return match

    @astro_data_tag
    def _tag_instrument(self):
        return TagSet(['GS_ALLSKYCAMERA'])

    @astro_data_tag
    def _tag_site(self):
        return TagSet(['SOUTH'])

    @astro_data_descriptor
    def instrument(self):
        """Return the name of the instrument, from the TELESCOP keyword."""
        return self.phu['TELESCOP'].strip('"')

    @astro_data_descriptor
    def object(self):
        """Return the object name, always 'ZENITH'."""
        return 'ZENITH'
