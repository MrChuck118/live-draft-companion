"""Launcher: in-process uvicorn on first free port + auto-open browser (M6a/T42).

Spec Â§7.1 "porta libera auto-rilevata" / RF-001 / MVP-001. The server runs
IN-PROCESS via `uvicorn.Server` (NOT an external `uvicorn` command in PATH),
so the same entrypoint works both in development and inside the PyInstaller
`.exe` (real `.exe` test is T66/T67). Port is chosen here, not in app.main.
"""

from __future__ import annotations

import logging
import socket
import sys
import threading
import time
import webbrowser
from collections.abc import Sequence

import uvicorn

from app.main import app

logger = logging.getLogger("live_draft_companion.launcher")

HOST = "127.0.0.1"
CANDIDATE_PORTS: tuple[int, ...] = (8000, 8001, 8002, 8003)


def find_free_port(ports: Sequence[int] = CANDIDATE_PORTS) -> int | None:
    """Return the first port that can be bound, or None if all are taken."""
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((HOST, port))
            except OSError:
                continue
            return port
    return None


def wait_for_port(host: str, port: int, timeout: float = 5.0) -> bool:
    """Block until something accepts TCP connections on host:port (or timeout)."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.1)
    return False


def _build_server(port: int) -> uvicorn.Server:
    config = uvicorn.Config(app, host=HOST, port=port, log_level="info")
    return uvicorn.Server(config)


def main() -> int:
    """Pick a free port, start uvicorn in-process, open the browser. Returns exit code."""
    logging.basicConfig(level=logging.INFO)

    port = find_free_port()
    if port is None:
        message = "Nessuna porta libera 8000-8003"
        logger.error(message)
        print(message, file=sys.stderr)
        return 1

    url = f"http://localhost:{port}"
    server = _build_server(port)
    thread = threading.Thread(target=server.run, name="uvicorn-server", daemon=True)
    thread.start()

    if not wait_for_port(HOST, port):
        message = f"Server non in ascolto su {url} entro il timeout"
        logger.error(message)
        print(message, file=sys.stderr)
        server.should_exit = True
        return 1

    logger.info("Live Draft Companion in ascolto su %s", url)
    print(f"Live Draft Companion: {url}")
    webbrowser.open(url)

    try:
        thread.join()
    except KeyboardInterrupt:
        server.should_exit = True
        thread.join(timeout=5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
