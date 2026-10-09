import importlib.util
from pathlib import Path

import numpy as np
import pytest

import astrodata_gemini

from .lut_tags import tags_data
from ..testing import astrofaker, find_test_data, get_storage_location

test_files = [
    "S20070131S0152.fits", # bHROS
    "S20150624S0172.fits", # F2
    "S20160317S0055.fits", # F2
    "S20230214S0025.fits", # GHOST
    "N20110718S0294.fits", # GMOS
    "N20160407S0076.fits", # GMOS
    "N20160726S0179.fits", # GMOS
    "N20190216S0039.fits", # GMOS
    "S20060130S0079.fits", # GMOS
    "S20091217S0032.fits", # GMOS
    "S20160905S0003.fits", # GMOS
    "S20261001S0185_bias.fits", # GMOS
    "N20120117S0042.fits", # GNIRS
    "N20130814S0231.fits", # GNIRS
    "N20131222S0070_flat.fits", # GNIRS
    "N20160726S0260.fits", # GNIRS
    "N20240116S0138.fits", # GNIRS
    "S20060507S0125.fits", # GNIRS
    "S20070102S0073.fits", # GNIRS
    "S20161014S0043.fits", # GPI
    "N20190116G0054i.fits", # GRACES
    "S20160613S0316.fits", # GSAOI
    "N20260923S0392.fits", # IGRINS-2
    "N20111112S0316.fits", # MICHELLE
    "S20130806S0071.fits", # NICI
    "N20160727S0078.fits", # NIFS
    "N20131215S0178.fits", # NIRI
    "N20131215S0428.fits", # NIRI
    "S20051113S0300.fits", # TRECS
]

descriptor_lut_path_map = {
    "bHROS": Path(__file__).parent / "others_lut_descriptors.py",
    "F2": Path(__file__).parent / "f2_lut_descriptors.py",
    "GHOST": Path(__file__).parent / "ghost_lut_descriptors.py",
    "GMOS-N": Path(__file__).parent / "gmos_lut_descriptors.py",
    "GMOS-S": Path(__file__).parent / "gmos_lut_descriptors.py",
    "GNIRS": Path(__file__).parent / "gnirs_lut_descriptors.py",
    "GPI": Path(__file__).parent / "others_lut_descriptors.py",
    "GRACES": Path(__file__).parent / "others_lut_descriptors.py",
    "GSAOI": Path(__file__).parent / "gsaoi_lut_descriptors.py",
    "IGRINS-2": Path(__file__).parent / "igrins2_lut_descriptors.py",
    "michelle": Path(__file__).parent / "others_lut_descriptors.py",
    "NICI": Path(__file__).parent / "others_lut_descriptors.py",
    "NIFS": Path(__file__).parent / "nifs_lut_descriptors.py",
    "NIRI": Path(__file__).parent / "niri_lut_descriptors.py",
    "TReCS": Path(__file__).parent / "others_lut_descriptors.py",
}


@pytest.fixture(scope="module")
def ad(request):
    """Returns an AstroData object for each of the test files in the list."""
    current_file = Path(__file__).resolve()
    store_location = get_storage_location(current_file)
    return find_test_data(request.param, store_location)

@pytest.mark.github
@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad",
    [pytest.param(fname, id=fname) for fname in test_files],
    indirect=["ad"]
)
def test_tags(ad):
    """Check all the tags for all the test files in the LUTs."""
    inst = ad.instrument()
    expected_tags = tags_data.get((inst, ad.filename), [])
    assert set(ad.tags) == set(expected_tags)


@pytest.mark.github
@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "ad",
    [pytest.param(fname, id=fname) for fname in test_files],
    indirect=["ad"]
)
def test_descriptors(ad):
    """
    Check all the descriptors for all the test files in the LUTs.  The file
    names and expected descriptor values are stored in a separate LUT.
    """
    inst = ad.instrument()
    lut_path = descriptor_lut_path_map.get(inst)
    lut_module_name = lut_path.stem
    descriptors_data = get_lut_data(lut_module_name, lut_path).descriptors_data
    expected_descriptors = descriptors_data.get((inst, ad.filename), {})

    failures = []
    for descriptor, expected_value in expected_descriptors:
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
            assert mvalue == pytest.approx(expected_value, abs=1e-7,
                                           rel=1e-5)
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


# ---

def get_lut_data(module_name, lut_path):
    """Get the LUT data from the lut_tags.py file.

    Arguments
    ---------
    module_name : str
        The name of the module to import.
    lut_path : str
        The path to the lookup table python file.

    Returns
    -------
    The LUT module.
    """
    spec = importlib.util.spec_from_file_location(module_name, lut_path)
    lut = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lut)
    return lut