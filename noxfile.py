# pragma: no cover
"""Nox sessions for the astrodata_gemini package."""

import fileinput
import functools
import glob
import importlib.util
import os
import sys
from pathlib import Path
from typing import ClassVar

import nox
from packaging.requirements import Requirement

sys.path.insert(0, str(Path(__file__).parent))
from nox_utils import dragons_support
from nox_utils.devpi_support import devpi_available_port

# Sessions to run by default when nox is called without arguments.
nox.options.sessions = ["unit_tests"]
nox.options.error_on_external_run = True


# ----------------------------------------------------------------------
# Session Variables
# -----------------------------------------------------------------------


class SessionVariables:
    """Session variables for the nox sessions."""

    # Python versions:
    python_versions: ClassVar[list[str]] = [
        "3.12",
        "3.13",
        "3.14",
    ]  # fmt: skip

    # paths to test directories
    unit_test_dir = Path(__file__).parent / "tests" / "unit"
    integration_test_dir = Path(__file__).parent / "tests" / "integration"

    # pytest options for the test sessions
    pytest_options = []
    pytest_options = ["--cov=astrodata_gemini", "--cov-report=term-missing"]
    unit_pytest_options = pytest_options + [str(unit_test_dir)]
    integration_pytest_options = pytest_options + [str(integration_test_dir)]

    # conda channels and url for DRAGONS integration tests
    dragons_conda_channels: ClassVar[list[str]] = (
        dragons_support.dragons_conda_channels
    )
    dragons_venv_params = dragons_support.dragons_venv_params
    dragons_github_url = dragons_support.dragons_github_url

    # devpi server information
    devpi_host = "localhost"
    devpi_initial_port = 1420

    @classmethod
    @functools.cache
    def devpi_port(cls):
        """Return the devpi port."""
        return devpi_available_port(cls.devpi_host, cls.devpi_initial_port)

    @classmethod
    def devpi_url(cls):
        """Return the devpi url."""
        return f"http://{cls.devpi_host}:{cls.devpi_port()}/"

    def __new__(cls) -> None:
        """Just catches accidental invocations."""
        message = "This class should not be instantiated."
        raise NotImplementedError(message)


# ------------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------------


def apply_data_caching_environment_variable(session: nox.Session) -> None:
    """Add a test caching env var to the session's environment."""
    default_data_cache_path = str(Path(os.getcwd()) / "_test_data_cache")

    # astrodata.testing.download_from_archive() will download the files
    # into this location.
    session.env["ADGEMINI_TESTDATA"] = (
        os.getenv("ADGEMINI_TESTDATA") or default_data_cache_path
    )

    # Non-downloadable files (e.g. reduced data) are stored in the
    # $ADGEMINI_STORE_TESTDATA directory.
    session.env["ADGEMINI_STORE_TESTDATA"] = (
        os.getenv("ADGEMINI_STORE_TESTDATA") or default_data_cache_path
    )


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


def install_pip_test_dependencies(session, packages=None, optionals=[]):
    """Install the test dependencies from pyproject.toml using pip.

    Arguments
    ---------
    session : nox.Session
        The nox session object.

    packages : list of str, optional
        A list of the packages to install. If not specified, the packages
        will be read from pyproject.toml.

    optionals : list of str
        A list of the optional dependencies to include in the installation.
        The valid options are defined under the [project.optional-dependencies]
        section of pyproject.toml.
    """
    # If using venv, upgrade pip first. Report the pip version.
    # Not needed if backend is a conda environment.
    if session.venv_backend == "venv":
        session.install("--upgrade", "pip")
        session.run("python", "-m", "pip", "--version")

    # Write the requirements.txt file if no packages are specified,
    # otherwise write the specified packages to a temporary requirements.txt
    # file.
    if not packages:
        req_file_path = write_req_file(session, optionals=optionals)
    else:
        req_file_path = Path(session.create_tmp()) / "requirements.txt"
        req_file_path.write_text("\n".join(packages) + "\n")

    # Install the dependencies from the requirements.txt file.
    # The timeout helps when devpi is used in a conda environment.
    session.install("-r", str(req_file_path), "--timeout=30")


