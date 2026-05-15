import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/todo-app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start Docker daemon
    dockerd_process = subprocess.Popen(
        ["dockerd"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    time.sleep(5) # Wait for Docker to be ready

    # Start the app
    process = subprocess.Popen(
        ["encore", "run"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(4000, timeout=120):
        # Kill the processes before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        os.killpg(os.getpgid(dockerd_process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 4000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)
    
    os.killpg(os.getpgid(dockerd_process.pid), signal.SIGTERM)
    dockerd_process.wait(timeout=30)

def test_post_todo(start_app):
    """Test POST /todo endpoint inserts an item and returns an id."""
    data = json.dumps({"title": "Buy milk"}).encode('utf-8')
    req = urllib.request.Request("http://localhost:4000/todo", data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            res_body = json.loads(response.read().decode('utf-8'))
            assert "id" in res_body, f"Expected 'id' in response, got {res_body}"
    except urllib.error.URLError as e:
        pytest.fail(f"POST request failed: {e}")

def test_get_todo(start_app):
    """Test GET /todo endpoint returns the inserted item."""
    req = urllib.request.Request("http://localhost:4000/todo", method='GET')
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            res_body = json.loads(response.read().decode('utf-8'))
            
            # The response could be an array or an object containing an array.
            # We'll check if the string 'Buy milk' is in the JSON representation.
            res_str = json.dumps(res_body)
            assert "Buy milk" in res_str, f"Expected 'Buy milk' in GET response, got {res_str}"
    except urllib.error.URLError as e:
        pytest.fail(f"GET request failed: {e}")
