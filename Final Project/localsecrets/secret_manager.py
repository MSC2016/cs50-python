from localsecrets.crypto import encrypt, decrypt
from localsecrets.fileio import FileIO
from localsecrets.logger import log
from datetime import datetime
from  localsecrets.config import DEFAULT_DB_FILE_DATA, DEFAULT_VAULT_DATA
import json, copy, uuid

class SecretManager:
    def __init__(self, file_path: str, password =''):
        self._fileio = FileIO(file_path)
        self._file_path = file_path
        self._data = {}
        self._current_vault = "default"
        self._password = password
        self._treat_file_as_plain_text = password == None

        if self._fileio.file_exists():
            log(f'Found {self._file_path}')
            self.load_from_file()
        else:
            log(f'{self._file_path} does not exist, creating a new file...')
            self._data = self._create_new_file_data()
            self.save_to_file()

    def load_from_file(self) -> bool:
        data = self._fileio.read_data()
        log(f'Read {len(data)} bytes of data.')
        if not data:
            return False
        try:
            if self._treat_file_as_plain_text:
                self._data = json.loads(data.decode())
                return True
            else:
                data = decrypt(data, self._password)
                self._data = json.loads(data.decode())
                return True
        except Exception:
            log('Could not read/decrypt data, make sure to enter the right password.', 'error')
            raise IOError('Could not read/decrypt data, make sure to enter the right password.')

    def save_to_file(self) -> bool:
        try:
            encoded = json.dumps(self._data, indent=4).encode()
            log(f'Encoded {len(encoded)} bytes of data.')
            if self._treat_file_as_plain_text:
                log(f'Saving {self._file_path} as a plain text file','warn')
                return self._fileio.save_data(encoded)
            else:
                data = encrypt(encoded, self._password)
                log(f'Saving {self._file_path} with encryption','info')
                return self._fileio.save_data(data)
        except Exception as e:
            log(f"Save failed: {e}", "error")
            return False
        
    def set_file_password(self, password = '') -> bool:
        if password == None:
            log(f'Encryption disabled, {self._file_path} will be saved as a plain text file.','warn')
            self._password = ''
            self._treat_file_as_plain_text = True
            return True
        if isinstance(password,str):
            self._treat_file_as_plain_text = False
            self._password = password
            log('Encryption enabled.', 'info')
            return True
        raise ValueError('Password must be "None" to save as plain text, or a string of any length')

    def create_vault(self, vault_name:str) -> bool:
        if not self.vault_exists(vault_name) and len(vault_name) > 0:
            self._data['vaults'][vault_name] = copy.deepcopy(DEFAULT_VAULT_DATA['this_name'])
            return True
        return False
    
    def list_vaults(self) -> list:
        result = []
        for vault in self._data['vaults']:
            result.append(vault)
        return result
    
    def set_default_vault(self, vault_name : str) -> bool:
        if vault_name in self._data['vaults']:
            self._current_vault = vault_name
            return True
        log(f'Could not set default vault to {vault_name}','error')
        return False
    
    def rename_vault(self, old_name: str, new_name: str) -> bool:
        if old_name == new_name:
            log('Old and new vault names are the same.', 'warning')
            return False
        
        if old_name == 'default':
            log('You can nor rename the default vault.', 'error')
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

    def vault_exists(self, vault_name: str) -> bool:
        return vault_name in self._data['vaults']

    def delete_vault(self, vault_name: str, permanent: bool = False) -> bool:
        if not self.vault_exists(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return False

        if vault_name == self._current_vault:
            log(f"Cannot delete the currently active vault '{vault_name}'.", 'error')
            return False

        if vault_name == 'default':
            log("Cannot delete the 'default' vault.", 'error')
            return False

        secrets = list(self._data['vaults'][vault_name]['secrets'].keys())
        
        for secret_name in secrets:
            self.delete_secret_entry(secret_name, vault_name=vault_name, permanent=permanent)

        del self._data['vaults'][vault_name]
        log(f"Vault '{vault_name}' has been {'permanently ' if permanent else ''}deleted.", 'info')
        return True

    def add_secret_entry(self, secret_name: str = '', secret_data: str = '', vault_name: str = '') -> bool:
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
            log(f'Could not add {secret_name} to {vault_name} vault, secret already exists', 'error')
            return False
        
    def get_secret(self, secret_name: str, vault_name: str = '') -> dict | None:
        if vault_name == '':
            vault_name = self._current_vault

        if self.vault_exists(vault_name):
            secrets = self._data['vaults'][vault_name]['secrets']
            if secret_name in secrets:
                secrets[secret_name]['meta-data']['accessed'] = datetime.now().isoformat()
                return secrets[secret_name]['secret']
            log(f"Secret '{secret_name}' not found in vault '{vault_name}'.", 'error')
        return None

    def rename_secret_entry(self, old_name: str, new_name: str, vault_name: str = '') -> bool:
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

    def delete_secret_entry(self, secret_name: str, vault_name: str = '', permanent: bool = False) -> bool:
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
                'name': secret_name,
                'data': secret_data
}
            self._data['deleted_secrets'][deletion_uuid] = deletion_entry
            log(f"Secret '{secret_name}' moved to deleted_secrets from vault '{vault_name}'.", 'info')

        return True

    def update_secret(self, secret_name: str, new_secret: str, vault_name: str = '') -> bool:
        if vault_name == '':
            vault_name = self._current_vault

        if self.vault_exists(vault_name):
            secrets = self._data['vaults'][vault_name]['secrets']
            if secret_name in secrets:
                secrets[secret_name]['secret'] = new_secret
                secrets[secret_name]['meta-data']['moddified'] = datetime.now().isoformat()
                return True
        log(f"Failed to update secret '{secret_name}' in vault '{vault_name}'.", 'error')
        return False

    def list_secret_entries(self, vault_name: str = '') -> list:
        if vault_name == '':
            vault_name = self._current_vault
        if self.vault_exists(vault_name):
            return list(self._data['vaults'][vault_name]['secrets'].keys())
        log(f"Vault '{vault_name}' not found.", 'error')
        return []

    def restore_secret_entry(self, deletion_id: str) -> bool:
        deleted_secrets = self._data.get('deleted_secrets', {})

        if deletion_id not in deleted_secrets:
            log(f"Deletion ID '{deletion_id}' not found.", 'error')
            return False

        deleted_entry = deleted_secrets[deletion_id]
        vault_name = deleted_entry['from']
        secret_name = deleted_entry['name']
        secret_data = deleted_entry['data']

        if not self.vault_exists(vault_name):
            log(f"Vault '{vault_name}' no longer exists. Creating it.", 'warn')
            self.create_vault(vault_name)

        secrets = self._data['vaults'][vault_name]['secrets']

        if secret_name in secrets:
            log(f"Secret '{secret_name}' already exists in vault '{vault_name}'.", 'error')
            return False

        secrets[secret_name] = secret_data
        del deleted_secrets[deletion_id]

        log(f"Secret '{secret_name}' successfully restored to vault '{vault_name}'.", 'info')
        return True

    def _create_new_file_data(self) -> dict:
        local_default_db_file_data = copy.deepcopy(DEFAULT_DB_FILE_DATA)
        local_default_db_file_data['vaults']['default'] = copy.deepcopy(DEFAULT_VAULT_DATA['this_name'])
        return local_default_db_file_data