def install_conda_test_dependencies(session, packages=None, optionals=[]):
    """Install the test dependencies from pyproject.toml using conda.

    Arguments
    ---------
    session : nox.Session
        The nox session object.

    packages : list of str, optional
        A list of the packages to install. If not specified, the packages
        will be read from pyproject.toml.

    optionals : list of str
        A list of the optional dependencies to include in the installation.
        The valid options are defined under the [project.optional-dependencies]
        section of pyproject.toml.
    """
    # Write the requirements.txt file if no packages are specified,
    # otherwise write the specified packages to a temporary requirements.txt
    # file.
    if not packages:
        # write_req_file will always include the project dependencies.
        req_file_path = write_req_file(session, optionals=optionals)
    else:
        req_file_path = Path(session.create_tmp()) / "requirements.txt"
        req_file_path.write_text("\n".join(packages) + "\n")

    # Get the session's python version.
    cmd = [
        "python",
        "-c",
        (
            "import sys;"
            "print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        ),
    ]
    session_python_version = session.run(*cmd, silent=True).strip()

    # The requirements file may contain PEP 508 environment markers
    # (e.g. numpy's python_version-conditioned pins). conda cannot
    # parse those. Evaluate each marker for this session's Python
    # version and strip it, dropping any requirement that doesn't
    # apply.
    with fileinput.input(files=str(req_file_path), inplace=True) as file:
        for line in file:
            stripped = line.strip()
            if not stripped:
                continue

            requirement = Requirement(stripped)

            if requirement.marker is None or requirement.marker.evaluate(
                environment={"python_version": session_python_version}
            ):
                requirement.marker = None
                print(str(requirement), end="\n")

    session.conda_install(
        "--quiet",
        "--file",
        str(req_file_path),
        channel=SessionVariables.dragons_conda_channels,
    )


def write_req_file(session, optionals=[]):
    """Write the requirements.txt file from pyproject.toml.

    Arguments
    ---------
    session : nox.Session
        The nox session object.

    optionals : list of str
        A list of the optional dependencies to include in the
        requirements.txt file.  The valid options are defined under the
        [project.optional-dependencies] section of pyproject.toml.
    """
    # Get the dependencies from pyproject.toml
    toml_config = nox.project.load_toml("pyproject.toml")
    requirements = toml_config["project"]["dependencies"]
    for optional in optionals:
        requirements += toml_config["project"]["optional-dependencies"].get(
            optional, []
        )

    # Write the requirements to a temporary file
    req_file_path = Path(session.create_tmp()) / "requirements.txt"
    req_file_path.write_text("\n".join(requirements) + "\n")

    # Log list to the session log
    session.log(f"Requirements written to {req_file_path}")
    session.log("\n".join(requirements) + "\n")

    return req_file_path


# -----------------------------------------------------------------------
# Nox Sessions
# -----------------------------------------------------------------------


@nox.session(python="3.14")
def coverage(session):
    """Build the coverage reports and badge from the .coverage data file.

    The data is collected by pytest-cov in the unit_tests session, so run
    that session first.
    """
    if not Path(".coverage").exists():
        session.error("No .coverage file; run the unit_tests session first.")

    session.install("coverage>=7.15", "genbadge[coverage]>=1.1.3")

    # Generate the coverage report.
    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "html")

    # Create a coverage badge
    session.run("coverage", "xml")
    Path("_badges").mkdir(exist_ok=True)
    session.run(
        "genbadge",
        "coverage",
        "-i", "./coverage.xml",
        "-o", "_badges/coverage.svg"
    )  # fmt: skip


@nox.session
def linting(session):
    """Run the linters.

    Only ruff is needed.  The files, the rules and the line length are set in
    [tool.ruff] in pyproject.toml.  Keep the ruff version in step with the
    one in .pre-commit-config.yaml.
    """
    session.install("ruff==0.17.0")

    # On GitHub Actions, annotate the pull request with the errors.
    check_options = []
    if os.environ.get("GITHUB_ACTIONS"):
        check_options.append("--output-format=github")

    session.run("ruff", "check", *check_options, ".")
    session.run("ruff", "format", "--diff", ".")


