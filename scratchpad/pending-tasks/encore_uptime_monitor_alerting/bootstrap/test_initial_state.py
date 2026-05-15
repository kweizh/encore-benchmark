import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/uptime-monitor"

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json does not exist in {PROJECT_DIR}."

def test_encore_app_exists():
    encore_app_path = os.path.join(PROJECT_DIR, "encore.app")
    assert os.path.isfile(encore_app_path), f"encore.app does not exist in {PROJECT_DIR}."
