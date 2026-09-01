from pathlib import Path

import pytest

import astrofaker
import astrodata_gemini

from ..testing import find_test_data, get_storage_location

STANDARD_TEST_FILE = "S20190215S0188.fits"

GMOS_DESCRIPTORS_TYPES = [
    ('detector_x_offset', float),
    ('detector_y_offset', float),
    ('nod_count', tuple),
    ('nod_offsets', tuple),
    ('pixel_scale', float),
    ('shuffle_pixels', int),
]

test_files = [
    "N20110826S0336.fits",
    "N20150624S0106.fits",
    "N20160524S0119.fits",
    "N20170529S0168.fits",
]


@pytest.fixture(scope="module")
def ad(request):
    """Returns an AstroData object for each of the test files in the list."""
    current_file = Path(__file__).resolve()
    store_location = get_storage_location(current_file)
    return find_test_data(request.param, store_location)


@pytest.mark.gmos
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", test_files, indirect=True)
def test_is_right_instance(ad):
    assert isinstance(ad, astrodata_gemini.gmos.adclass.AstroDataGmos)


@pytest.mark.gmos
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", test_files, indirect=True)
def test_can_return_instrument(ad):
    assert ad.phu['INSTRUME'] in ['GMOS-N', 'GMOS-S']
    assert ad.instrument() == ad.phu['INSTRUME']


@pytest.mark.gmos
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", test_files, indirect=True)
def test_can_return_ad_length(ad):
    assert len(ad)


@pytest.mark.gmos
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", test_files, indirect=True)
@pytest.mark.parametrize("descriptor,expected_type", GMOS_DESCRIPTORS_TYPES)
def test_descriptor_matches_type(ad, descriptor, expected_type):
    print(ad.filename, descriptor, expected_type)
    value = getattr(ad, descriptor)()
    assert isinstance(value, expected_type) or value is None, \
        "Assertion failed for file: {}".format(ad.filename)


@pytest.mark.gmos
@pytest.mark.astrofaker
def test_tag_as_standard_fake():
    # LTT4363 (a high proper motion specphot) on Jan 1, 2021
    ad = astrofaker.create('GMOS-S', ['SPECT'],
                           extra_keywords={'RA': 176.46534847,
                                           'DEC': -64.84352513,
                                           'DATE-OBS': '2021-01-01T12:00:00.000',
                                           'OBSTYPE': 'OBJECT'}
                           )
    assert 'STANDARD' in ad.tags


@pytest.mark.gmos
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [STANDARD_TEST_FILE], indirect=True)
def test_tag_as_standard_real(ad):
    assert 'STANDARD' in ad.tags


@pytest.mark.gmos
@pytest.mark.astrofaker
def test_ra_dec_from_text():
    ad = astrofaker.create('GMOS-S', ['SPECT'],
                           extra_keywords={'RA': '03:48:30.113',
                                           'DEC': '+24:20:43.00',
                                           'DATE-OBS': '2021-01-01T12:00:00.000'}
                           )
    assert ad.ra() == pytest.approx(57.12547083333333)
    assert ad.dec() == pytest.approx(24.345277777777778)

    # test bad RA/DEC values, just doing this for GMOS but it's testing the base
    ad = astrofaker.create('GMOS-S', ['SPECT'],
                           extra_keywords={'RA': 'Fail',
                                           'DEC': 'Fail',
                                           'DATE-OBS': '2021-01-01T12:00:00.000'}
                           )
    assert ad.ra() is None
    assert ad.dec() is None

