"""Tests for launcher: port fallback + auto-browser (M6a/T42).

Hermetic: the real server is never started; uvicorn/webbrowser are mocked
and find_free_port runs against ephemeral OS-assigned ports (no reliance on
fixed 8000-8003 being free in the test environment).
"""

import socket

import launcher


def _bind_ephemeral() -> tuple[socket.socket, int]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((launcher.HOST, 0))
    return sock, sock.getsockname()[1]


def _free_port() -> int:
    sock, port = _bind_ephemeral()
    sock.close()
    return port


def test_find_free_port_skips_busy_returns_next() -> None:
    busy_sock, busy_port = _bind_ephemeral()
    free_port = _free_port()
    try:
        result = launcher.find_free_port([busy_port, free_port])
        assert result == free_port
    finally:
        busy_sock.close()


def test_find_free_port_all_busy_returns_none() -> None:
    sock_a, port_a = _bind_ephemeral()
    sock_b, port_b = _bind_ephemeral()
    try:
        assert launcher.find_free_port([port_a, port_b]) is None
    finally:
        sock_a.close()
        sock_b.close()


def test_wait_for_port_false_when_closed() -> None:
    closed_port = _free_port()
    assert launcher.wait_for_port(launcher.HOST, closed_port, timeout=0.3) is False


def test_wait_for_port_true_when_listening() -> None:
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((launcher.HOST, 0))
    listener.listen(1)
    port = listener.getsockname()[1]
    try:
        assert launcher.wait_for_port(launcher.HOST, port, timeout=1.0) is True
    finally:
        listener.close()


def test_main_opens_browser_on_chosen_port(monkeypatch) -> None:
    chosen_port = 8002
    build_calls: list[int] = []
    opened: list[str] = []

    class FakeServer:
        def __init__(self) -> None:
            self.should_exit = False

        def run(self) -> None:  # returns immediately -> thread ends, join() unblocks
            return None

    monkeypatch.setattr(launcher, "find_free_port", lambda ports=None: chosen_port)

    def fake_build(port: int) -> FakeServer:
        build_calls.append(port)
        return FakeServer()

    monkeypatch.setattr(launcher, "_build_server", fake_build)
    monkeypatch.setattr(launcher, "wait_for_port", lambda host, port, timeout=5.0: True)
    monkeypatch.setattr(launcher.webbrowser, "open", lambda url: opened.append(url))

    exit_code = launcher.main()

    assert exit_code == 0
    assert build_calls == [chosen_port]
    assert opened == [f"http://localhost:{chosen_port}"]


def test_main_returns_1_when_all_ports_busy(monkeypatch) -> None:
    monkeypatch.setattr(launcher, "find_free_port", lambda ports=None: None)
    monkeypatch.setattr(
        launcher.webbrowser, "open", lambda url: pytest_fail_if_called()
    )

    assert launcher.main() == 1


def pytest_fail_if_called() -> None:
    raise AssertionError("browser must not open when no port is free")
