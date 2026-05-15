import os
import shutil
import pytest

PROJECT_DIR = "/home/user/app"

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_project_dir_is_empty():
    assert len(os.listdir(PROJECT_DIR)) == 0, f"Project directory {PROJECT_DIR} is not empty."
