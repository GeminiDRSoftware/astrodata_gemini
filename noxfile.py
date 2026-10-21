# pragma: no cover
"""Nox sessions for the astrodata_gemini package."""

import fileinput
import functools
import glob
import importlib.util
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import ClassVar

import nox
from packaging.utils import parse_sdist_filename

# from packaging.requirements import Requirement

sys.path.insert(0, str(Path(__file__).parent))
from nox_utils import dragons_support
from nox_utils.devpi_support import TESTPASS, TESTUSER, DevpiServerManager

# Sessions to run by default when nox is called without arguments.
nox.options.sessions = ["unit_tests"]
nox.options.error_on_external_run = True

PYPROJECT = Path(__file__).parent / "pyproject.toml"

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

    def __new__(cls) -> None:
        """Just catches accidental invocations."""
        message = "This class should not be instantiated."
        raise NotImplementedError(message)


# ------------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------------


def apply_data_caching_environment_variable(session: nox.Session):
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


def build_and_upload_to_devpi(session):
    """Build the package and upload it to the devpi server.

    Arguments
    ---------
    session : nox.Session
        The nox session object.

    Returns
    -------
    str
        The version of the package that was built and uploaded.
    """
    # Build the package.
    tmp_build_dir = Path(session.create_tmp()) / "build"
    tmp_build_dir.mkdir()
    session.run(
        "python", "-m", "build",
        "--sdist",
        "--outdir", str(tmp_build_dir)
    )  # fmt: skip

    # Get the version
    sdist = next(Path(tmp_build_dir).glob("*.tar.gz"))
    name, version = parse_sdist_filename(sdist.name)
    version = str(version)

    # Upload the package to the devpi server.
    session.run(
        "twine",
        "upload",
        "--repository-url", session.env["DEVPI_INDEX_URL"],
        "--username", TESTUSER,
        "--password", TESTPASS,
        str(sdist),
    )  # fmt: skip

    return version


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


def _requirement_name(requirement):
    """Return the normalized package name of a requirement string."""
    return re.split(r"[\s<>=!~;\[]", requirement, maxsplit=1)[0].lower()


def _parse_conda_json(session, output):
    """Return the JSON document found in the output of a conda command.

    Conda can print notices (e.g. "A newer version of conda exists") on
    standard output before, or after, the JSON document.  Skip them.
    """
    start = output.find("{")
    if start >= 0:
        try:
            return json.JSONDecoder().raw_decode(output[start:])[0]
        except ValueError:
            pass
    session.error(f"Unexpected output from conda:\n{output[:2000]}")


def _missing_on_conda(session, python_version, requirements, channels):
    """Return the names of the requirements that conda cannot provide.

    A single dry-run solve of all the requirements, together with the
    session's Python version, tells which ones are not available from the
    channels, taking the version requirements into account.  Nothing is
    installed.

    Arguments
    ---------
    session : nox.Session
        The nox session object.

    python_version : str
        The Python version of the session, e.g. "3.14".

    requirements : list of str
        The requirements to check, in a syntax conda understands.

    channels : list of str
        The conda channels to search.  Only these are searched, not the
        default channels or the ones in the user's .condarc.

    Returns
    -------
    set of str
        The normalized names of the packages that are not available.
    """
    if not requirements:
        return set()

    channel_args = [arg for ch in channels for arg in ("-c", ch)]
    probe_prefix = str(Path(session.create_tmp()) / "probe")

    # The astroconda channel fails at random, so try a few times.
    attempts = 3
    for attempt in range(1, attempts + 1):
        output = session.run(
            "conda", "create", "--dry-run", "--json",
            "--prefix", probe_prefix,
            "--override-channels", *channel_args,
            f"python={python_version}", *requirements,
            silent=True, success_codes=[0, 1],
        )  # fmt: skip
        result = _parse_conda_json(session, output)

        error = result.get("exception_name")
        if error is None:
            return set()
        if error == "PackagesNotFoundError":
            return {_requirement_name(p) for p in result["packages"]}
        if error != "UnavailableInvalidChannel":
            session.error(f"conda could not check the packages: {error}")

        session.log(f"conda channel error (attempt {attempt}/{attempts})")
        if attempt < attempts:
            time.sleep(5)

    session.error("The conda channels are not available.")


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

    channels = SessionVariables.dragons_conda_channels

    # Requirements that conda cannot take (direct references, extras) go
    # straight to pip.  For the others, check which ones are available as
    # conda packages.
    candidates = []
    pip_deps = []
    with fileinput.input(files=str(req_file_path)) as file:
        for line in file:
            stripped = line.strip()
            if not stripped:
                continue

            if (
                "@" in stripped
                or line.startswith("git+")
                or ("[" in stripped and "]" in stripped)
            ):
                pip_deps.append(stripped)
            else:
                candidates.append(stripped)

    missing = _missing_on_conda(
        session, session_python_version, candidates, channels
    )
    conda_deps = []
    for requirement in candidates:
        if _requirement_name(requirement) in missing:
            pip_deps.append(requirement)
        else:
            conda_deps.append(requirement)

    # "conda env update" has no --channel option; the channels are set here.
    # "nodefaults" keeps conda from also searching the default channels.
    env_contents = (
        "channels:\n  - " + "\n  - ".join([*channels, "nodefaults"]) + "\n"
        f"dependencies:\n  - python={session_python_version}\n"
        "  - pip\n"
        "  - " + "\n  - ".join(conda_deps) + "\n"
        "  - pip:\n    - " + "\n    - ".join(pip_deps) + "\n"
    )
    env_file_path = Path(session.create_tmp()) / "environment.yml"
    env_file_path.write_text(env_contents)

    session.run(
        "conda", "env", "update",
        "--prefix", session.virtualenv.location,
        "--quiet",
        "--file", str(env_file_path),
    )  # fmt: skip


