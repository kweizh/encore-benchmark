import os
import subprocess
import time
import socket
import urllib.request
import urllib.error
import pytest

PROJECT_DIR = "/home/user/uptime-monitor"

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
    # Start docker daemon
    subprocess.run(["service", "docker", "start"])
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
    if not wait_for_port(4000, timeout=120):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail(f"App failed to start and listen on port 4000. Stderr: {process.stderr.read().decode()}")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)
    subprocess.run(["service", "docker", "stop"])

def test_ping_valid_url(start_app):
    url = "http://localhost:4000/ping?url=https://example.com"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to call ping API: {e}")

    # Verify it saves to database
    result = subprocess.run(
        ["encore", "db", "shell", "uptime", "-c", "SELECT count(*) FROM ping_results WHERE url='https://example.com' AND up=true;"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"encore db shell failed: {result.stderr}"
    assert "1" in result.stdout or "2" in result.stdout or "3" in result.stdout, f"Expected ping result in db, got: {result.stdout}"

def test_ping_invalid_url(start_app):
    url = "http://localhost:4000/ping?url=http://localhost:9999/invalid"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to call ping API: {e}")

    # Verify it saves to database
    result = subprocess.run(
        ["encore", "db", "shell", "uptime", "-c", "SELECT count(*) FROM ping_results WHERE url='http://localhost:9999/invalid' AND up=false;"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"encore db shell failed: {result.stderr}"
    assert "1" in result.stdout or "2" in result.stdout or "3" in result.stdout, f"Expected ping result in db, got: {result.stdout}"

    # Verify it writes to alert.log
    time.sleep(5)
    log_file = os.path.join(PROJECT_DIR, "alert.log")
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."
    with open(log_file) as f:
        content = f.read()
    assert "[ALERT] URL is down: http://localhost:9999/invalid" in content, f"Expected alert in log file, got: {content}"
