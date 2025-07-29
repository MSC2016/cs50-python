from localsecrets.item import Item

class Vault:
    def __init__(self, vault_data: dict):
        self._vault = vault_data

    def __getitem__(self, item_name):
        return Item(self._vault[item_name])

    def __contains__(self, item_name):
        return item_name in self._vault

    def add_item(self, item_name: str, secret: str) -> bool:
        '''
        Adds a new item with a secret to the vault.

        Returns:
            bool: True if the item was added successfully.
        '''
        if item_name in self._vault:
            raise KeyError(f'Item "{item_name}" already exists in vault.')

        self._vault[item_name] = ({
            'secret': secret
        })
        return True

    def get_item(self, item: str, secret_only: bool = False):
        '''
        Retrieves an item or its secret from the vault.

        Returns:
            dict or str: The full item data if secret_only is False, else the secret string.
        '''
        if item not in self._vault:
            raise KeyError(f'Item "{item}" not found in vault.')
        return self._vault[item] if not secret_only else self._vault[item]['secret']
    
    def rename_item(self, old_name: str, new_name: str) -> bool:
        '''
        Renames an item within the vault.

        Returns:
            bool: True if the rename was successful.
        '''
        if old_name not in self._vault:
            raise KeyError(f'Item "{old_name}" not found in vault.')
        if new_name in self._vault:
            raise KeyError(f'Item "{new_name}" already exists in vault.')

        self._vault[new_name] = self._vault.pop(old_name)
        return True

    def get_secret(self, item_name: str) -> str:
        '''
        Retrieves the secret value of the specified item.

        Returns:
            str: The secret value of the item.
        '''
        return self.get_item(item_name, True)

