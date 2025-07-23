from localsecrets.fileio import FileIO
from localsecrets.config import version, now
from localsecrets.crypto import encrypt, decrypt
from localsecrets.logger import log
from localsecrets.utils import update_meta_data
from localsecrets.vault import Vault
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
        self._db_meta_data = None
        self._current_vault = 'default'
        loaded = self.load_db_file()
        if loaded and self._version != version:
            raise ValueError(f'incorrect DB file version, expected v{version}, file is v{self._version}')
        
    def __getitem__(self, key):
        if key not in self._vaults:
            raise KeyError(f"Vault '{key}' not found.")

        def update_db_meta():
            self._db_meta_data = update_meta_data(self._db_meta_data, accessed=True)

        def update_vault_meta():
            self._vaults[key]['meta-data'] = update_meta_data(
                self._vaults[key].get('meta-data', {}),
                accessed=True
            )

        return Vault(self._vaults[key], update_db_meta, update_vault_meta)

    
    def load_db_file(self):
        if not self._fileIO.file_exists():
            log(f'File {self._file_path} doesnt exist. Initializing new database.', 'warn')
            self._version = 1.0
            self._use_soft_delete = True
            self._auto_save = False
            self._vaults = {}
            self._deleted_items = {}
            self._db_meta_data = update_meta_data({}, created=True)
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
        self._vaults = data.get('vaults')
        if not isinstance(self._vaults, dict):
            log('Invalid or missing vaults. Initializing empty vaults.', 'warn')
            self._vaults = {}
        self._deleted_items = data.get('deleted_items')
        if not isinstance(self._deleted_items, dict):
            log('Invalid or missing deleted_items. Initializing empty.', 'warn')
            self._deleted_items = {}
        meta_data = data.get('meta-data')
        if not isinstance(meta_data, dict):
            log('Invalid meta-data. Resetting.', 'warn')
            meta_data = {}
        self._db_meta_data = update_meta_data(data.get('meta-data', {}), accessed=True)

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
            'meta-data':self._db_meta_data,
            }, indent=4).encode('utf-8')
        data = encrypt(json_data, self._encription_key) if self._encription_key is not None else json_data
        return self._fileIO.save_data(data)
    
    def data_is_valid(self):
        problem = []
        if not isinstance(self._vaults, dict):
            problem.append('self._vaults')
        if not isinstance(self._db_meta_data, dict):
            problem.append('self._db_meta_data')
        if not isinstance(self._deleted_items, dict):
            problem.append('self._deleted_items')
        if not self._vaults.get('default'):
            problem.append('"default" vault does not exist')
        if problem:
            problem_text = f"Internal state is corrupted or incomplete ({', '.join(problem)})"
            log(problem_text, "error")
            return False
        return True
    
    def add_vault(self, vault_name: str) -> bool:
        if vault_name in self._vaults:
            log(f"Vault '{vault_name}' already exists.", "warn")
            return False
        else:
            self._vaults[vault_name] = {}
            self._vaults[vault_name]['meta-data'] = update_meta_data({},created=True)
            self._db_meta_data = update_meta_data(self._db_meta_data, modified=True)
            log(f"Vault '{vault_name}' created.", "info")
            return True

    def add_item(self, item_name : str, item_secret : str, vault_name : str = '') -> bool:
        if not isinstance(vault_name, str):
            raise ValueError('Vault name must be a string.')
        vault = vault_name if len(vault_name) > 0 else self._current_vault
        if not vault in self._vaults:
            log(f'Vault {vault} does not exist', 'error')
            return False
        if item_name in self._vaults[vault]:
            log(f'Vault {vault} already has an item named {item_name}', 'error')
            return False
        self._vaults[vault][item_name] = {
            'secret' : item_secret,
            'metadata' : update_meta_data({},created=True)
        }
        return True
    
    def get_item(self, item: str, vault_name: str = '') -> str:
        vault = vault_name if len(vault_name) > 0 else self._current_vault
        if vault not in self._vaults:
            raise KeyError(f"Vault '{vault}' not found.")
        
        if item not in self._vaults[vault]:
            raise KeyError(f"Item '{item}' not found in vault '{vault}'.")

        self._vaults[vault][item]['metadata'] = update_meta_data( self._vaults[vault][item].get('metadata', {}), accessed=True)
        self._vaults[vault]['meta-data'] = update_meta_data(self._vaults[vault].get('meta-data', {}), accessed=True)
        self._db_meta_data = update_meta_data(self._db_meta_data, accessed=True)
        return self._vaults[vault][item]['secret']

    def set_current_vault(self, vault : str = '') -> bool:
        if vault not in self._vaults:
            raise KeyError(f"Vault '{vault}' not found.")
        self._current_vault = vault
        return True