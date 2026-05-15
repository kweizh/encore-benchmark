import os
import pytest

PROJECT_DIR = "/home/user/my-saas-app"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} was not created."

def test_encore_app_file_exists():
    app_file = os.path.join(PROJECT_DIR, "encore.app")
    assert os.path.isfile(app_file), f"Encore app file {app_file} does not exist."

def test_frontend_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "frontend", "package.json")
    assert os.path.isfile(package_json), f"Frontend package.json {package_json} does not exist."