def optional_dependencies(*names):
    """Return the requirements of the given extras in pyproject.toml."""
    extras = nox.project.load_toml(PYPROJECT)["project"][
        "optional-dependencies"
    ]
    return [requirement for name in names for requirement in extras[name]]


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
    toml_config = nox.project.load_toml(PYPROJECT)
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
# Decorators
# -----------------------------------------------------------------------


def use_devpi_server(func):
    """Start and stop a devpi server for the session.

    This is used as a function decorator, and must come after the
    ``@nox.session`` decorator.
    """

    @functools.wraps(func)
    def wrapper(session, *args, **kwargs):
        install_pip_test_dependencies(
            session, packages=optional_dependencies("build_test")
        )

        # Launch the devpi server and run the session function.
        with DevpiServerManager(session):
            func(session, *args, **kwargs)

    return wrapper


# -----------------------------------------------------------------------
# Nox Sessions
# -----------------------------------------------------------------------


@nox.session(python=SessionVariables.python_versions)
@use_devpi_server
def build_tests_unit(session):
    """Run the unit tests from a build stored in a devpi server.

    This session will build the package, upload it to an isolated devpi server,
    and run the tests using the build version of the package.
    """
    # build the package and upload it to the devpi server
    version = build_and_upload_to_devpi(session)

    apply_data_caching_environment_variable(session)

    # Switch to a work directory
    working_dir = Path(session.create_tmp())
    with session.chdir(working_dir):
        # install the package from the devpi server.
        install_pip_test_dependencies(session, optionals=["test"])
        session.install(
            "--trusted-host",
            "localhost",
            "--index-url",
            session.env["PIP_INDEX_URL"],
            f"astrodata_gemini=={version}",
        )

        # run the unit tests
        # --import-mode=importlib is needed to ensure that the root repo
        # is not on sys.path, so that the tests are run against the installed
        # package, not the source code in the repo.
        pos_args = session.posargs
        session.run(
            "pytest",
            "--import-mode=importlib",
            *SessionVariables.unit_pytest_options,
            *pos_args,
        )


@nox.session(venv_backend="conda", python=SessionVariables.python_versions)
def conda_unit_tests(session):
    """Run the unit tests with pytest in a conda environment."""
    apply_data_caching_environment_variable(session)
    session.run("conda", "config", "--env", "--add", "channels", "conda-forge")

    install_conda_test_dependencies(session, optionals=["test"])
    session.install("-e", ".", "--no-deps")

    # Positional arguments after -- are passed to pytest
    pytest_args = session.posargs

    # Run the tests.
    session.run(
        "pytest",
        *SessionVariables.unit_pytest_options,
        *pytest_args,
        external=True,
    )


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
def docs(session):
    """Build the documentation."""
    # Install the dependencies for building the docs.
    install_pip_test_dependencies(session, optionals=["docs"])
    session.install("-e", ".", "--no-deps")

    # Build the docs.
    build_dir = Path("docs") / "_build" / "html"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    session.run("sphinx-build", "-W", "--keep-going", "docs", str(build_dir))
    session.log(f"Documentation built in {str(build_dir)}")

    index_location = build_dir / "index.html"
    session.log(
        "Open the documentation in a browser with:\n"
        f"  {index_location.absolute().as_uri()}"
    )


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
