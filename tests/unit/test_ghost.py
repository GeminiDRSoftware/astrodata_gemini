from datetime import datetime, timedelta
from pathlib import Path

import pytest

import astrodata_gemini

from ..testing import find_test_data, get_storage_location

PRIMARY_TEST_FILE = "S20221209S0007.fits"
BIAS_TEST_FILE = "S20221208S0089.fits"
FLAT_TEST_FILE = "S20221209S0026.fits"
ARC_TEST_FILE = "S20221208S0064.fits"

# These files take forever to download.
test_files = [
    "S20221209S0007.fits",
    "S20221209S0009.fits",
    "S20221209S0010.fits",
    "S20221209S0011.fits",
    "S20221209S0012.fits",
    "S20221209S0049.fits",
    "S20221209S0054.fits",
    "S20221209S0057.fits",
    "S20221209S0061.fits",
]


@pytest.fixture(scope="module")
def ad(request):
    """Returns an AstroData object for each of the test files in the list."""
    current_file = Path(__file__).resolve()
    store_location = get_storage_location(current_file)
    return find_test_data(request.param, store_location)


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", test_files, indirect=True)
def test_is_right_instance(ad):
    assert isinstance(ad, astrodata_gemini.ghost.adclass.AstroDataGhost)


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", test_files, indirect=True)
def test_can_return_ad_length(ad):
    assert len(ad)


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [PRIMARY_TEST_FILE], indirect=True)
def test_instrument(ad):
    assert ad.phu["INSTRUME"] == "GHOST"
    assert ad.instrument() == "GHOST"


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [PRIMARY_TEST_FILE], indirect=True)
def test_various_tags(ad):
    assert "GHOST" in ad.tags
    assert "BUNDLE" in ad.tags


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [PRIMARY_TEST_FILE], indirect=True)
def test_detector_x_bin(ad):
    xbin = ad.detector_x_bin()
    # should be a dict, since we are a bundle
    assert isinstance(xbin, dict)


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [PRIMARY_TEST_FILE], indirect=True)
def test_ut_datetime(ad):
    udt = ad.ut_datetime()
    # Check against expected UT Datetime, this descriptor also exercises
    # the nascent PHU logic
    assert abs(udt - datetime(2022, 12, 8, 20, 52, 22)) < timedelta(seconds=1)


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [PRIMARY_TEST_FILE], indirect=True)
def test_data_label(ad):
    dl = ad.data_label()
    # Check against expected UT Datetime, this descriptor also exercises
    # the nascent PHU logic
    assert dl == "GS-ENG-GHOST-COM-3-123-001"


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [BIAS_TEST_FILE], indirect=True)
def test_tab_bias(ad):
    assert "BIAS" in ad.tags


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [FLAT_TEST_FILE], indirect=True)
def test_tab_flat(ad):
    assert "FLAT" in ad.tags


@pytest.mark.ghost
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", [ARC_TEST_FILE], indirect=True)
def test_tab_arc(ad):
    assert "ARC" in ad.tags
