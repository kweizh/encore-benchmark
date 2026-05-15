import os
import shutil
import pytest

PROJECT_DIR = "/home/user/my-app"
HELLO_FILE = os.path.join(PROJECT_DIR, "hello/hello.ts")

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_hello_file_exists():
    assert os.path.isfile(HELLO_FILE), f"hello.ts file {HELLO_FILE} does not exist."

def test_initial_api_is_internal():
    with open(HELLO_FILE, "r") as f:
        content = f.read()
    assert "expose: true" not in content, "Expected initial API to be internal (missing expose: true)."
