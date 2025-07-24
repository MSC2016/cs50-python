import pytest
from localsecrets.vault import Vault

@pytest.fixture
def sample_vault_data():
    return {
        'item1': {'secret': 's1'},
        'item2': {'secret': 's2'},
    }

def test_init_and_get_item(sample_vault_data):
    vault = Vault(sample_vault_data)
    item = vault.get_item('item1')
    assert item['secret'] == 's1'
    with pytest.raises(KeyError):
        vault.get_item('nonexistent')

def test_add_item_and_rename(sample_vault_data):
    vault = Vault(sample_vault_data)
    assert vault.add_item('item3', 'secret3') is True
    assert 'item3' in vault
    assert vault.rename_item('item3', 'item4') is True
    assert 'item3' not in vault
    assert 'item4' in vault

def test_get_secret(sample_vault_data):
    vault = Vault(sample_vault_data)
    assert vault.get_secret('item1') == 's1'
    
    # Expect KeyError when item is missing
    with pytest.raises(KeyError):
        vault.get_secret('missing')

def test_rename_item_errors(sample_vault_data):
    vault = Vault(sample_vault_data)
    with pytest.raises(KeyError):
        vault.rename_item('nonexistent', 'new_name')
    vault.add_item('existing', 'secret')
    with pytest.raises(KeyError):
        vault.rename_item('item1', 'existing')  # already exists

def test_add_item_empty_secret(sample_vault_data):
    vault = Vault(sample_vault_data)
    vault.add_item('empty_secret', '')
    assert vault.get_secret('empty_secret') == ''
