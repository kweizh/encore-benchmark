import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_encore_app_file_exists():
    app_file = os.path.join(PROJECT_DIR, "encore.app")
    assert os.path.isfile(app_file), f"Encore app file {app_file} does not exist."

def test_services_exist():
    order_dir = os.path.join(PROJECT_DIR, "order")
    user_dir = os.path.join(PROJECT_DIR, "user")
    assert os.path.isdir(order_dir), f"Service directory {order_dir} does not exist."
    assert os.path.isdir(user_dir), f"Service directory {user_dir} does not exist."

def test_circular_dependency_exists():
    result = subprocess.run(["encore", "check"], cwd=PROJECT_DIR, capture_output=True, text=True)
    # The check should fail due to circular dependency
    assert result.returncode != 0, "Expected 'encore check' to fail initially, but it succeeded."
    assert "import cycle" in result.stderr or "circular dependency" in result.stderr or "cycle" in result.stderr or "import cycle" in result.stdout or "cycle" in result.stdout, "Expected circular dependency error in output."
