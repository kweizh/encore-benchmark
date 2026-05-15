import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
MIGRATIONS_DIR = os.path.join(PROJECT_DIR, "todo", "migrations")

def test_migration_files_renamed_correctly():
    """Priority 3: Check that the migration files have been renamed correctly."""
    # Check that the old incorrectly named files are gone
    assert not os.path.exists(os.path.join(MIGRATIONS_DIR, "1_init.sql")), \
        "Expected 1_init.sql to be renamed, but it still exists."
    assert not os.path.exists(os.path.join(MIGRATIONS_DIR, "3_seed.up.sql")), \
        "Expected 3_seed.up.sql to be renamed, but it still exists."

    # Check that the new correctly named files exist
    assert os.path.exists(os.path.join(MIGRATIONS_DIR, "1_init.up.sql")), \
        "Expected 1_init.up.sql to exist."
    assert os.path.exists(os.path.join(MIGRATIONS_DIR, "2_seed.up.sql")), \
        "Expected 2_seed.up.sql to exist."

def test_encore_build_succeeds():
    """Priority 1: Use Encore CLI to verify that the application builds successfully without migration errors."""
    result = subprocess.run(
        ["encore", "build"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, \
        f"'encore build' failed: {result.stderr}\n{result.stdout}"
