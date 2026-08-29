from pathlib import Path

import numpy as np
import pytest

from ..testing import find_test_data

# Keep separate because GHOST has non-raw files
#  KL TODO:  why does that matter here?
from .ghost_lut_descriptors import descriptors_data as ghost_descriptors_data
from .lut_descriptors import descriptors_data

FLOAT_TYPES = (float, np.float32, np.float64)


@pytest.mark.slow
@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "instr,filename,descriptor,value",
    list(
        [*k] + [*vv]
        for k, v in (
            list(descriptors_data.items())
            + list(ghost_descriptors_data.items())
        )
        for vv in v
    ),
)
def test_descriptor(instr, filename, descriptor, value):
    """Check all the descriptors for all the test files in the LUTs."""

    store_location = _get_store_location()
    ad = find_test_data(filename, store_location)

    method = getattr(ad, descriptor)
    if value is None:
        assert method() is None
    else:
        mvalue = method()
        if type(value) in FLOAT_TYPES or type(mvalue) in FLOAT_TYPES:
            assert mvalue == pytest.approx(value, abs=1e-7, rel=1e-5)
        elif isinstance(value, list):
            assert len(value) == len(mvalue)
            for v, mv in zip(value, mvalue):
                if type(v) in FLOAT_TYPES or type(mv) in FLOAT_TYPES:
                    assert mv == pytest.approx(v, abs=1e-7, rel=1e-5)
                else:
                    assert v == mv


def _get_store_location():
    """Get the list of directories components to build the stored data
    path.
    """
    current_file = Path(__file__).resolve()

    module_name = "astrodata_gemini"

    path_parts = list(current_file.parts)
    store_location = path_parts[path_parts.index(module_name) + 2 :]

    store_location[-1] = store_location[-1].removesuffix(".py")

    store_location.append("inputs")

    return store_location
