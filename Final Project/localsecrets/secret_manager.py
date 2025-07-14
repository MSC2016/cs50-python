from localsecrets.crypto import encrypt, decrypt
from localsecrets.fileio import FileIO
from localsecrets.logger import log
from datetime import datetime
from  localsecrets.config import DEFAULT_DB_FILE_DATA, DEFAULT_VAULT_DATA
import json, copy, uuid

class SecretManager:
    def __init__(self, file_path, password=''):
        self._fileio = FileIO(file_path)
        self._file_path = file_path
        self._data = {}
        self._current_vault = "default"
        self._password = password

        if self._fileio.file_exists():
            log(f'{self._file_path} exists, loading...')
            self.load_file()
        else:
            log(f'{self._file_path} does not exist, creating a new file...')
            self._data = self._create_new_file_data()
            self.save_file()

    def load_file(self):
        data = self._fileio.read_data()
        if not data:
            return False
        try:
            if not self._password == '':
                data = decrypt(data, self._password)
            self._data = json.loads(data.decode())
            return True
        except Exception:
            log('Could not read/decrypt data, make sure to enter the right password.', 'error')
            raise IOError('Could not read/decrypt data, make sure to enter the right password.')

    def save_file(self):
        try:
            encoded = json.dumps(self._data, indent=4).encode()
            if self._password == '':
                return self._fileio.save_data(encoded)
            else:
                data = encrypt(encoded, self._password)
                return self._fileio.save_data(data)
        except Exception as e:
            log(f"Save failed: {e}", "error")
            return False

    def set_password(self, password=''):
        if self.load_file():
            self._password = password
        else:
            log('Can not change password, unless file was open with the right password', 'error')
            raise IOError('Can not change password, unless file was open with the right password')
            
    def create_vault(self, vault_name:str):
        if not self.vault_exists(vault_name) and len(vault_name) > 0:
            self._data['vaults'][vault_name] = copy.deepcopy(DEFAULT_VAULT_DATA['this_name'])
            return True
        return False
    
    def list_vaults(self):
        result = []
        for vault in self._data['vaults']:
            result.append(vault)
        return result
    
    def set_default_vault(self, vault_name : str):
        if vault_name in self._data['vaults']:
            self._current_vault = vault_name
            return True
        log(f'Could not set default vault to {vault_name}','error')
        return False
    
    def rename_vault(self, old_name: str, new_name: str) -> bool:
        if old_name == new_name:
            log('Old and new vault names are the same.', 'warning')
            return False
        
        if not self.vault_exists(old_name):
            log(f"Vault '{old_name}' does not exist.", 'error')
            return False

        if self.vault_exists(new_name):
            log(f"Vault '{new_name}' already exists.", 'error')
            return False

        self._data['vaults'][new_name] = self._data['vaults'].pop(old_name)

        if self._current_vault == old_name:
            self._current_vault = new_name

        log(f"Vault '{old_name}' renamed to '{new_name}'.", 'info')
        return True

    def vault_exists(self, vault_name: str):
        return vault_name in self._data['vaults']

    def add_secret(self, secret_name: str = '', secret_data: str = '', vault_name: str = ''):
        if vault_name == '':
            vault_name = self._current_vault

        if len(vault_name) > 0 and len(secret_name) > 0 and len(secret_data) > 0:
            if vault_name in self._data['vaults']:
                vault = self._data['vaults'][vault_name]
                if secret_name not in vault['secrets']:
                    secret_entry = {
                        'secret': secret_data,
                        'meta-data': {
                            'created': datetime.now().isoformat(),
                            'accessed': datetime.now().isoformat(),
                            'moddified': datetime.now().isoformat()
                        },
                        'user-data': {}
                    }
                    vault['secrets'][secret_name] = secret_entry
                    return True
            log(f'Could not add {secret_name} to {vault_name} vault.', 'error')
            return False
        
    def rename_secret(self, old_name: str, new_name: str, vault_name: str = '') -> bool:
        if vault_name == '':
            vault_name = self._current_vault

        if not self.vault_exists(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return False

        secrets = self._data['vaults'][vault_name]['secrets']

        if old_name not in secrets:
            log(f"Secret '{old_name}' does not exist in vault '{vault_name}'.", 'error')
            return False

        if new_name in secrets:
            log(f"Secret '{new_name}' already exists in vault '{vault_name}'.", 'error')
            return False

        secrets[new_name] = secrets.pop(old_name)
        secrets[new_name]['meta-data']['moddified'] = datetime.now().isoformat()

        log(f"Secret '{old_name}' renamed to '{new_name}' in vault '{vault_name}'.", 'info')
        return True


    def delete_secret(self, secret_name: str, vault_name: str = '', permanent: bool = False) -> bool:
        if vault_name == '':
            vault_name = self._current_vault

        if not self.vault_exists(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return False

        secrets = self._data['vaults'][vault_name]['secrets']

        if secret_name not in secrets:
            log(f"Secret '{secret_name}' does not exist in vault '{vault_name}'.", 'error')
            return False

        soft_delete_enabled = self._data.get('config', {}).get('soft_delete_secrets', False)

        if permanent or not soft_delete_enabled:
            del secrets[secret_name]
            log(f"Secret '{secret_name}' permanently deleted from vault '{vault_name}'.", 'info')
        else:
            secret_data = secrets.pop(secret_name)
            deletion_uuid = str(uuid.uuid4())
            deletion_entry = {
                'deleted': datetime.now().isoformat(),
                'from': vault_name,
                'data': secret_data
            }
            self._data['deleted_secrets'][deletion_uuid] = deletion_entry
            log(f"Secret '{secret_name}' moved to deleted_secrets from vault '{vault_name}'.", 'info')

        return True

    def _create_new_file_data(self):
        local__default_db_file_data = copy.deepcopy(DEFAULT_DB_FILE_DATA)
        local__default_db_file_data['vaults']['default'] = copy.deepcopy(DEFAULT_VAULT_DATA['this_name'])
        return local__default_db_file_data