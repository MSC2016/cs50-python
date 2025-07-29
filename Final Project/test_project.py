import os
import pytest
from project import (
    create_manager,
    add_secret,
    list_items_in_vault,
    move_item,
    delete_and_restore,
    search_items,
)

TEST_DB_PATH = "test_secrets.db"


@pytest.fixture
def manager():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    sm = create_manager(TEST_DB_PATH)
    yield sm
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_create_manager(manager):
    assert manager is not None
    assert isinstance(manager._vaults, dict)
    assert manager._file_path == TEST_DB_PATH


def test_add_secret(manager):
    result = add_secret(manager, "test-vault", "test-item", "top-secret")
    assert result is True
    assert "test-item" in manager._vaults["test-vault"]
    assert manager._vaults["test-vault"]["test-item"]["secret"] == "top-secret"


def test_list_items_in_vault(manager):
    add_secret(manager, "work", "email", "pass123")
    items = list_items_in_vault(manager, "work")
    assert items == ["email"]


def test_move_item(manager):
    add_secret(manager, "vaultA", "token", "abc123")
    moved = move_item(manager, "vaultA", "vaultB", "token")
    assert moved is True
    assert "token" in manager._vaults["vaultB"]
    assert "token" not in manager._vaults["vaultA"]


def test_delete_and_restore(manager):
    add_secret(manager, "main", "note", "sensitive-data")
    restored = delete_and_restore(manager, "main", "note", "restored")
    assert restored is True
    assert "note" in manager._vaults["restored"]
    assert "note" not in manager._vaults["main"]


def test_search_items(manager):
    add_secret(manager, "searchvault", "github", "gh-token")
    add_secret(manager, "searchvault", "gitlab", "gl-token")
    results = search_items(manager, "git")
    names = [item["item_name"] for item in results]
    assert "github" in names
    assert "gitlab" in names


def test_search_items_case_insensitive(manager):
    add_secret(manager, "mix", "DropBox", "token")
    results = search_items(manager, "drop")
    assert any("dropbox" in r["item_name"].lower() for r in results)
