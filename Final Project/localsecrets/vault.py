from localsecrets.item import Item

class Vault:
    def __init__(self, vault_data: dict):
        self._vault = vault_data

    def __getitem__(self, item_name):
        return Item(self._vault[item_name])

    def __contains__(self, item_name):
        return item_name in self._vault

    def add_item(self, item_name: str, secret: str) -> bool:
        if item_name in self._vault:
            raise KeyError(f'Item "{item_name}" already exists in vault.')

        self._vault[item_name] = ({
            'secret': secret
        })
        return True

    def get_item(self, item: str, secret_only: bool = False):
        if item not in self._vault:
            raise KeyError(f'Item "{item}" not found in vault.')
        return self._vault[item] if not secret_only else self._vault[item]['secret']
    
    def rename_item(self, old_name: str, new_name: str) -> bool:
        """Rename an item in the vault."""
        if old_name not in self._vault:
            raise KeyError(f'Item "{old_name}" not found in vault.')
        if new_name in self._vault:
            raise KeyError(f'Item "{new_name}" already exists in vault.')

        self._vault[new_name] = self._vault.pop(old_name)
        return True

    def get_secret(self, item: str) -> str:
        return self.get_item(item, secret_only=True)

