import pytest
from localsecrets.secretmanager import SecretManager
from localsecrets.itemcontroller import ItemController

@pytest.fixture
def sm(tmp_path):
    db_file = tmp_path / "testdb.json"
    sm = SecretManager(str(db_file), '')
    return sm

@pytest.fixture
def ic(sm):
    return ItemController(sm)

def test_add_and_list_items(ic):
    assert ic.add('item1', 'secret1') is True
    assert 'item1' in ic.list_()

def test_add_duplicate_item(ic):
    ic.add('item1', 'secret1')
    with pytest.raises(KeyError):
        ic.add('item1', 'secret2')

def test_rename_item(ic):
    ic.add('item1', 'secret1')
    assert ic.rename('item1', 'item2') is True
    assert 'item2' in ic.list_()
    assert 'item1' not in ic.list_()

def test_delete_and_restore_item(ic):
    ic.add('item1', 'secret1')
    assert ic.delete('item1', permanent=False) is True
    assert 'item1' not in ic.list_()
    # Restore deleted item
    deleted = list(ic._manager._deleted_items.keys())
    assert len(deleted) == 1
    assert ic.restore_deleted_item(deleted[0]) is True
    assert 'item1' in ic.list_()

def test_set_get_user_data(ic):
    ic.add('item1', 'secret1')
    assert ic.set_user_data('item1', 'key', 'value') is True
    assert ic.get_user_data('item1', 'key') == 'value'

def test_delete_user_data_key(ic):
    ic.add('item1', 'secret1')
    ic.set_user_data('item1', 'key', 'value')
    assert ic.delete_user_data_key('item1', 'key') is True
    assert ic.delete_user_data_key('item1', 'key') is False

def test_rename_user_data_key(ic):
    ic.add('item1', 'secret1')
    ic.set_user_data('item1', 'oldkey', 'val')
    assert ic.rename_user_data_key('item1', 'oldkey', 'newkey') is True
    assert ic.get_user_data('item1', 'newkey') == 'val'
