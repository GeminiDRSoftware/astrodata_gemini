"""Support functions for the devpi test-index nox sessions."""

import socket
from contextlib import closing


def devpi_available_port(host, initial_port):
    """
    Find an available port starting from the initial_port.

    If the initial_port is not available, increment the port number until
    an available one is found.
    """
    port = initial_port

    # In case there's a bug/issue, only try a specific number of times.
    attempts = 1000

    af_inet, sock_stream = socket.AF_INET, socket.SOCK_STREAM
    with closing(socket.socket(af_inet, sock_stream)) as sock:
        for _ in range(attempts):
            if sock.connect_ex((host, port)) != 0:
                break

            port += 1

    return port
