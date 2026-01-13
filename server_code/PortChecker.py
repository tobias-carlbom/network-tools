import anvil.server
import socket

DEFAULT_TIMEOUT = 3  # seconds


def _resolve_host(host: str):
    try:
        return socket.gethostbyname(host), None
    except socket.gaierror as e:
        return None, f"DNS resolution failed: {e}"


@anvil.server.callable
def check_port(host: str, port: int):
    resolved_ip, err = _resolve_host(host)
    if err:
        return {
            "host": host,
            "resolved_ip": None,
            "port": int(port),
            "status": "error",
            "error": err,
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


@anvil.server.callable
def check_udp_port(host: str, port: int):
    resolved_ip, err = _resolve_host(host)
    if err:
        return {
            "host": host,
            "resolved_ip": None,
            "port": int(port),
            "status": "error",
            "error": err,
        }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(DEFAULT_TIMEOUT)

    try:
        sock.connect((resolved_ip, int(port)))
        try:
            sock.send(b"\x00")
        except OSError:
            return {
                "host": host,
                "resolved_ip": resolved_ip,
                "port": int(port),
                "status": "closed",
                "error": None,
            }

        try:
            sock.recv(1)
            status = "OPEN"
        except socket.timeout:
            status = "OPEN|filtered"
        except OSError:
            status = "closed"
    finally:
        try:
            sock.close()
        except Exception:
            pass

    return {
        "host": host,
        "resolved_ip": resolved_ip,
        "port": int(port),
        "status": status,
        "error": None,
    }
