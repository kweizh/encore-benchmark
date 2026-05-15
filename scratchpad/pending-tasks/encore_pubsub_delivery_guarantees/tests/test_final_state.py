import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/cart-app"

def test_encore_build_success():
    """Priority 1: Use Encore CLI to verify the project builds successfully."""
    result = subprocess.run(
        ["encore", "build"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, \
        f"'encore build' failed: {result.stderr}\n{result.stdout}"

def test_pubsub_delivery_guarantee():
    """Priority 3 fallback: Verify deliveryGuarantee in pubsub.ts"""
    pubsub_file = os.path.join(PROJECT_DIR, "cart", "pubsub.ts")
    assert os.path.isfile(pubsub_file), f"pubsub.ts not found at {pubsub_file}"
    
    with open(pubsub_file, "r") as f:
        content = f.read()
    
    assert "exactly-once" in content, "Expected 'exactly-once' deliveryGuarantee in pubsub.ts."

def test_pubsub_ordering_attribute():
    """Priority 3 fallback: Verify orderingAttribute in pubsub.ts"""
    pubsub_file = os.path.join(PROJECT_DIR, "cart", "pubsub.ts")
    
    with open(pubsub_file, "r") as f:
        content = f.read()
    
    assert "shoppingCartID" in content and "orderingAttribute" in content, \
        "Expected 'orderingAttribute' set to 'shoppingCartID' in pubsub.ts."

def test_api_publishes_event():
    """Priority 3 fallback: Verify api.ts publishes the event"""
    api_file = os.path.join(PROJECT_DIR, "cart", "api.ts")
    assert os.path.isfile(api_file), f"api.ts not found at {api_file}"
    
    with open(api_file, "r") as f:
        content = f.read()
    
    assert "cartEvents.publish" in content, "Expected 'cartEvents.publish' to be called in api.ts."
    assert "/cart/:id" in content or "/cart/:id" in content.replace(" ", ""), "Expected endpoint path '/cart/:id' in api.ts."
