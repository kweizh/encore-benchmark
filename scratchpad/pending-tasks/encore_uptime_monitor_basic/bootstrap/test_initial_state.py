import os
import shutil
import pytest

PROJECT_DIR = "/home/user/uptime-monitor"

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_monitor_service_exists():
    ping_ts_path = os.path.join(PROJECT_DIR, "monitor", "ping.ts")
    assert os.path.isfile(ping_ts_path), f"File {ping_ts_path} does not exist."
