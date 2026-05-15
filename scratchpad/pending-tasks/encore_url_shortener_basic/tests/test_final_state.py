import os
import pytest

PROJECT_DIR = "/home/user/url-shortener"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory not found at {PROJECT_DIR}"

def test_encore_app_file_exists():
    app_file = os.path.join(PROJECT_DIR, "encore.app")
    assert os.path.isfile(app_file), f"encore.app file not found at {app_file}"

def test_url_service_exists():
    url_service_file = os.path.join(PROJECT_DIR, "url", "url.ts")
    assert os.path.isfile(url_service_file), f"URL service file not found at {url_service_file}"

def test_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"package.json file not found at {package_json}"
