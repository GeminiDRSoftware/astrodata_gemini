"""Support functions for the devpi test-index nox sessions."""

import shutil
import socket
import subprocess
import time
from contextlib import closing
from pathlib import Path

import nox

HOST = "localhost"
INITIAL_PORT = 1420


class DevpiServerError(RuntimeError):
    """Exception for devpi server errors."""

    def __init__(self, message: str):
        """Initialize the error."""
        super().__init__(f"Problem with devpi server: {message}")


class DevpiServerManager:
    """Context manager that will start and stop a devpi server."""

    def __init__(self, session, tmp_dir=None):
        """Initialize the context manager."""
        self.session = session
        self.tmp_dir = tmp_dir

        self.host = HOST
        self.port = devpi_available_port(self.host, INITIAL_PORT)
        self.url = f"http://{self.host}:{self.port}/"

        # Initialize other attributes.
        self.index_url = None
        self.server_process = None

        # Initialization methods
        self.configure_devpi_tmp_dir()

    def __enter__(self):
        """Start the devpi server."""
        self.generate_config_file()
        self.start_devpi_server()

    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the devpi server."""
        self.stop_devpi_server()

    def configure_devpi_tmp_dir(self):
        """Configure the temporary directory for the devpi server."""
        session = self.session
        tmp_dir = self.tmp_dir

        if tmp_dir is None:
            tmp_dir = Path(session.create_tmp()) / "devpi"

        tmp_dir = Path(tmp_dir).absolute()
        tmp_dir.mkdir()

        self.tmp_dir = tmp_dir

    def generate_config_file(self):
        """Generate the devpi configuration file."""
        session = self.session
        tmp_dir = self.tmp_dir
        port = self.port

        with session.cd(tmp_dir):
            session.run("devpi-init", "--serverdir", ".")
            session.run(
                "devpi-gen-config", "--serverdir", tmp_dir, "--port", str(port)
            )

    def wait_for_devpi_startup(self, session):
        """Wait for the devpi server to start.

        This assumes that the server has been started, there is no check for
        the server process itself.  It performs a curl request to the devpi
        server to check if it is running, and it will pass for any kind of
        response.
        """
        timeout = 25
        started = False

        for check in range(1, timeout + 1):
            session.log(f"Checking for devpi server... {check}/{timeout}")

            try:
                session.run("curl", self.url, silent=True, external=True)
                started = True
                break

            except nox.command.CommandFailed:
                time.sleep(1)

        # If the process has failed, show the output and stderr
        session.log(f"Server process: {self.server_process.pid}")

        return started

    def check_devpi_server_process(self):
        """Check that the devpi server process is running without issue."""
        server_process = self.server_process
        session = self.session
        started = self.wait_for_devpi_startup(session)

        if server_process.poll() is not None or not started:
            stdout, stderr = server_process.communicate()
            session.log(f"stdout: {stdout}")
            session.log(f"stderr: {stderr}")

            message = "Devpi server failed to start."
            raise DevpiServerError(message)

    def start_devpi_server(self):
        """Start the devpi server."""
        session = self.session
        tmp_dir = self.tmp_dir
        port = self.port

        # Check that the server is available.  It is installed in the
        # session's environment, which is not on the PATH of the nox process.
        devpi_server_path = shutil.which("devpi-server", path=session.bin)
        if devpi_server_path is None:
            message = "devpi-server is not installed in the session."
            raise DevpiServerError(message)

        # The request-timeout helps when using a conda environment.
        self.server_process = subprocess.Popen(
            [
                devpi_server_path,
                "--serverdir", tmp_dir,
                "--port", str(port),
                "--request-timeout", "30",
            ],  # noqa: S603
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )  # fmt: skip

        # Wait for the server to start
        session.log("Waiting for devpi server to start...")

        # If the process has failed, show the output and stderr
        self.check_devpi_server_process()

        session.log(f"Server process: {self.server_process.pid}")

        self.configure_devpi_client()

    def configure_devpi_client(self):
        """Configure the devpi client."""
        session = self.session

        # Configure the devpi client
        session.run("devpi", "use", self.url)
        session.run("devpi", "user", "-c", "testuser", "password=123")
        session.run("devpi", "login", "testuser", "--password=123")
        session.run("devpi", "index", "-c", "dev", "bases=root/pypi")
        session.run("devpi", "use", "-l")
        session.run("devpi", "use", "testuser/dev")
        session.run(
            "devpi",
            "index",
            "testuser/dev",
            "mirror_whitelist=astrodata_gemini",
        )

        # Set the pip index URL
        session.env["DEVPI_INDEX_URL"] = f"{self.url}testuser/dev/"
        session.env["PIP_INDEX_URL"] = f"{self.url}testuser/dev/+simple/"

        self.index_url = f"{self.url}testuser/dev/+simple/"

    def stop_devpi_server(self):
        """Stop the devpi server."""
        session = self.session
        tmp_dir = self.tmp_dir

        session.log("Stopping devpi server...")

        if self.server_process is not None:
            self.server_process.terminate()
            self.server_process.wait()

        if tmp_dir is not None and tmp_dir.exists():
            # tmp_dir should be the absolute path by now.
            shutil.rmtree(tmp_dir)


def devpi_available_port(host, initial_port):
    """
    Find an available port starting from the initial_port.

    If the initial_port is not available, increment the port number until
    an available one is found.
    """
    port = initial_port

    # In case there's a bug/issue, only try a specific number of times.
    attempts = 1000

    # Check if the port is available by trying to connect to it.
    # If the connection fails, the port is available and can be used for
    # the devpi server.
    af_inet, sock_stream = socket.AF_INET, socket.SOCK_STREAM
    with closing(socket.socket(af_inet, sock_stream)) as sock:
        for _ in range(attempts):
            if sock.connect_ex((host, port)) != 0:
                break

            port += 1

    return port
