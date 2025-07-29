from localsecrets.logger import log

class Item:
    def __init__(self, item_data: dict):
        if not isinstance(item_data, dict):
            raise TypeError(f"Expected dict for item_data, got {type(item_data)}")
        self._data = item_data

    def to_dict(self):
        return self._data

    def __str__(self):
        return self.secret

    def __repr__(self):
        return self.secret

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    @property
    def secret(self):
        '''
        Returns the secret string of the item.

        Returns:
            str: The secret value, or empty string if not set.
        '''
        return self._data.get('secret', '')

    def set_user_data(self, key: str, value: str) -> bool:
        '''
        Adds or updates a user-defined data key-value pair.

        Returns:
            bool: True if the operation was successful.
        '''
        if 'user-data' not in self._data:
            self._data['user-data'] = {}
        self._data['user-data'][key] = value
        return True

    def get_user_data(self, key, default=None):
        '''
        Retrieves the value for a user-defined data key.

        Returns:
            The value associated with the key, or the default if not found.
        '''
        return self._data.get('user-data', {}).get(key, default)

    def list_user_data_keys(self) -> list[str]:
        '''
        Returns a list of keys in the user-defined data.

        Returns:
            list[str]: List of user-data keys.
        '''
        return list(self._data.get('user-data', {}).keys())

    def delete_user_data_key(self, key: str) -> bool:
        '''
        Deletes a specific key from user-defined data.

        Returns:
            bool: True if the key was found and deleted, False otherwise.
        '''
        user_data = self._data.get('user-data')
        if user_data and key in user_data:
            del user_data[key]
            return True
        return False
    
    def rename_user_data_key(self, old_key: str, new_key: str) -> bool:
        '''
        Renames a user-data key in this item.

        Returns:
            bool: True if the key was renamed successfully; False if old_key doesn't exist or new_key already exists.
        '''
        user_data = self._data.get('user-data', {})
        if old_key not in user_data:
            return False
        if new_key in user_data:
            return False
        user_data[new_key] = user_data.pop(old_key)
        return True

    def purge_user_data(self) -> bool:
        '''
        Removes all user-defined data from this item.

        Returns:
            bool: True if user data existed and was removed, False otherwise.
        '''
        if 'user-data' in self._data:
            del self._data['user-data']
            return True
        return False