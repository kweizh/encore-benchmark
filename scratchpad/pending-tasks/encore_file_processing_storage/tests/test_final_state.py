import os
import subprocess
import time
import socket
import pytest
import urllib.request
import json
from urllib.error import URLError, HTTPError

PROJECT_DIR = "/home/user/app"

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
    # 1. Send PUT request to /upload/test.txt
    file_content = b"hello world"
    req = urllib.request.Request(
        url="http://localhost:4000/upload/test.txt",
        data=file_content,
        method="PUT"
    )
    req.add_header("Content-Type", "text/plain")
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK for PUT /upload/test.txt, got {response.status}"
    except HTTPError as e:
        pytest.fail(f"PUT /upload/test.txt failed with HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')}")
    except URLError as e:
        pytest.fail(f"PUT /upload/test.txt failed: {e.reason}")

    # 2. Wait for the asynchronous Pub/Sub subscription to process the file
    time.sleep(5)

    # 3. Send GET request to /processed
    try:
        req = urllib.request.Request(url="http://localhost:4000/processed", method="GET")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK for GET /processed, got {response.status}"
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                pytest.fail(f"GET /processed did not return valid JSON: {body}")
                
            # Verify that the response contains test.txt
            assert "test.txt" in str(data), f"Expected 'test.txt' in /processed response, got {data}"
    except HTTPError as e:
        pytest.fail(f"GET /processed failed with HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')}")
    except URLError as e:
        pytest.fail(f"GET /processed failed: {e.reason}")
