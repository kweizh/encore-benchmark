import os
import shutil
import pytest

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_docker_binary_available():
    assert shutil.which("docker") is not None, "docker binary not found in PATH."

def test_dockerd_binary_available():
    assert shutil.which("dockerd") is not None, "dockerd binary not found in PATH."

def test_home_user_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."