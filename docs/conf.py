# Configuration file for the Sphinx documentation builder.
#

# -- Import sanity check ----------------------------------------------------
# Guard against a stale or duplicate copy of the package being picked up
# from PYTHONPATH (or any other entry on sys.path ahead of the repo itself).
# A stray second copy previously caused a confusing failure deep in
# sphinx.ext.autodoc.importer.get_class_members:
#   TypeError: argument of type 'property' is not iterable
# triggered by sphinx_automodapi's custom `type` attrgetter operating on
# the wrong/stale `Section` class. Fail fast and clearly instead.

import os
import sys

_PACKAGE_NAME = "astrodata_gemini"
_EXPECTED_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")  # adjust if conf.py moves
)


def _check_import_path():
    """Verify the package being documented is loaded from this repo.

    Raises
    ------
    RuntimeError
        If the imported package resolves to a location outside the
        expected repository root, which usually means a stray
        PYTHONPATH entry (or another sys.path entry) is shadowing the
        local checkout with a different copy of the package.
    """
    try:
        module = __import__(_PACKAGE_NAME)
    except ImportError as err:
        raise RuntimeError(
            f"Could not import '{_PACKAGE_NAME}' while building docs. "
            f"Check that it is installed/importable in this environment."
        ) from err

    module_path = os.path.abspath(module.__file__)

    if not module_path.startswith(_EXPECTED_REPO_ROOT):
        pythonpath = os.environ.get("PYTHONPATH", "<not set>")
        raise RuntimeError(
            f"'{_PACKAGE_NAME}' was imported from an unexpected location:\n"
            f"    {module_path}\n"
            f"Expected it to be under:\n"
            f"    {_EXPECTED_REPO_ROOT}\n"
            f"This usually means PYTHONPATH (or another sys.path entry) "
            f"is pointing at a different checkout.\n"
            f"    PYTHONPATH = {pythonpath}\n"
            f"    sys.path   = {sys.path}\n"
            f"Unset PYTHONPATH or remove the offending entry and retry."
        )

_check_import_path()

# --- End of PYTHONPATH check ------------

# -- Project information -----------------------------------------------------

project = 'astrodata_gemini'
copyright = '2026, Association of Universities for Research in Astronomy'
author = 'DRAGONS Team'

from astrodata import __version__
release = __version__

#today = 'April 2026'

# -- General configuration ---------------------------------------------------

# Local extensions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "_ext"))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "gemini_pages",
]

#templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = "index"

# -- Options for doctest extension ---------------------------------------

# Run doctest when building the docs
doctest_test_doctest_blocks = "True"
doctest_show_successes = False

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    "astrodata": ("https://geminidrsoftware.github.io/astrodata/", None),
    "astropy": ("http://docs.astropy.org/en/stable/", None),
    "DRAGONS": ("https://dragons.readthedocs.io/en/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/", None),
}

intersphinx_disabled_reftypes = ["*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_logo = "images/DRAGONS - Icon blue.png"


# -- Customization -------------------------------------------------------------

# Activate the todos
todo_include_todos = True

# By default, when rendering docstrings for classes, sphinx.ext.autodoc will
# make docs with the class-level docstring and the class-method docstrings,
# but not the __init__ docstring, which often contains the parameters to
# class constructors across the scientific Python ecosystem. The option below
# will append the __init__ docstring to the class-level docstring when rendering
# the docs. For more options, see:
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autoclass_content
autoclass_content = "both"

# Automodapi options
numpydoc_show_class_members = False


def setup(app):
   app.add_css_file('custom_code.css')
   app.add_css_file('todo-styles.css')
   app.add_css_file('rtd_theme_overrides.css')
   app.add_css_file('fonts.css')


rst_prolog = """
.. role:: raw-html(raw)
   :format: html

.. |astrodata| replace:: `AstroData <https://geminidrsoftware.github.io/astrodata/>`__
.. |DRAGONS| replace:: `DRAGONS <https://dragons.readthedocs.io/en/stable/>`__

"""
