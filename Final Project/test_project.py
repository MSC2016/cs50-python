import os
import pytest
from project import *

TEST_DB_PATH = "test_secrets.db"


@pytest.fixture
def manager():
    # Ensure a clean test DB
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    sm = create_manager(TEST_DB_PATH)
    # Add default vaults
    sm.add_vault("work")
    sm.add_vault("personal")
    yield sm
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_create_manager(manager):
    assert manager is not None
    assert isinstance(manager._vaults, dict)
    assert manager._file_path == TEST_DB_PATH


def test_add_secret(manager):
    add_secret(manager, "work", "test-item", "top-secret", {"meta": "data"})
    assert "test-item" in manager._vaults["work"]
    assert manager._vaults["work"]["test-item"]["secret"] == "top-secret"
    assert manager.item("test-item").get_user_data("meta") == "data"


def test_move_secret(manager):
    add_secret(manager, "personal", "email", "pass123")
    moved = move_secret(manager, "personal", "work", "email")
    assert moved is True
    assert "email" in manager._vaults["work"]
    assert "email" not in manager._vaults["personal"]


def test_search_secrets(manager):
    add_secret(manager, "work", "github", "gh-token")
    add_secret(manager, "work", "gitlab", "gl-token")
    results = search_secrets(manager, "git")
    names = [item["item_name"] for item in results]
    assert "github" in names
    assert "gitlab" in names


def test_search_secrets_case_insensitive(manager):
    add_secret(manager, "personal", "DropBox", "token")
    results = search_secrets(manager, "drop")
    names = [item["item_name"].lower() for item in results]
    assert "dropbox" in names



def test_delete_and_restore(manager):
    add_secret(manager, "personal", "netflix", "netflix-pass")
    restored = delete_and_restore(manager, "netflix", "personal")
    assert restored is True
    assert "netflix" in manager._vaults["personal"]


def test_add_item_direct(manager):
    manager["work"].add_item("project_one", "api-key")
    assert "project_one" in manager._vaults["work"]
    assert manager._vaults["work"]["project_one"]["secret"] == "api-key"
