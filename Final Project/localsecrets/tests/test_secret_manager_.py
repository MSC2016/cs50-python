import os
import pytest
from localsecrets.secretmanager import SecretManager

# Get the folder path where this test file lives
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DB_FILE = os.path.join(TEST_DIR, 'test_secrets_db.json')

# Delete DB file if exists before tests run
if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

DUMMY_KEY = None

def test_init_creates_default_vault():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    assert 'default' in sm._vaults
    assert sm._vaults['default'] != {}
    assert os.path.exists(TEST_DB_FILE)

def test_add_vault_success():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    assert sm.add_vault('personal') is True
    assert 'personal' in sm._vaults
    sm.save_db_file()

def test_check_vault_persists():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    assert 'personal' in sm._vaults

def test_create_vault_no_persistance():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    assert sm.add_vault('should_not_persist') is True
    assert sm._auto_save is False
    # exit without saving

def test_ensure_changes_were_not_saved():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    assert 'should_not_persist' not in sm._vaults

def test_add_vault_duplicate():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    sm.add_vault('work')
    assert sm.add_vault('work') is False  # already exists

def test_add_item_success():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    sm.add_vault('myvault')
    added = sm.add_item('email', 'hunter2', 'myvault')
    sm.save_db_file()
    assert added is True
    assert 'email' in sm._vaults['myvault']
    assert sm._vaults['myvault']['email']['secret'] == 'hunter2'

def test_save_and_load_cycle():
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    sm.add_vault('vault1')
    sm.add_item('entry1', 'secret1', 'vault1')
    sm.save_db_file()
    id1 = id(sm)
    del(sm)
    sm = SecretManager(TEST_DB_FILE, DUMMY_KEY)
    id2 = id(sm)
    assert 'vault1' in sm._vaults
    assert 'entry1' in sm._vaults['vault1']
    assert sm._vaults['vault1']['entry1']['secret'] == 'secret1'
    assert id1 != id2

