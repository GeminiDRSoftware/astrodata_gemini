from pathlib import Path
import os
import pytest
import astrodata
from astrodata.testing import download_from_archive

def find_test_data(filename, store_location):
    """
    Find the test data file in the local store.

    Parameters
    ----------
    filename : str
        The name of the test data file to find.
    store_location : str
        The path to the local store of test data files.

    Returns
    -------
    AstroData
        An opened AstroData object for the test data file.

    Raises
    ------
    FileNotFoundError
        If the test data file is not found in the local store.
    """

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
        adgemini_testdata_path = Path(os.getenv("ADGEMINI_TESTDATA")).expanduser()
        try:
            path_to_test_file = Path(os.getenv("ADGEMINI_TESTDATA")) / filename
            ad = astrodata.open(path_to_test_file)
        except FileNotFoundError:
            skip_message += (
                f"\n{str(filename)} not found in $ADGEMINI_TESTDATA."
                f"  {adgemini_testdata_path}."
            )

        # If this is running on Jenkins, the data should be available in
        # the $ADGEMINI_STORE_TESTDATA directory.
        path_to_stored_files = os.getenv("ADGEMINI_STORE_TESTDATA")
        if path_to_stored_files is None:
            pytest.skip(f"{skip_message}  "
                f"Also, environment variable not set: $ADGEMINI_STORE_TESTDATA"
            )

        path_to_stored_files = Path(path_to_stored_files).expanduser()
        path_to_stored_files = path_to_stored_files.joinpath(*store_location)

        filepath = path_to_stored_files / filename
        try:
            ad = astrodata.open(filepath)
        except FileNotFoundError:
            pytest.skip(
                f"{skip_message}  "
                f"\n{str(filename)} not found in $ADGEMINI_STORE_TESTDATA"
                f" {path_to_stored_files}."
            )

    return ad