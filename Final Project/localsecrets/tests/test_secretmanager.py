import os
import pytest
from localsecrets.secretmanager import SecretManager

@pytest.fixture
def test_db_path(tmp_path):
    return tmp_path / "test_secrets_db.json"

def test_delete_item_permanent(test_db_path):
    sm = SecretManager(str(test_db_path), '')
    sm.add_vault('vault')
    sm.add_item('item1', 'secret1', 'vault')
    assert sm.delete_item('vault', 'item1', permanent=True) is True
    assert 'item1' not in sm._vaults['vault']

def test_delete_item_soft(test_db_path):
    sm = SecretManager(str(test_db_path), '')
    sm.add_vault('vault')
    sm.add_item('item2', 'secret2', 'vault')
    assert sm.delete_item('vault', 'item2', permanent=False) is True
    assert 'item2' not in sm._vaults['vault']
    assert any(i["name"] == "item2" for i in sm._deleted_items.values())

def test_delete_vault(test_db_path):
    sm = SecretManager(str(test_db_path), '')
    sm.add_vault('vault2')
    assert sm.delete_vault('vault2', permanent=True) is True
    assert 'vault2' not in sm._vaults

def test_rename_vault(test_db_path):
    sm = SecretManager(str(test_db_path), '')
    sm.add_vault('oldvault')
    assert sm.rename_vault('oldvault', 'newvault') is True
    assert 'newvault' in sm._vaults

def test_list_vaults(test_db_path):
    sm = SecretManager(str(test_db_path), '')
    sm.add_vault('vaultA')
    vaults = sm.list_vaults()
    assert 'vaultA' in vaults

def test_restore_soft_deleted_item(test_db_path):
    sm = SecretManager(str(test_db_path), '')
    sm.add_vault('vault')
    sm.add_item('item1', 'secret1', 'vault')
    sm.delete_item('vault', 'item1', permanent=False)

    deleted_items = sm.item.list_deleted()
    assert len(deleted_items) == 1

    uuid = deleted_items[0]['uuid']  # get the UUID string properly

    assert sm.item.restore_deleted(uuid,'vault') is True
    # After restoring, the item should be back in the vault:
    assert 'item1' in sm._vaults['vault']
