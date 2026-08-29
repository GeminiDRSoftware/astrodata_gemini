import pytest
import astrodata
from astrodata.testing import download_from_archive
import astrodata_gemini
import os
from pathlib import Path

from .lut_tags import tags_data

@pytest.mark.goa_remote_data
@pytest.mark.parametrize("instr,filename,tag_set",
                         list([*k]+[v] for k, v in tags_data.items()))
def test_descriptor(instr, filename, tag_set):
    path_to_test_data = os.getenv("DRAGONS_TEST")
    if path_to_test_data is None:
        pytest.skip('Environment variable not set: $DRAGONS_TEST')

    path_to_test_data = os.path.expanduser(path_to_test_data).strip()
    path_to_files = ['gemini_instruments', 'test_astrodata_tags',
                     'inputs']
    path_to_test_data = os.path.join(path_to_test_data, *path_to_files)

    if '_' in filename:
        filepath = os.path.join(path_to_test_data, filename)
        try:
            ad = astrodata.open(filepath)
        except FileNotFoundError:
            pytest.skip(f"{filename} not found")
    else:
        ad = astrodata.open(download_from_archive(filename))

    assert ad.tags == set(tag_set)
