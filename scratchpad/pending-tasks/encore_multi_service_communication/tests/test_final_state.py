import os
import subprocess
import time
import socket
import pytest
import json

PROJECT_DIR = "/home/user/multi-service-app"

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

def test_order_create_endpoint(start_app):
    """Priority 1: Use curl to verify the order.create API endpoint."""
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:4000/order/create", 
         "-H", "Content-Type: application/json", 
         "-d", '{"item": "Laptop", "userEmail": "test@example.com"}'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert data.get("orderId") == "12345", f"Expected orderId to be '12345', got: {data.get('orderId')}"
    assert data.get("emailDelivered") is True, f"Expected emailDelivered to be true, got: {data.get('emailDelivered')}"

def test_email_send_endpoint(start_app):
    """Priority 1: Use curl to verify the email.send API endpoint."""
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:4000/email/send", 
         "-H", "Content-Type: application/json", 
         "-d", '{"to": "test@example.com", "body": "hello"}'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert data.get("delivered") is True, f"Expected delivered to be true, got: {data.get('delivered')}"
