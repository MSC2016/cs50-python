from __future__ import annotations
from localsecrets.item import Item
import json

class ItemController:
    def __init__(self, manager: 'SecretManager'):
        self._manager = manager

    def __call__(self, item_name: str):
        vault = self._manager._vaults[self._manager._current_vault]
        if item_name not in vault:
            raise KeyError(f'Item "{item_name}" not found in current vault.')
        return Item(vault[item_name])

    def add(self, item_name: str, secret: str) -> bool:
        '''
        Adds a new item with the given secret.

        Returns:
            bool: True if the item was successfully added.
        '''
        result = self._manager.add_item(item_name, secret)
        return result


    def rename(self, item_name: str, new_name: str) -> bool:
        '''
        Renames an item in the current vault.

        Returns:
            bool: True if the rename was successful.
        '''
        vault = self._manager._vaults[self._manager._current_vault]
        if item_name not in vault:
            raise KeyError(f'Item "{item_name}" not found.')
        if new_name in vault:
            raise KeyError(f'Item "{new_name}" already exists.')

        vault[new_name] = vault.pop(item_name)

        item = vault[new_name]
        return True


    def delete(self, item_name: str, permanent: bool = False) -> bool:
        '''
        Deletes an item from the current vault, If not permanent and soft delete is enabled,
        moves the item to deleted items, otherwise the item is permantly deleted.

        Returns:
            bool: True if the deletion was successful.
        '''
        return self._manager.delete_item(item_name, self._manager._current_vault, permanent=permanent)
    
    def rename(self, item_name: str, new_name: str) -> bool:
        '''
        Renames an item within the current vault.

        Returns:
            bool: True if the rename was successful.
        '''
        vault = self._manager._vaults[self._manager._current_vault]

        if item_name not in vault:
            raise KeyError(f'Item "{item_name}" not found.')
        if new_name in vault:
            raise KeyError(f'Item "{new_name}" already exists.')

        vault[new_name] = vault.pop(item_name)
        return True
    
    def list_(self) -> list[str]:
        '''
        Returns a sorted list of all item names in the current vault.
        '''
        vault = self._manager._vaults[self._manager._current_vault]
        return sorted(name for name in vault)

    def set_user_data(self, item_name: str, key: str, value) -> bool:
        '''
        Adds or updates user-defined data for a specific item.

        Returns:
            bool: True if the data was successfully set.
        '''
        vault = self._manager._vaults[self._manager._current_vault]

        if item_name not in vault:
            raise KeyError(f'Item "{item_name}" not found in current vault.')

        item_data = vault[item_name]
        item = Item(item_data)
        
        item.set_user_data(key, value)

        # Save if auto_save is enabled
        if self._manager._auto_save:
            self._manager.save_db_file()

        return True


    def get_user_data(self, item_name: str, key: str, default=None):
        '''
        Retrieves user-defined data for a specific item.

        Returns:
            Any: The value associated with the user-data key, or the default if missing.

        '''
        vault = self._manager._vaults[self._manager._current_vault]

        if item_name not in vault:
            raise KeyError(f'Item "{item_name}" not found in current vault.')

        item_data = vault[item_name]
        item = Item(item_data)

        # Accessing the data
        value = item.get_user_data(key, default)

        if self._manager._auto_save:
            self._manager.save_db_file()

        return value

    def list_user_data_keys(self, item_name: str) -> list[str]:
        '''
        Lists all user-data keys for the specified item.

        Returns:
            list[str]: A list of user-data key names.
        '''
        item = self(item_name)
        return item.list_user_data_keys()

    def delete_user_data_key(self, item_name: str, key: str) -> bool:
        '''
        Deletes a user-data key from the specified item.

        Returns:
            bool: True if the key was successfully deleted.
        '''
        item = self(item_name)
        result = item.delete_user_data_key(key)
        return result

    def rename_user_data_key(self, item_name: str, old_key: str, new_key: str) -> bool:
        '''
        Renames a user-data key within a specified item.

        Returns:
            bool: True if the key was successfully renamed.
        '''
        item = self(item_name)
        result = item.rename_user_data_key(old_key, new_key)
        return result

    def purge_user_data(self, item_name: str) -> bool:
        '''
        Removes all user-specific data from the specified item.
        Returns:
            bool: True if the user data was successfully purged.
        '''
        item = self(item_name)
        result = item.purge_user_data()
        return result

    def restore_deleted(self, uuid: str, dst_vault: str | None = None) -> bool:
        '''
        Restores a deleted item to a specified vault.

        Returns:
            bool: True if the item was successfully restored.

        '''
        if uuid not in self._manager._deleted_items:
            raise KeyError(f'Deleted item with UUID "{uuid}" not found.')

        dst_vault = dst_vault or self._manager._current_vault

        if dst_vault not in self._manager._vaults:
            raise KeyError(f'Vault "{dst_vault}" not found.')

        deleted_item = self._manager._deleted_items[uuid]

        # Use the original name from deleted item
        item_name = deleted_item.get('name')
        if not item_name:
            raise ValueError('Deleted item missing name.')

        vault = self._manager._vaults[dst_vault]
        if item_name in vault:
            raise KeyError(
                f'Cannot restore: item "{item_name}" already exists in vault "{dst_vault}". '
                'Rename or delete the existing item before restoring.')

        vault[item_name] = deleted_item['data']
        del self._manager._deleted_items[uuid]
        return True


    def pprint_deleted(self) -> None:
        '''
        Prints all deleted items in a readable, formatted JSON style.
        '''
        for item in self.list_deleted():
            print(json.dumps(item, indent=4))

    def list_deleted(self, vault: str | None = None, name_contains: str | None = None) -> list[dict]:
        '''
        Lists deleted items filtered by vault and/or name substring.

        Returns:
            list[dict]: List of deleted items matching the filters, each including its UUID and user data.
        '''
        items = []
        for uuid, item in self._manager._deleted_items.items():
            if vault and item.get("vault") != vault:
                continue
            if name_contains and name_contains.lower() not in item.get("name", "").lower():
                continue
            items.append({"uuid": uuid, **item})
        return items


    def purge_deleted_item(self, uuid: str) -> bool:
        '''
        Permanently removes a deleted item by its UUID.

        Returns:
            bool: True if the item was successfully purged.
        '''
        if uuid not in self._manager._deleted_items:
            raise KeyError(f'Deleted item with UUID "{uuid}" not found.')
        del self._manager._deleted_items[uuid]
        return True


    def purge_all_deleted_items(self) -> int:
        '''
        Permanently removes all deleted items from the manager.

        Returns:
            int: The number of deleted items purged.
        '''
        count = len(self._manager._deleted_items)
        self._manager._deleted_items.clear()
        return count
    
    def search(self, term: str, vault: str | None = None) -> list[dict]:
        '''
        Searches for items matching a term in specified vault or all vaults.

        Returns:
            list[dict]: List of matching items and deleted items with metadata:
                        Each dict contains keys: 'type', 'vault', 'item_name', 'uuid', 'data'.
        '''
        results = []
        term_lower = term.lower()

        def matches(item_name, item_data):
            if term_lower in item_name.lower():
                return True
            if 'secret' in item_data and term_lower in str(item_data['secret']).lower():
                return True
            user_data = item_data.get('user-data', {})
            for k, v in user_data.items():
                if term_lower in k.lower() or term_lower in str(v).lower():
                    return True
            return False

        vaults_to_search = [vault] if vault else self._manager._vaults.keys()
        for vault_name in vaults_to_search:
            vault_items = self._manager._vaults[vault_name]
            for item_name, item_data in vault_items.items():
                if matches(item_name, item_data):
                    results.append({
                        'type': 'vault',
                        'vault': vault_name,
                        'item_name': item_name,
                        'uuid': None,
                        'data': item_data
                    })

        for uuid, deleted in self._manager._deleted_items.items():
            deleted_vault = deleted.get('vault')
            if not deleted_vault:
                continue
            if vault and deleted_vault != vault:
                continue
            if matches(deleted.get('name', ''), deleted.get('data', {})):
                results.append({
                    'type': 'deleted',
                    'vault': deleted_vault,
                    'item_name': deleted.get('name'),
                    'uuid': uuid,
                    'data': deleted.get('data'),
                })

        return results
