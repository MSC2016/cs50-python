from localsecrets.logger import log

class Item:
    def __init__(self, item_data: dict):
        if not isinstance(item_data, dict):
            raise TypeError(f"Expected dict for item_data, got {type(item_data)}")
        self._data = item_data

    def to_dict(self):
        """Return the full underlying dict (for advanced use/debug)."""
        return self._data

    def __str__(self):
        return self.secret

    def __repr__(self):
        return f"Item(secret={repr(self.secret)})"

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    @property
    def secret(self):
        """Get the secret string."""
        return self._data.get('secret', '')

    def set_user_data(self, key: str, value: str) -> bool:
        """Add or update user-defined data inside the item."""
        if 'user-data' not in self._data:
            self._data['user-data'] = {}
        self._data['user-data'][key] = value
        return True

    def get_user_data(self, key, default=None):
        """Retrieve user-defined data."""
        return self._data.get('user-data', {}).get(key, default)

    def list_user_data_keys(self) -> list[str]:
        """Return a list of user-defined data keys."""
        return list(self._data.get('user-data', {}).keys())

    def delete_user_data_key(self, key: str) -> bool:
        """Delete a single key from user-defined data."""
        user_data = self._data.get('user-data')
        if user_data and key in user_data:
            del user_data[key]
            return True
        return False
    
    def rename_user_data_key(self, old_key: str, new_key: str) -> bool:
        user_data = self._data.get('user-data', {})
        if old_key not in user_data:
            return False
        if new_key in user_data:
            return False
        user_data[new_key] = user_data.pop(old_key)
        return True

    def purge_user_data(self) -> bool:
        """Completely remove all user-defined data."""
        if 'user-data' in self._data:
            del self._data['user-data']
            return True
        return False