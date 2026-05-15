import shutil
import subprocess

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_docker_binary_available():
    assert shutil.which("docker") is not None, "docker binary not found in PATH."

def test_docker_is_running():
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        assert False, "Docker daemon is not running or accessible."
