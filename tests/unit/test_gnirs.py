from pathlib import Path

import numpy as np
import pytest

import astrodata_gemini  # noqa: F401  (plugin: registers the AstroData classes)

from ..testing import find_test_data, get_storage_location
from .gnirs_lut_descriptors import descriptors_data
from .lut_tags import tags_data


@pytest.fixture(scope="module")
def ad(request):
    """Returns an AstroData object for each of the test files in the list."""
    current_file = Path(__file__).resolve()
    store_location = get_storage_location(current_file)
    return find_test_data(request.param, store_location)


@pytest.mark.gnirs
@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad",
    [
        pytest.param(fname, id=fname)
        for (inst, fname), tags in tags_data.items()
        if inst == "GNIRS"
    ],
    indirect=["ad"],
)
def test_is_right_instance(ad):
    """
    Check that the AstroData object is of the correct type for GNIRS data.
    Using the files from the tags LUT to avoid having to maintain a separate
    list of test files.
    """
    assert isinstance(ad, astrodata_gemini.gnirs.adclass.AstroDataGnirs)


@pytest.mark.gnirs
@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad, expected_tags",
    [
        pytest.param(fname, tags, id=fname)
        for (inst, fname), tags in tags_data.items()
        if inst == "GNIRS"
    ],
    indirect=["ad"],
)
def test_gnirs_tags(ad, expected_tags):
    """Check all the tags for all the test files in the LUTs."""
    assert set(ad.tags) == set(expected_tags)


@pytest.mark.gnirs
@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad, dvalue_pairs",
    [
        pytest.param(fname, dvalue_pairs, id=fname)
        for (inst, fname), dvalue_pairs in descriptors_data.items()
        if inst == "GNIRS"
    ],
    indirect=["ad"],
)
def test_descriptors(ad, dvalue_pairs):
    """
    Check all the descriptors for all the test files in the LUTs.  The file
    is opened once and all its descriptors are checked in a loop; the
    mismatches are collected and reported together.
    """
    failures = []
    for descriptor, expected_value in dvalue_pairs:
        try:
            _check_descriptor(ad, descriptor, expected_value)
        except Exception as err:
            failures.append(f"{descriptor}: {type(err).__name__}: {err}")
    assert not failures, (
        f"{len(failures)} of {len(dvalue_pairs)} descriptors failed for "
        f"{ad.filename}:\n" + "\n".join(failures)
    )


def _check_descriptor(ad, descriptor, expected_value):
    """
    Raise an exception if the descriptor does not match the expected value.
    """
    method = getattr(ad, descriptor)
    if expected_value is None:
        assert method() is None
    else:
        mvalue = method()
        if isinstance(mvalue, (float, np.floating)) or isinstance(
            expected_value, (float, np.floating)
        ):
            assert mvalue == pytest.approx(expected_value, abs=1e-7, rel=1e-5)
        elif isinstance(expected_value, list):
            assert len(expected_value) == len(mvalue)
            for v, mv in zip(expected_value, mvalue):
                if isinstance(mv, (float, np.floating)) or isinstance(
                    v, (float, np.floating)
                ):
                    assert mv == pytest.approx(v, abs=1e-7, rel=1e-5)
                else:
                    assert v == mv
        else:
            assert mvalue == expected_value


@pytest.mark.gnirs
@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad",
    [
        pytest.param(fname, id=fname)
        for (inst, fname) in descriptors_data
        if inst == "GNIRS"
    ],
    indirect=["ad"],
)
def test_all_descriptors_represented(ad):
    """Check that the LUT has a value for every name in ad.descriptors."""
    fname = ad.filename
    represented = {
        descriptor
        for (inst, name), pairs in descriptors_data.items()
        if inst == "GNIRS" and name == fname
        for descriptor, _ in pairs
    }
    assert represented == set(ad.descriptors)


# The files on which the WCS fallback is tested: one of each kind of
# spectroscopy and imaging, including IFU (north and south).
WCS_FALLBACK_FILES = [
    "N20120117S0019.fits",  # image
    "N20241216S0168.fits",  # longslit
    "N20190206S0279.fits",  # cross-dispersed
    "N20240330S0209.fits",  # IFU (LR-IFU)
    "S20070102S0073.fits",  # IFU, south
]


@pytest.mark.gnirs
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("ad", WCS_FALLBACK_FILES, indirect=True)
def test_ra_and_dec_wcs_fallback(ad, monkeypatch):
    """
    Tests that the get the RA/DEC coordinates using descriptors when the WCS
    coordinate mapping fails

    Parameters
    ----------
    ad : fixture
        Custom fixture that downloads and opens the input file.
    """

    def _fake_wcs_call():
        return None

    monkeypatch.setattr(ad, "wcs_ra", _fake_wcs_call)
    monkeypatch.setattr(ad, "wcs_dec", _fake_wcs_call)
    assert ad.ra() == ad.phu.get("RA", None)
    assert ad.dec() == ad.phu.get("DEC", None)
