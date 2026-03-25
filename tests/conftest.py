#ไฟล์ตั้งค่าส่วนกลาง สำหรับการทดสอบด้วย Playwright และ Uvicorn
from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from playwright.sync_api import Browser

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"


def _port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex((host, port)) == 0


@pytest.fixture(scope="session")
def live_server() -> str:
    """Start uvicorn once for Playwright / manual demo."""
    if _port_open(HOST, PORT):
        yield BASE_URL
        return

    env = dict(**__import__("os").environ)
    pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(PROJECT_ROOT) + (__import__("os").pathsep + pythonpath if pythonpath else "")

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            HOST,
            "--port",
            str(PORT),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.time() + 20
    while time.time() < deadline:
        if _port_open(HOST, PORT):
            break
        time.sleep(0.25)
    else:
        process.terminate()
        raise RuntimeError("Uvicorn server did not start in time.")

    try:
        yield BASE_URL
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(scope="session")
def base_url(live_server: str) -> str:
    return live_server


@pytest.fixture
def browser_context_args(browser_context_args, pytestconfig):
    """Configure browser context when running in headed mode.""" 
    return browser_context_args


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """Configure browser launch with slow_mo when running in headed mode."""
    # Check if --headed flag is used (indicates headed mode)  
    headed = pytestconfig.getoption("--headed", default=False)
    
    if headed:
        return {**browser_type_launch_args, "slow_mo": 1000}  # 1 second delay
    return browser_type_launch_args
