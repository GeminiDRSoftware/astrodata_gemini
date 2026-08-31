from pathlib import Path

import pytest

from ..testing import find_test_data

from .lut_tags import tags_data

@pytest.mark.goa_remote_data
@pytest.mark.parametrize("instr,filename,tag_set",
                         list([*k]+[v] for k, v in tags_data.items()))
def test_descriptor(instr, filename, tag_set):
    """Check all the tags for all the test files in the LUTs."""

    store_location = _get_store_location()
    ad = find_test_data(filename, store_location)

    assert ad.tags == set(tag_set)


# Needs to be here because we need the name and location of this file.
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
