from localsecrets.itemcontroller import ItemController
from localsecrets.crypto import encrypt, decrypt
from localsecrets.config import version
from localsecrets.fileio import FileIO
from localsecrets.vault import Vault
from localsecrets.logger import log
from localsecrets.config import now

import copy, uuid
import json

class SecretManager:
    def __init__(self, file_path, encription_key = ''):
        self._file_path = file_path
        self._encription_key = encription_key
        self._fileIO = FileIO(file_path)
        self._raw_data = None
        self._version = None
        self._use_soft_delete = None
        self._auto_save = None
        self._vaults = None
        self._deleted_items = None
        self._current_vault = 'default'
        loaded = self.load_db_file()
        if loaded and self._version != version:
            raise ValueError(f'incorrect DB file version, expected v{version}, file is v{self._version}')
        
    def __getitem__(self, key):
        if key not in self._vaults:
            raise KeyError(f'Vault "{key}" not found.')
        return Vault(self._vaults[key])


    @property
    def item(self):
        return ItemController(self)

    
    def load_db_file(self):
        if not self._fileIO.file_exists():
            log(f'File {self._file_path} doesn’t exist. Initializing new database.', 'warn')
            self._version = 1.0
            self._use_soft_delete = True
            self._auto_save = False
            self._vaults = {}
            self._deleted_items = {}
            self.add_vault('default')
            self.save_db_file()
            return True
        else:
            self._raw_data = self._fileIO.read_data()

        try:
            decrypted = decrypt(self._raw_data, self._encription_key) if self._encription_key is not None else (self._raw_data, None)
            parsed = json.loads(decrypted[0] if isinstance(decrypted, tuple) else decrypted)
            self._load_data(parsed)
            return True
        except Exception as e:
            log(f'Failed to load data: {e}', 'error')
            return False


    def _load_data(self, data):
        self._version = data.get('version')
        self._use_soft_delete = data.get('config', {}).get('soft_delete_items', True)
        self._auto_save = data.get('config', {}).get('auto_save', False)

        self._vaults = data.get('vaults', {})
        if not isinstance(self._vaults, dict):
            log('Invalid or missing vaults. Initializing empty vaults.', 'warn')
            self._vaults = {}

        self._deleted_items = data.get('deleted_items', {})
        if not isinstance(self._deleted_items, dict):
            log('Invalid or missing deleted_items. Initializing empty.', 'warn')
            self._deleted_items = {}


    def save_db_file(self):
        if not self.data_is_valid():
            raise ValueError('Invalid data')
        json_data = json.dumps({
            'version': version,
            'config': {'soft_delete_items': self._use_soft_delete,
                       'auto_save': self._auto_save,
                       },
            'vaults': self._vaults,
            'deleted_items':self._deleted_items,
            }, indent=4).encode('utf-8')
        data = encrypt(json_data, self._encription_key) if self._encription_key is not None else json_data
        return self._fileIO.save_data(data)
    
    def data_is_valid(self):
        problem = []
        if not isinstance(self._vaults, dict):
            problem.append('self._vaults')
        if not isinstance(self._deleted_items, dict):
            problem.append('self._deleted_items')
        if 'default' not in self._vaults:
            problem.append('"default" vault does not exist')
        if problem:
            problem_text = f'Internal state is corrupted or incomplete ({", ".join(problem)})'
            log(problem_text, 'error')
            return False
        return True

    def add_vault(self, vault_name: str) -> bool:
        if self._vaults is None:
            self._vaults = {}

        if vault_name in self._vaults:
            raise KeyError(f'Vault "{vault_name}" already exists.')

        # Add vault as an empty dict (no items yet)
        self._vaults[vault_name] = {}

        log(f'Vault "{vault_name}" created.', 'info')
        return True

    def rename_vault(self, vault_name: str, new_name: str) -> bool:
        if not isinstance(vault_name, str) or not isinstance(new_name, str):
            raise ValueError('vault_name and new_name must be strings.')
        
        if not vault_name or not new_name:
            raise ValueError('vault_name and new_name must not be empty.')
        
        if vault_name == new_name:
            raise ValueError('vault_name and new_name must be different.')
        
        if new_name in self._vaults:
            raise ValueError(f'A vault named "{new_name}" already exists.')
        
        if vault_name not in self._vaults:
            raise ValueError(f'Could not rename vault "{vault_name}": vault not found.')
        
        if vault_name == 'default':
            raise ValueError('Cannot rename the default vault.')

        if vault_name == self._current_vault:
            raise ValueError('Cannot rename the current vault')
        
        self._vaults[new_name] = self._vaults.pop(vault_name)        
        return True
            

    def add_item(self, item_name: str, item_secret: str, vault_name: str = '') -> bool:
        vault_name = vault_name if vault_name else self._current_vault
        if vault_name not in self._vaults:
            raise KeyError(f'Vault "{vault_name}" does not exist.')
        vault = self[vault_name]
        return vault.add_item(item_name, item_secret)
    
    def get_item(self, item: str, vault_name: str = '', secret_only: bool = False):
        vault_name = vault_name if vault_name else self._current_vault
        if vault_name not in self._vaults:
            raise KeyError(f'Vault "{vault_name}" not found.')
        vault = self[vault_name]
        return vault.get_item(item, secret_only)

    def get_secret(self, item: str, vault_name: str = '') -> str:
        return self.get_item(item, vault_name, True)

    def delete_item(self, vault_name: str, item_name: str, permanent: bool = False) -> bool:
        """
        Delete an item from a vault. If soft delete is enabled, and not explicitly permanent,
        move item to deleted_items instead of erasing it.
        """
        vault = self._vaults.get(vault_name)
        if not vault:
            raise KeyError(f'Vault "{vault_name}" not found.')

        item_data = vault[item_name]

        if not permanent and self._use_soft_delete:
            uid = str(uuid.uuid4())
            self._deleted_items[uid] = {
                'name': item_name,
                'vault': vault_name,
                'deleted' : now(),
                'data': copy.deepcopy(item_data)
            }
        del vault[item_name]
        return True
    
    def delete_vault(self, vault_name: str, permanent: bool = False) -> bool:
        """
        Delete a vault. If vault has items and soft delete is enabled,
        move items to deleted_items unless permanent is True.
        """
        if vault_name not in self._vaults:
            raise KeyError(f'Vault "{vault_name}" not found.')

        if vault_name == 'default':
            raise ValueError('Cannot delete the default vault.')

        if vault_name == self._current_vault:
            raise ValueError('Cannot delete the current vault.')

        vault = self._vaults[vault_name]
        item_names = [k for k in vault]

        for name in item_names:
            self.delete_item(vault_name, name, permanent=permanent)
        del self._vaults[vault_name]
        log(f'Vault "{vault_name}" deleted.', 'info')
        return True
    
    def set_current_vault(self, vault : str = '') -> bool:
        if vault not in self._vaults:
            raise KeyError(f'Vault "{vault}" not found.')
        self._current_vault = vault
        return True
    
    def list_vaults(self) -> list[str]:
        """Returns a list of all existing vault names."""
        return list(self._vaults.keys())
