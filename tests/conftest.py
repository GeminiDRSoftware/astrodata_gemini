# conftest.py — loads before any test_*.py is collected
import copy
import sys

import astrodata

import astrodata_gemini  # noqa: F401  (plugin: registers the AstroData classes)


def pytest_report_header(config):
    return (
        f"astrodata_gemini {astrodata_gemini.__version__}: "
        f"{astrodata_gemini.__file__}"
    )


if any(m == "astrofaker" or m.startswith("astrofaker.") for m in sys.modules):
    raise RuntimeError(
        "astrofaker was already imported before conftest.py ran — "
        "registry snapshot will not be clean."
    )

_CLEAN_REGISTRY = copy.deepcopy(astrodata.factory._registry)
# Sanity check: the snapshot should contain real classes, not just
# the AstroData base class.
assert len(_CLEAN_REGISTRY) > 1, (
    "Registry snapshot is empty — astrodata_gemini import may not have "
    "registered classes as expected; check import order."
)
