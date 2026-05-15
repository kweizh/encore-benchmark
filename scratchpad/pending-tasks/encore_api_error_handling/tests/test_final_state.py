import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
from urllib.error import HTTPError

PROJECT_DIR = "/home/user/myproject"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["encore", "run"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(4000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 4000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_valid_request(start_app):
    url = "http://localhost:4000/hello/world"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("message") == "Hello world", f"Expected message 'Hello world', got {data}"
    except Exception as e:
        pytest.fail(f"Request to {url} failed: {e}")

def test_error_request(start_app):
    url = "http://localhost:4000/hello/error"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            pytest.fail(f"Expected HTTP 404 error, but request succeeded with status {response.status}")
    except HTTPError as e:
        assert e.code == 404, f"Expected HTTP 404, got {e.code}"
        data = json.loads(e.read().decode('utf-8'))
        assert data.get("code") == "not_found", f"Expected error code 'not_found', got {data.get('code')}"
        assert data.get("message") == "name not found", f"Expected error message 'name not found', got {data.get('message')}"
    except Exception as e:
        pytest.fail(f"Request to {url} failed with unexpected error: {e}")
