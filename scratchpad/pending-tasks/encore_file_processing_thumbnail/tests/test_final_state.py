import os
import subprocess
import time
import socket
import urllib.request
import urllib.error
import json
import pytest

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
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 4000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_file_processing_pipeline(start_app):
    # Send POST request
    url = "http://localhost:4000/image"
    payload = json.dumps({
        "filename": "test.txt",
        "content": "aGVsbG8gd29ybGQ="
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"URL Error: {e.reason}")

    # Check raw file
    raw_path = os.path.join(PROJECT_DIR, "uploads", "raw", "test.txt")
    assert os.path.isfile(raw_path), f"Raw file {raw_path} does not exist."
    with open(raw_path, "r") as f:
        content = f.read()
    assert content == "hello world", f"Expected raw file to contain 'hello world', got '{content}'"

    # Wait for Pub/Sub processing
    time.sleep(5)

    # Check thumbnail file
    thumb_path = os.path.join(PROJECT_DIR, "uploads", "thumbnails", "thumb_test.txt")
    assert os.path.isfile(thumb_path), f"Thumbnail file {thumb_path} does not exist. The Pub/Sub subscription might not be working."
    with open(thumb_path, "r") as f:
        content = f.read()
    assert content == "hello world", f"Expected thumbnail file to contain 'hello world', got '{content}'"
