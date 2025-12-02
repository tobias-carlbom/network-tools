import anvil.server
import socket

DEFAULT_TIMEOUT = 3  # seconds


@anvil.server.callable
def check_port(host: str, port: int):
    try:
        resolved_ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        return {
            "host": host,
            "resolved_ip": None,
            "port": port,
            "status": "error",
            "error": f"DNS resolution failed: {e}",
        }

    try:
        with socket.create_connection((resolved_ip, int(port)), timeout=DEFAULT_TIMEOUT):
            status = "OPEN"
    except OSError:
        status = "closed"

    return {
        "host": host,
        "resolved_ip": resolved_ip,
        "port": int(port),
        "status": status,
        "error": None,
    }
