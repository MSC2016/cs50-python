import pytest
from localsecrets.item import Item

@pytest.fixture
def sample_item_data():
    return {
        'secret': 'topsecret',
        'user-data': {
            'note': 'important'
        }
    }

def test_init_and_to_dict(sample_item_data):
    item = Item(sample_item_data)
    assert item.secret == 'topsecret'
    d = item.to_dict()
    assert d['secret'] == 'topsecret'
    assert d['user-data']['note'] == 'important'

def test_str_and_repr(sample_item_data):
    item = Item(sample_item_data)
    s = str(item)
    r = repr(item)
    assert 'topsecret' in s
    assert 'topsecret' in r

def test_get_set_item(sample_item_data):
    item = Item(sample_item_data)
    assert item['secret'] == 'topsecret'
    item['secret'] = 'newsecret'
    assert item['secret'] == 'newsecret'

def test_set_and_get_user_data(sample_item_data):
    item = Item(sample_item_data)
    assert item.set_user_data('priority', 'high') is True
    assert item.get_user_data('priority') == 'high'
    assert item.get_user_data('missing', 'default') == 'default'

def test_list_user_data_keys(sample_item_data):
    item = Item(sample_item_data)
    keys = item.list_user_data_keys()
    assert 'note' in keys

def test_delete_user_data_key(sample_item_data):
    item = Item(sample_item_data)
    assert item.delete_user_data_key('note') is True
    assert item.delete_user_data_key('note') is False

def test_rename_user_data_key(sample_item_data):
    item = Item(sample_item_data)
    item.set_user_data('oldkey', 'value')
    assert item.rename_user_data_key('oldkey', 'newkey') is True
    assert item.get_user_data('newkey') == 'value'
    assert item.rename_user_data_key('oldkey', 'newkey2') is False

def test_purge_user_data(sample_item_data):
    item = Item(sample_item_data)
    assert item.purge_user_data() is True
    assert item.list_user_data_keys() == []
