from localsecrets.itemwrapper import ItemWrapper

class VaultWrapper:
    def __init__(self, name: str, data: dict, vault_manager):
        self._name = name
        self._data = data
        self._vault_manager = vault_manager

    def __getitem__(self, item_name: str) -> ItemWrapper:
        secrets = self._data.get("secrets", {})
        if item_name not in secrets:
            raise KeyError(f"Item '{item_name}' not found in vault '{self._name}'")
        return ItemWrapper(secrets[item_name])

    def list_items(self) -> list:
        return list(self._data.get('secrets', {}).keys())

    def set_default(self) -> bool:
        return self._vault_manager.set_default(self._name)

    def delete(self, permanent=False) -> bool:
        return self._vault_manager.delete(self._name, permanent)

    def delete_item(self, item_name: str, permanent: bool = False) -> bool:
        return self._vault_manager.delete_item(self._name, item_name, permanent)

    def rename(self, new_name: str) -> bool:
        return self._vault_manager.rename(self._name, new_name)

    def list_items(self) -> list:
        return self._vault_manager.list_items(self._name)