from localsecrets.vault_wrapper import VaultWrapper
from localsecrets.logger import log

class VaultManager:
    def __init__(self, data: dict, get_current_vault: callable, set_current_vault: callable):
        self._data = data
        self._get_current_vault = get_current_vault
        self._set_current_vault = set_current_vault

    def __getitem__(self, vault_name: str) -> VaultWrapper:
        vault_data = self._data['vaults'].get(vault_name)
        if vault_data is None:
            raise KeyError(f"Vault '{vault_name}' does not exist.")
        return VaultWrapper(vault_name, vault_data, self)
    
    def __contains__(self, vault_name: str) -> bool:
        return vault_name in self._data['vaults']

    def get(self, vault_name: str):
        vault_data = self._data['vaults'].get(vault_name)
        if vault_data is None:
            return None
        return VaultWrapper(vault_name, vault_data, self)

    def delete(self, vault_name: str, permanent: bool = False) -> bool:
        if vault_name not in self._data['vaults']:
            log(f"Vault '{vault_name}' does not exist.", 'warn')
            return False

        if vault_name == self._get_current_vault():
            log(f"Cannot delete the currently active vault '{vault_name}'.", 'warn')
            return False

        if vault_name == 'default':
            log("Cannot delete the 'default' vault.", 'error')
            return False

        secrets = list(self._data['vaults'][vault_name]['secrets'].keys())
        
        for secret_name in secrets:
            self.delete_item(vault_name, secret_name, permanent)

        del self._data['vaults'][vault_name]
        log(f"Vault '{vault_name}' has been {'permanently ' if permanent else ''}deleted.", 'debug')
        return True

    def set_default(self, name: str) -> bool:
        if name in self._data['vaults']:
            self._set_current_vault(name)
            return True
        log(f'Could not set default vault to {name}', 'error')
        return False

    def add(self, name: str) -> bool:
        if len(name) == 0:
            raise ValueError('Vault name can not be an empty string')
        if name in self._data['vaults']:
            log(f'Could not create vault "{name}", vault already exists.', 'warn')
            return False
        self._data['vaults'][name] = {'secrets': {}, 'metadata': {}}
        return True

    def list(self) -> list:
        return list(self._data['vaults'].keys())
    
    def delete_item(self, vault_name: str, item_name: str, permanent: bool = False) -> bool:
        if vault_name not in self._data['vaults']:
            log(f'Vault {vault_name} does not exist.', 'warn')
            return False
        if item_name not in self._data['vaults'][vault_name]['secrets']:
            log(f'Item {item_name} does not exist in {vault_name}.', 'warn')
            return False

        del self._data['vaults'][vault_name]['secrets'][item_name]
        log(f'Item {item_name} deleted from vault {vault_name}.', 'debug')
        return True
    
    def rename(self, old_name: str, new_name: str) -> bool:
        if old_name == new_name:
            log('Old and new vault names are the same.', 'warn')
            return False

        if old_name == 'default':
            log('You cannot rename the default vault.', 'error')
            return False

        if old_name not in self._data['vaults']:
            log(f"Vault '{old_name}' does not exist.", 'warn')
            return False

        if new_name in self._data['vaults']:
            log(f"Vault '{new_name}' already exists.", 'warn')
            return False

        self._data['vaults'][new_name] = self._data['vaults'].pop(old_name)

        # update current vault if needed
        if self._get_current_vault() == old_name:
            self._set_current_vault(new_name)

        log(f"Vault '{old_name}' renamed to '{new_name}'.", 'debug')
        return True

    def has(self, vault_name: str) -> bool:
        return vault_name in self._data['vaults']
    
    def list_items(self, vault_name: str) -> list:
        if vault_name not in self._data['vaults']:
            log(f"Vault '{vault_name}' not found.", 'error')
            return []
        return list(self._data['vaults'][vault_name]['secrets'].keys())