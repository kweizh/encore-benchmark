import os
import stat
import pytest

APP_DIR = "/home/user/myapp"
SCRIPT_PATH = "/home/user/deploy.sh"

def test_encore_app_created():
    """Verify that the Encore app was created."""
    encore_app_file = os.path.join(APP_DIR, "encore.app")
    assert os.path.isfile(encore_app_file), f"Expected encore.app file not found at {encore_app_file}"

def test_deploy_script_exists_and_executable():
    """Verify that deploy.sh exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Deploy script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deploy script {SCRIPT_PATH} is not executable"

def test_deploy_script_contains_install_command():
    """Verify that the deploy script installs the Encore CLI."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "https://encore.dev/install.sh" in content, \
        "Deploy script does not contain the Encore CLI installation command."

def test_deploy_script_contains_auth_command():
    """Verify that the deploy script authenticates using the auth key."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "encore auth login" in content, \
        "Deploy script does not contain the 'encore auth login' command."
    assert "ENCORE_AUTH_KEY" in content, \
        "Deploy script does not use the ENCORE_AUTH_KEY environment variable."

def test_deploy_script_contains_build_command():
    """Verify that the deploy script builds the docker image."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "encore build docker" in content, \
        "Deploy script does not contain the 'encore build docker' command."
    assert "myapp:latest" in content, \
        "Deploy script does not contain the target image name 'myapp:latest'."
