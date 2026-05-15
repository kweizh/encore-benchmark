import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/my-app"
HELLO_FILE = os.path.join(PROJECT_DIR, "hello/hello.ts")

def test_api_is_exposed():
    """Priority 3: Check that expose: true is in the file."""
    assert os.path.isfile(HELLO_FILE), f"hello.ts file {HELLO_FILE} does not exist."
    with open(HELLO_FILE, "r") as f:
        content = f.read()
    
    assert "expose: true" in content, "Expected 'expose: true' to be present in hello.ts."

def test_encore_check_succeeds():
    """Priority 1: Run encore check to ensure the project is still valid."""
    result = subprocess.run(
        ["encore", "check"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'encore check' failed: {result.stderr}\n{result.stdout}"
