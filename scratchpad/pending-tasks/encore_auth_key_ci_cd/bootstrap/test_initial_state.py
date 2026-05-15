import os
import shutil
import subprocess

def test_encore_binary_available():
    """Verify that the encore CLI is available in the PATH."""
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_dir_not_exists():
    """Verify that the project directory does not exist yet."""
    assert not os.path.exists("/home/user/myapp"), "Project directory /home/user/myapp should not exist initially."

def test_script_not_exists():
    """Verify that the deploy script does not exist yet."""
    assert not os.path.exists("/home/user/deploy.sh"), "Script /home/user/deploy.sh should not exist initially."
