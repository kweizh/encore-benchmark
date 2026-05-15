import os
import subprocess
import time
import socket
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

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
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 4000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_ping_endpoint_responses(start_app):
    """Priority 1: Verify the API endpoint via HTTP request."""
    result = subprocess.run(
        ["curl", "-s", "http://localhost:4000/ping"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON response: {result.stdout}")
        
    assert data.get("message") == "pong", f"Expected message 'pong', got {data.get('message')}"

def test_cron_job_definition():
    """Priority 3: Verify the cron job definition in code."""
    ping_file = os.path.join(PROJECT_DIR, "monitor", "ping.ts")
    assert os.path.isfile(ping_file), f"Expected file {ping_file} does not exist."
    
    with open(ping_file, "r") as f:
        content = f.read()
        
    assert "CronJob" in content, "CronJob is not imported or used in ping.ts"
    assert "every:" in content and "1h" in content, "CronJob doesn't have every: '1h' schedule"
    assert "endpoint:" in content and "ping" in content, "CronJob is not targeting the ping endpoint"
