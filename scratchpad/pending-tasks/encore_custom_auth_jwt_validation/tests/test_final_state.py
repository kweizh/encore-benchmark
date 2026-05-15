import os
import subprocess
import time
import socket
import pytest
import json

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
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

def test_login_success(start_app):
    """Test Login (Success)"""
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:4000/auth/login", 
         "-H", "Content-Type: application/json", 
         "-d", '{"username": "admin", "password": "password123"}'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert "token" in data, f"Expected 'token' in response, got: {data}"
    assert isinstance(data["token"], str), "Token should be a string"

def test_login_failure(start_app):
    """Test Login (Failure)"""
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "http://localhost:4000/auth/login", 
         "-H", "Content-Type: application/json", 
         "-d", '{"username": "admin", "password": "wrong"}'],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "401", f"Expected HTTP 401, got: {result.stdout}"

def test_profile_unauthenticated(start_app):
    """Test Profile (Unauthenticated)"""
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:4000/profile/me"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "401", f"Expected HTTP 401, got: {result.stdout}"

def test_profile_authenticated(start_app):
    """Test Profile (Authenticated)"""
    # First get the token
    login_result = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:4000/auth/login", 
         "-H", "Content-Type: application/json", 
         "-d", '{"username": "admin", "password": "password123"}'],
        capture_output=True, text=True
    )
    data = json.loads(login_result.stdout)
    token = data["token"]
    
    # Now fetch profile
    profile_result = subprocess.run(
        ["curl", "-s", "-w", "\\n%{http_code}", "-H", f"Authorization: Bearer {token}", "http://localhost:4000/profile/me"],
        capture_output=True, text=True
    )
    
    output_parts = profile_result.stdout.strip().split('\n')
    http_code = output_parts[-1]
    body = '\n'.join(output_parts[:-1])
    
    assert http_code == "200", f"Expected HTTP 200, got: {http_code}. Body: {body}"
    
    try:
        profile_data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {body}")
        
    assert profile_data.get("message") == "Hello admin-1", f"Expected message 'Hello admin-1', got: {profile_data.get('message')}"
    assert profile_data.get("userID") == "admin-1", f"Expected userID 'admin-1', got: {profile_data.get('userID')}"
