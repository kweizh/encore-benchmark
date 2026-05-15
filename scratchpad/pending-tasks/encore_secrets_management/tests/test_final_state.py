import os
import subprocess
import time
import socket
import json
import pytest
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/my-app"

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
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 4000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_secrets_file_exists():
    """Priority 3 fallback: basic file existence check."""
    secrets_file = os.path.join(PROJECT_DIR, ".secrets.local.cue")
    assert os.path.isfile(secrets_file), f".secrets.local.cue not found at {secrets_file}"
    
    with open(secrets_file, "r") as f:
        content = f.read()
    
    assert "ThirdPartyToken" in content, "Expected 'ThirdPartyToken' in .secrets.local.cue"
    assert "my-super-secret-token" in content, "Expected 'my-super-secret-token' in .secrets.local.cue"

def test_token_endpoint(start_app):
    """Priority 1: Test the endpoint returns the secret value."""
    try:
        req = urllib.request.Request("http://localhost:4000/token")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert "token" in data, f"Expected 'token' in response, got {data}"
            assert data["token"] == "my-super-secret-token", f"Expected token 'my-super-secret-token', got {data['token']}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to request /token endpoint: {e}")
