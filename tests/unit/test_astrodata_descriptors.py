import pytest
import astrodata
import astrodata_gemini
import os
from pathlib import Path
from astrodata.testing import download_from_archive

import numpy as np


FLOAT_TYPES = (float, np.float32, np.float64)

THIS_DIR = Path(__file__).parent

from .lut_descriptors import descriptors_data
# Keep separate because GHOST has non-raw files
#  KL TODO:  why does that matter here?
from .ghost_lut_descriptors import descriptors_data as ghost_descriptors_data

@pytest.mark.slow
@pytest.mark.goa_remote_data
@pytest.mark.parametrize("instr,filename,descriptor,value",
                         list([*k]+[*vv] for k, v in (list(descriptors_data.items()) +
                                                      list(ghost_descriptors_data.items())
                                                      )
                          for vv in v))
def test_descriptor(instr, filename, descriptor, value):

    # First try to download the file from the archive.
    failed_to_download = False
    try:
        ad = astrodata.open(
            download_from_archive(filename, env_var="ADGEMINI_TESTDATA")
        )
    except OSError:
        skip_message = f"\n{str(filename)} cannot be downloaded from the archive."
        failed_to_download = True

    # If the download fails, see if the file is stored locally in the
    # $ADGEMINI_STORE_TESTDATA directory.  Eg. Reduced test files not in the
    # archive would be stored there on Jenkins.
    if failed_to_download:
        # First check if the file in in ADGEMINI_TESTDATA.  If so, use that.
        # If not, check if the file is in ADGEMINI_STORE_TESTDATA.  If not,
        # skip the test.
        try:
            path_to_test_file = Path(os.environ["ADGEMINI_TESTDATA"]) / filename
            ad = astrodata.open(path_to_test_file)
        except FileNotFoundError:
            skip_message += (
                f"\n{str(filename)} not found in $ADGEMINI_TESTDATA."
                f"  {os.getenv("ADGEMINI_TESTDATA")}."
            )

        # If this is running on Jenkins, the data should be available in
        # the $ADGEMINI_STORE_TESTDATA directory.
        path_to_stored_files = os.getenv("ADGEMINI_STORE_TESTDATA")
        if path_to_stored_files is None:
            pytest.skip(f"{skip_message}  "
                f"Also, environment variable not set: $ADGEMINI_STORE_TESTDATA"
            )

        path_to_stored_files = Path(path_to_stored_files).expanduser()
        path_to_stored_files = (
                path_to_stored_files
                / "unit"
                / "test_astrodata_descriptors"
                / "inputs"
        )

        filepath = path_to_stored_files / filename
        try:
            ad = astrodata.open(filepath)
        except FileNotFoundError:
            pytest.skip(
                f"{skip_message}  "
                f"\n{str(filename)} not found in $ADGEMINI_STORE_TESTDATA"
                f" {path_to_stored_files}."
            )


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
