"""Tests for the instruments that have only a few test files each."""
from pathlib import Path

import numpy as np
import pytest

import astrodata_gemini

from .lut_tags import tags_data
from .others_lut_descriptors import descriptors_data
from ..testing import find_test_data, get_storage_location

# Instruments covered by this module and their AstroData class.
INSTRUMENT_CLASSES = {
    'BHROS': astrodata_gemini.bhros.adclass.AstroDataBhros,
    'GPI': astrodata_gemini.gpi.adclass.AstroDataGpi,
    'GRACES': astrodata_gemini.graces.adclass.AstroDataGraces,
    'MICHELLE': astrodata_gemini.michelle.adclass.AstroDataMichelle,
    'NICI': astrodata_gemini.nici.adclass.AstroDataNici,
    'TRECS': astrodata_gemini.trecs.adclass.AstroDataTrecs,
}

# Mark every test in this module.
pytestmark = pytest.mark.others


@pytest.fixture(scope="module")
def ad(request):
    """Returns an AstroData object for each of the test files in the list."""
    current_file = Path(__file__).resolve()
    store_location = get_storage_location(current_file)
    return find_test_data(request.param, store_location)


@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad, expected_class",
    [pytest.param(fname, INSTRUMENT_CLASSES[inst], id=fname)
     for (inst, fname), tags in tags_data.items() if inst in INSTRUMENT_CLASSES],
    indirect=["ad"]
)
def test_is_right_instance(ad, expected_class):
    """
    Check that the AstroData object is of the correct type for the
    instrument.  Using the files from the tags LUT to avoid having to
    maintain a separate list of test files.
    """
    assert isinstance(ad, expected_class)


@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad, expected_tags",
    [pytest.param(fname, tags, id=fname)
     for (inst, fname), tags in tags_data.items() if inst in INSTRUMENT_CLASSES],
    indirect=["ad"]
)
def test_tags(ad, expected_tags):
    """Check all the tags for all the test files in the LUTs."""
    assert set(ad.tags) == set(expected_tags)


@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad, dvalue_pairs",
    [pytest.param(fname, dvalue_pairs, id=fname)
     for (inst, fname), dvalue_pairs in descriptors_data.items()
     if inst in INSTRUMENT_CLASSES],
    indirect=["ad"]
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
    """Raise an exception if the descriptor does not match the expected value."""
    method = getattr(ad, descriptor)
    if expected_value is None:
        assert method() is None
    else:
        mvalue = method()
        if (isinstance(mvalue, (float, np.floating)) or
            isinstance(expected_value, (float, np.floating))):
            assert mvalue == pytest.approx(expected_value, abs=1e-7, rel=1e-5)
        elif isinstance(expected_value, list):
            assert len(expected_value) == len(mvalue)
            for v, mv in zip(expected_value, mvalue):
                if (isinstance(mv, (float, np.floating)) or
                    isinstance(v, (float, np.floating))):
                    assert mv == pytest.approx(v, abs=1e-7, rel=1e-5)
                else:
                    assert v == mv
        else:
            assert mvalue == expected_value


@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad",
    [pytest.param(fname, id=fname)
     for (inst, fname) in descriptors_data if inst in INSTRUMENT_CLASSES],
    indirect=["ad"]
)
def test_all_descriptors_represented(ad):
    """Check that the LUT has a value for every name in ad.descriptors."""
    fname = ad.filename
    represented = {descriptor
                   for (inst, name), pairs in descriptors_data.items()
                   if inst in INSTRUMENT_CLASSES and name == fname
                   for descriptor, _ in pairs}
    assert represented == set(ad.descriptors)


@pytest.mark.cirpass
def test_cirpass_ra_dec_from_text():
    """CIRPASS: RA and Dec are read from sexagesimal text in the PHU."""
    ad = astrodata_gemini.cirpass.AstroDataCirpass()
    ad.phu["TEL_RA"] = "03:48:30.113"
    ad.phu["TEL_DEC"] = "+24:20:43.00"
    assert ad.ra() == pytest.approx(57.12547083333333)
    assert ad.dec() == pytest.approx(24.345277777777778)
