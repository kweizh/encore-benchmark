import os
import subprocess
import time
import socket
import json
import urllib.request
import urllib.error
import pytest

PROJECT_DIR = "/home/user/url-shortener"

def wait_for_port(port, timeout=120):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the Docker daemon if it's not running (for dind environments)
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        subprocess.Popen(["dockerd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        
    # Start the app
    process = subprocess.Popen(
        ["encore", "run"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(4000, timeout=180):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 4000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_url_shortening_and_analytics(start_app):
    """Priority 1/3: Test the actual API endpoints to verify the system behavior."""
    # 1. Shorten URL
    req = urllib.request.Request(
        "http://localhost:4000/url",
        data=json.dumps({"url": "https://example.com"}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            data = json.loads(response.read().decode())
            assert "id" in data, f"Expected 'id' in response, got {data}"
            short_id = data["id"]
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to shorten URL: {e}")

    # 2. Redirect URL
    req = urllib.request.Request(f"http://localhost:4000/{short_id}", method="GET")
    try:
        # We don't want urllib to automatically follow redirects if it's a 30x
        # But if it does, it will go to example.com.
        # Let's use a custom opener that doesn't follow redirects
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def http_error_302(self, req, fp, code, msg, headers):
                return urllib.response.addinfourl(fp, headers, req.get_full_url(), code)
            http_error_301 = http_error_303 = http_error_307 = http_error_302
            
        opener = urllib.request.build_opener(NoRedirectHandler)
        response = opener.open(req)
        # It could be a redirect (30x) or just returning the URL in JSON (200)
        assert response.status in [200, 301, 302, 303, 307, 308], f"Expected redirect or success, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to resolve URL: {e}")

    # 3. Wait for Pub/Sub
    time.sleep(2)

    # 4. Check Analytics
    req = urllib.request.Request(f"http://localhost:4000/analytics/{short_id}", method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            data = json.loads(response.read().decode())
            # Depending on implementation, it might be 'clicks', 'count', etc.
            # We will check if any value in the dict equals 1.
            assert any(v == 1 for v in data.values()), f"Expected click count to be 1, got {data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to check analytics: {e}")
