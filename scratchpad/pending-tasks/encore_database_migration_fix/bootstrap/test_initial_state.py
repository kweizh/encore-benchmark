import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"
MIGRATIONS_DIR = os.path.join(PROJECT_DIR, "todo", "migrations")

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_migrations_dir_exists():
    assert os.path.isdir(MIGRATIONS_DIR), f"Migrations directory {MIGRATIONS_DIR} does not exist."

def test_initial_migration_files_exist():
    init_sql_path = os.path.join(MIGRATIONS_DIR, "1_init.sql")
    seed_sql_path = os.path.join(MIGRATIONS_DIR, "3_seed.up.sql")
    
    assert os.path.isfile(init_sql_path), f"Expected migration file {init_sql_path} does not exist."
    assert os.path.isfile(seed_sql_path), f"Expected migration file {seed_sql_path} does not exist."
