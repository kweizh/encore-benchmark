import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/uptime-monitor"

def test_ping_all_endpoint_via_encore_check():
    """Priority 1: Use encore check to verify the endpoint is active and returns the expected result."""
    result = subprocess.run(
        ["encore", "check", "curl /ping-all"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'encore check' failed: {result.stderr}\n{result.stdout}"
    assert '{"success":true}' in result.stdout or '{"success": true}' in result.stdout, \
        f"Expected {{\"success\":true}} in output, got: {result.stdout}"

def test_cron_job_defined_in_file():
    """Priority 3 fallback: check that the CronJob is defined in the file."""
    ping_ts_path = os.path.join(PROJECT_DIR, "monitor", "ping.ts")
    with open(ping_ts_path) as f:
        content = f.read()
    
    assert "CronJob" in content, "Expected 'CronJob' to be used in monitor/ping.ts."
    assert "ping-urls" in content, "Expected CronJob to be named 'ping-urls'."
    assert "1h" in content, "Expected CronJob to run every '1h'."
    assert "pingAll" in content, "Expected CronJob to call 'pingAll' endpoint."
