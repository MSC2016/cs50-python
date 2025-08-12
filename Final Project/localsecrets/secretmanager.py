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
        '''
        Initializes the SecretManager.

        Parameters:
        file_path (str): Path to the secrets database file. If the file exists, it will be loaded; 
                         otherwise, a new file will be created.
        encription_key (str or None, optional): Encryption key used to encrypt/decrypt data.
                    If set to a string, encryption is enabled.
                    If set to None (keyword), encryption is disabled.
        '''
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
        loaded = self._load_db_file()
        if loaded and self._version != version:
            raise ValueError(f'incorrect DB file version, expected v{version}, file is v{self._version}')
        
    def __getitem__(self, key):
        if key not in self._vaults:
            raise KeyError(f'Vault "{key}" not found.')
        return Vault(self._vaults[key])


    @property
    def item(self):
        return ItemController(self)

    def _load_db_file(self):
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
            raise IOError(f'Failed to load data: {e}')

    def export_no_encryption(self, file_path):
        '''
        Exports the current secret database to a file without encryption.

        Temporarily disables encryption and saves the database to the specified path
        in plain text format. After export, restores the original encryption settings 
        and file path.

        Returns:
            bool: True if the export was successful, False otherwise.
        '''
        backup_enc_key = self._encription_key
        backup_file_path = self._file_path
        self._encription_key = None
        self._file_path = file_path
        self._fileIO = FileIO(file_path)
        result = False
        try:
            if self.save_db_file():
                result = True
        except Exception as e:
            log('e', 'warn')
        finally:
            self._encription_key = backup_enc_key
            self._file_path = backup_file_path
            self._fileIO = FileIO(self._file_path)
        return result

    def set_encryption_key(self, encryption_key):
        '''
        Sets the encryption key for the secret manager.

        If a string is provided, encryption will be enabled using that key.
        If None or any non-string value is provided, encryption is disabled.
        '''
        if isinstance(encryption_key, str):
            self._encription_key = encryption_key
            log(f'Encryption key set to {'*' * len(self._encription_key)}', 'info')
        else:
            self._encription_key = None
            log(f'Encryption disabled.', 'info')

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
        '''
        Save changes to secret manager instance.

        Returns:
            bool: True if successfull.
        '''
        if not self._validate_data():
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
        result = self._fileIO.save_data(data)
        return result
    
    def _validate_data(self):
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
        '''
        Add a vault to the secret manager.

        Returns:
            bool: True if successfull.
        '''
        if self._vaults is None:
            self._vaults = {}

        if vault_name in self._vaults:
            raise KeyError(f'Vault "{vault_name}" already exists.')

        # Add vault as an empty dict (no items yet)
        self._vaults[vault_name] = {}

        log(f'Vault "{vault_name}" created.', 'info')
        return True

    def rename_vault(self, vault_name: str, new_name: str) -> bool:
        '''
        Rename a vault.

        Returns:
            bool: True if successfull.
        '''
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
        '''
        Adds an Item to a vault.

        Returns:
            bool: True if successfull.
        '''
        vault_name = vault_name if vault_name else self._current_vault
        if vault_name not in self._vaults:
            raise KeyError(f'Vault "{vault_name}" does not exist.')
        vault = self[vault_name]
        return vault.add_item(item_name, item_secret)
    
    def get_item(self, item_name: str, vault_name: str = '', secret_only: bool = False):
        '''
        Retrieves an item from a vault.

        Returns:
            Any: The item data or secret value, depending on the `secret_only` flag.

        '''
        vault_name = vault_name if vault_name else self._current_vault
        if vault_name not in self._vaults:
            raise KeyError(f'Vault "{vault_name}" not found.')
        vault = self[vault_name]
        return vault.get_item(item_name, secret_only)

    def get_secret(self, item_name: str, vault_name: str = '') -> str:
        '''
        Retrieves a secret item from a vault.

        Parameters:
            item (str): The name of the item to retrieve.
            vault_name (str): Name of the vault. Defaults to the current vault if not specified.

        Returns:
            str: The secret value.
        '''
        return self.get_item(item_name, vault_name, True)

    def delete_item(self, vault_name: str, item_name: str, permanent: bool = False) -> bool:
        '''
        Delete an item from a vault, if soft delete is enabled, and not explicitly permanent,
        move item to deleted_items instead of erasing it.

        Returns:
            bool: True if successfull.
        '''
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
    
    def move_item(self, item_name: str, origin_vault: str, dst_vault: str) -> bool:
        '''
        Moves an item from one vault to another.

        Returns:
            bool: True if the move was successful, False otherwise.
        '''
        if origin_vault not in self._vaults:
            raise KeyError(f'Vault "{origin_vault}" not found.')
        if dst_vault not in self._vaults:
            raise KeyError(f'Vault "{dst_vault}" not found.')
        if item_name not in self._vaults[origin_vault]:
            raise KeyError(f'Item "{item_name}" not found in vault "{origin_vault}".')

        item = self._vaults[origin_vault].pop(item_name)
        self._vaults[dst_vault][item_name] = item
        return item_name not in self._vaults[origin_vault] and item_name in self._vaults[dst_vault]
        
    def delete_vault(self, vault_name: str, permanent: bool = False) -> bool:
        '''
        Delete a vault. If vault has items and soft delete is enabled,
        move items to deleted_items unless permanent is True.

        Returns:
            bool: True if successfull.
        '''
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
        '''
        Sets the current vault for item operations.

        Returns:
            bool: True if successful.
        '''
        if vault not in self._vaults:
            raise KeyError(f'Vault "{vault}" not found.')
        self._current_vault = vault
        return True
    
    def list_vaults(self) -> list[str]:
        '''Returns a list of all existing vault names.'''
        return list(self._vaults.keys())
