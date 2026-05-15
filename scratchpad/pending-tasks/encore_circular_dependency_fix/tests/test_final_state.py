import os
import subprocess
import time
import socket
import pytest
import json

PROJECT_DIR = "/home/user/myproject"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

def test_encore_check_passes():
    """Priority 1: Use Encore CLI to verify compilation and no circular dependencies."""
    result = subprocess.run(
        ["encore", "check"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, \
        f"'encore check' failed, indicating circular dependency or compile error: {result.stderr}\n{result.stdout}"

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
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 4000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_endpoint_returns_correct_data(start_app):
    """Priority 1: Verify the endpoint works correctly via curl/subprocess."""
    result = subprocess.run(
        ["curl", "-s", "http://localhost:4000/order/1"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl request failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert "orderId" in data, f"Expected 'orderId' in response, got: {data}"
    assert data["orderId"] == "1", f"Expected orderId to be '1', got: {data['orderId']}"
    assert "user" in data, f"Expected 'user' in response, got: {data}"
