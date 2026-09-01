from pathlib import Path

import pytest

from ..testing import find_test_data, get_storage_location
from .lut_tags import tags_data


@pytest.mark.goa_remote_data
@pytest.mark.parametrize(
    "instr,filename,tag_set", list([*k] + [v] for k, v in tags_data.items())
)
def test_descriptor(instr, filename, tag_set):
    """Check all the tags for all the test files in the LUTs."""

    current_file = Path(__file__).resolve()
    store_location = get_storage_location(current_file)
    ad = find_test_data(filename, store_location)

    assert ad.tags == set(tag_set)