@nox.session(venv_backend="venv", python="3.14")
def pre_download_test_data(session):
    """Pre-download test data for the unit and integration tests."""
    apply_data_caching_environment_variable(session)

    # Install pytest and astrodata for downloading test data
    install_pip_test_dependencies(session, packages=["astrodata"])

    # Get the file names from the LUTs.
    lut_tag_path = SessionVariables.unit_test_dir / "lut_tags.py"
    lut_tags_dict = get_lut_data("lut_tags", lut_tag_path).tags_data

    # Get list of descriptor LUTs
    desc_luts_paths = glob.glob(
        str(SessionVariables.unit_test_dir / "*_lut_descriptors.py")
    )

    # Get the descriptor LUTs data
    desc_all_keys = set()
    for lut_path in desc_luts_paths:
        lut_name = Path(lut_path).stem
        lut_descriptors_dict = get_lut_data(
            lut_name, lut_path
        ).descriptors_data
        desc_all_keys = desc_all_keys | set(lut_descriptors_dict.keys())

    all_keys = set(lut_tags_dict.keys()) | desc_all_keys

    failed_to_download = []
    for _, filename in all_keys:
        cmd = (
            "import astrodata; "
            "path = astrodata.testing.download_from_archive("
            f"'{filename}', env_var='ADGEMINI_TESTDATA', "
            "fail_on_error=False); "
            "print('DOWNLOAD_FAILED' if path is None else path)"
        )
        output = session.run("python", "-c", cmd, silent=True)
        RED = "\033[31m"
        GREEN = "\033[32m"
        RESET = "\033[0m"
        if "DOWNLOAD_FAILED" in output:
            failed_to_download.append(filename)
            session.log(f"{RED}Not downloadable: {filename}{RESET}")
        else:
            session.log(f"{GREEN}Downloaded: {filename}{RESET}")

    if failed_to_download:
        session.log(
            f"{RED}Failed to download the following files (they might be "
            f"derivatives: {RESET}\n{'\n'.join(failed_to_download)}\n"
        )


@nox.session(python=SessionVariables.python_versions)
def unit_tests(session):
    """Run the unit tests with pytest."""
    apply_data_caching_environment_variable(session)
    install_pip_test_dependencies(session, optionals=["test"])
    session.install("-e", ".", "--no-deps")

    # Positional arguments after -- are passed to pytest
    pytest_args = session.posargs

    # Run the tests.
    session.run("pytest", *SessionVariables.unit_pytest_options, *pytest_args)


# -------------------------------------------------------------------------
# Development Environment Session
# -------------------------------------------------------------------------


@nox.session
def devshell(session):
    """Create a development environment with all dependencies installed.

    To not activate the pre-commit hooks, use the --no-pre-commit option.
    Eg.  nox -s devshell -- --no-pre-commit
    """
    venv_name = "adgemini_venv"
    venv_path = Path("." + venv_name + "/").absolute()
    activate_path = venv_path / "bin" / "activate"
    venv_python = venv_path / "bin" / "python"

    # Remove any existing virtual environment
    if venv_path.exists():
        session.run("rm", "-rf", str(venv_path), external=True)

    # Create fresh virtual environment
    session.run("python", "-m", "venv", str(venv_path), "--prompt", venv_name)

    # Install dependencies in the virtual environment
    req_file_path = write_req_file(
        session, optionals=["dev", "docs", "test", "build_test"]
    )

    session.run(
        str(venv_python),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
        external=True,
    )

    session.run(
        str(venv_python),
        "-m",
        "pip",
        "install",
        "-r",
        str(req_file_path),
        external=True,
    )

    # Install the package itself in editable mode
    session.run(
        str(venv_python),
        "-m",
        "pip",
        "install",
        "-e",
        ".",
        "--no-deps",
        external=True,
    )

    session.log("Virtual environment created.")
    session.log("Activate the environment with:")
    session.log(f"  source {activate_path.relative_to(Path.cwd())}")
    session.log("Deactivate the environment with: deactivate")

    if "--no-pre-commit" not in session.posargs:
        session.notify("initialize_pre_commit")


@nox.session(python="3.14")
def initialize_pre_commit(session):
    """Initialize pre-commit hooks."""
    session.install("pre-commit")
    session.run(
        "pre-commit",
        "install",
        "--install-hooks",
        "--hook-type=pre-commit",
        "--hook-type=commit-msg",
    )


@nox.session(python="3.14")
def deactivate_pre_commit(session):
    """Deactivate pre-commit hooks."""
    session.install("pre-commit")
    session.run(
        "pre-commit",
        "uninstall",
        "--hook-type=pre-commit",
        "--hook-type=commit-msg",
    )


# ------
