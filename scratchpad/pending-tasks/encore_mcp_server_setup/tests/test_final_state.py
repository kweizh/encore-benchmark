import os
import json
import pytest

PROJECT_DIR = "/home/user/app"
MCP_JSON_PATH = os.path.join(PROJECT_DIR, ".cursor", "mcp.json")

def test_mcp_json_exists():
    """Priority 3: Check if the .cursor/mcp.json file exists."""
    assert os.path.isfile(MCP_JSON_PATH), f"mcp.json file not found at {MCP_JSON_PATH}"

def test_mcp_json_content():
    """Priority 3: Verify the content of the .cursor/mcp.json file."""
    with open(MCP_JSON_PATH, "r") as f:
        try:
            content = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse mcp.json as valid JSON: {e}")
            
    assert "mcpServers" in content, "mcp.json is missing 'mcpServers' object."
    assert "encore-local" in content["mcpServers"], "mcp.json is missing 'encore-local' server configuration."
    
    server_config = content["mcpServers"]["encore-local"]
    assert "command" in server_config, "'command' is missing in 'encore-local' server configuration."
    assert server_config["command"] == "encore", f"Expected 'command' to be 'encore', got '{server_config['command']}'"
    
    assert "args" in server_config, "'args' is missing in 'encore-local' server configuration."
    expected_args = ["mcp", "run", "--app=my-test-app"]
    assert server_config["args"] == expected_args, f"Expected 'args' to be {expected_args}, got '{server_config['args']}'"
