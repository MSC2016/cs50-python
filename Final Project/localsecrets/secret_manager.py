from localsecrets.crypto import encrypt, decrypt
from localsecrets.fileio import FileIO
from localsecrets.logger import log
from datetime import datetime
from  localsecrets.config import DEFAULT_DB_FILE_DATA, DEFAULT_VAULT_DATA
import json, copy, uuid

class SecretManager:
    def __init__(self, file_path: str, password =''):
        """
        
        """
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

    def get_db_metadata(self) -> dict:
        metadata = {
            'total_vaults': len(self._data.get('vaults', {})),
            'vaults': {},
            'total_deleted_secrets': len(self._data.get('deleted_secrets', {})),
            'config': self._data.get('config', {}),
            'current_vault': self._current_vault,
        }

        for vault_name, vault_data in self._data.get('vaults', {}).items():
            vault_meta = vault_data.get('meta-data', {})
            total_secrets = len(vault_data.get('secrets', {}))
            metadata['vaults'][vault_name] = {
                'meta-data': vault_meta,
                'total_secrets': total_secrets
            }
        return metadata

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
        log(f'Vault "{vault_name}" already exists', 'warn')
        return False
    
    def list_vaults(self) -> list:
        return list(self._data['vaults'].keys())
    
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

    def get_vault_metadata(self, vault_name: str = '') -> dict:
        vault_name = vault_name or self._current_vault

        if not self.vault_exists(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return None

        vault = self._data['vaults'][vault_name]
        return vault.get('meta-data', None)

    def add_secret_entry(self, secret_name: str = '', secret_data: str = '', vault_name: str = '') -> bool:
        vault_name = vault_name or self._current_vault

        if len(vault_name) > 0 and len(secret_name) > 0 and len(secret_data) > 0:
            if vault_name in self._data['vaults']:
                vault = self._data['vaults'][vault_name]
                if secret_name not in vault['secrets']:
                    secret_entry = {
                        'secret': secret_data,
                        'meta-data': {
                            'created': datetime.now().isoformat(),
                            'accessed': datetime.now().isoformat(),
                            'modified': datetime.now().isoformat()
                        },
                        'user-data': {}
                    }
                    vault['secrets'][secret_name] = secret_entry
                    return True
            log(f'Could not add {secret_name} to {vault_name} vault, secret already exists', 'error')
            return False
        
    def get_secret(self, secret_name: str, vault_name: str = '') -> dict:
        vault_name = vault_name or self._current_vault

        if self.vault_exists(vault_name):
            secrets = self._data['vaults'][vault_name]['secrets']
            if secret_name in secrets:
                secrets[secret_name]['meta-data']['accessed'] = datetime.now().isoformat()
                return secrets[secret_name]['secret']
            log(f"Secret '{secret_name}' not found in vault '{vault_name}'.", 'error')
        return None

    def rename_secret_entry(self, old_name: str, new_name: str, vault_name: str = '') -> bool:
        vault_name = vault_name or self._current_vault

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
        secrets[new_name]['meta-data']['modified'] = datetime.now().isoformat()

        log(f"Secret '{old_name}' renamed to '{new_name}' in vault '{vault_name}'.", 'info')
        return True

    def delete_secret_entry(self, secret_name: str, vault_name: str = '', permanent: bool = False) -> bool:
        vault_name = vault_name or self._current_vault

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
        vault_name = vault_name or self._current_vault

        if self.vault_exists(vault_name):
            secrets = self._data['vaults'][vault_name]['secrets']
            if secret_name in secrets:
                secrets[secret_name]['secret'] = new_secret
                secrets[secret_name]['meta-data']['modified'] = datetime.now().isoformat()
                return True
        log(f"Failed to update secret '{secret_name}' in vault '{vault_name}'.", 'error')
        return False

    def secret_exists(self, secret_name: str, vault_name: str = '') -> bool:
        vault_name = vault_name or self._current_vault
        
        if not self.vault_exists(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return False
        
        return secret_name in self._data['vaults'][vault_name]['secrets']

    def copy_secret(self, secret_name: str, from_vault: str, to_vault: str) -> bool:
        if from_vault not in self._data['vaults']:
            log(f"Source vault '{from_vault}' does not exist.", 'error')
            return False

        if to_vault not in self._data['vaults']:
            log(f"Target vault '{to_vault}' does not exist.", 'error')
            return False

        from_vault_secrets = self._data['vaults'][from_vault]['secrets']
        to_vault_secrets = self._data['vaults'][to_vault]['secrets']

        if secret_name not in from_vault_secrets:
            log(f"Secret '{secret_name}' not found in vault '{from_vault}'.", 'error')
            return False

        # Avoid overwriting existing secret
        if secret_name in to_vault_secrets:
            log(f"Secret '{secret_name}' already exists in target vault '{to_vault}'.", 'error')
            return False

        # Deep copy the secret entry
        to_vault_secrets[secret_name] = copy.deepcopy(from_vault_secrets[secret_name])
        log(f"Copied secret '{secret_name}' from '{from_vault}' to '{to_vault}'.", 'info')
        return True

    def move_secret(self, secret_name: str, from_vault: str, to_vault: str) -> bool:
        if self.copy_secret(secret_name, from_vault, to_vault):
            return self.delete_secret_entry(secret_name, from_vault)
        return False

    def search_secrets(self, query: str, vault_name: str = '') -> list:
        query = query.lower()
        results = []

        vaults = self._data['vaults']
        target_vaults = [vault_name] if vault_name else vaults.keys()

        for vname in target_vaults:
            if vname not in vaults:
                log(f"Vault '{vname}' does not exist.", 'error')
                continue

            for sname, entry in vaults[vname]['secrets'].items():
                # Flatten all values into a string to check for match
                entry_str = f"{sname} {entry.get('secret', '')}".lower()

                for k, v in entry.get('meta-data', {}).items():
                    entry_str += f" {k} {v}".lower()
                for k, v in entry.get('user-data', {}).items():
                    entry_str += f" {k} {v}".lower()

                if query in entry_str:
                    results.append({
                        'vault': vname,
                        'name': sname,
                        'secret': entry.get('secret')
                    })

        return results

    def get_secret_metadata(self, secret_name: str, vault_name: str = '') -> dict:
        vault_name = vault_name or self._current_vault

        if not self.vault_exists(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return None

        secrets = self._data['vaults'][vault_name]['secrets']

        if secret_name not in secrets:
            log(f"Secret '{secret_name}' does not exist in vault '{vault_name}'.", 'error')
            return None

        return secrets[secret_name].get('meta-data', None)

    def list_secret_entries(self, vault_name: str = '') -> list:
        vault_name = vault_name or self._current_vault
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
    
    def list_deleted_secrets(self) -> list:
        deleted_secrets = self._data.get('deleted_secrets', {})
        result = []

        for deletion_id, entry in deleted_secrets.items():
            result.append({
                'uuid': deletion_id,
                'name': entry['name'],
                'from': entry['from'],
                'deleted': entry['deleted']
            })

        return result

    def delete_deleted_secret_permanently(self, deletion_id: str) -> bool:
        deleted_secrets = self._data.get('deleted_secrets', {})

        if deletion_id in deleted_secrets:
            del deleted_secrets[deletion_id]
            log(f"Deleted secret with ID '{deletion_id}' permanently from deleted_secrets.", 'info')
            return True

        log(f"Secret with ID '{deletion_id}' not found in deleted_secrets.", 'error')
        return False

    def purge_deleted_secrets(self) -> int:
        count = len(self._data.get('deleted_secrets', {}))
        if count > 0:
            self._data['deleted_secrets'].clear()
            log(f"Purged {count} deleted secret(s).", 'info')
        else:
            log("No deleted secrets to purge.", 'info')
        return count

    def set_user_data(self, secret_name: str, vault_name: str, user_data: dict) -> bool:
        vault_name = vault_name or self._current_vault

        if not isinstance(user_data, dict):
            log("User data must be a dictionary of key-value pairs.", "error")
            return False

        vault = self._data['vaults'].get(vault_name)
        if not vault:
            log(f"Vault '{vault_name}' does not exist.", "error")
            return False

        secret = vault['secrets'].get(secret_name)
        if not secret:
            log(f"Secret '{secret_name}' not found in vault '{vault_name}'.", "error")
            return False

        secret.setdefault('user-data', {}).update(user_data)
        log(f"Updated user-data for secret '{secret_name}' in vault '{vault_name}'.", "info")
        return True

    def get_user_data(self, secret_name: str, vault_name: str) -> dict:
        vault_name = vault_name or self._current_vault
        vault = self._data['vaults'].get(vault_name)
        if not vault:
            log(f"Vault '{vault_name}' does not exist.", "error")
            return {}

        secret = vault['secrets'].get(secret_name)
        if not secret:
            log(f"Secret '{secret_name}' not found in vault '{vault_name}'.", "error")
            return {}

        return secret.get('user-data', {})

    def list_user_data(self, secret_name: str, vault_name: str) -> list:
        vault_name = vault_name or self._current_vault
        user_data = self.get_user_data(secret_name, vault_name)
        return list(user_data.keys())

    def delete_user_data_entry(self, secret_name: str, vault_name: str, key: str) -> bool:
        vault_name = vault_name or self._current_vault
        user_data = self.get_user_data(secret_name, vault_name)

        if key not in user_data:
            log(f"User-data key '{key}' not found in secret '{secret_name}' of vault '{vault_name}'.", "error")
            return False

        del user_data[key]
        log(f"Deleted user-data key '{key}' from secret '{secret_name}' in vault '{vault_name}'.", "info")
        return True

    def purge_user_data(self, secret_name: str, vault_name: str) -> bool:
        vault_name = vault_name or self._current_vault

        vault = self._data['vaults'].get(vault_name)
        if not vault:
            log(f"Vault '{vault_name}' does not exist.", "error")
            return False

        secret = vault['secrets'].get(secret_name)
        if not secret:
            log(f"Secret '{secret_name}' not found in vault '{vault_name}'.", "error")
            return False

        secret['user-data'] = {}
        log(f"Purged all user-data from secret '{secret_name}' in vault '{vault_name}'.", "info")
        return True


    def _create_new_file_data(self) -> dict:
        local_default_db_file_data = copy.deepcopy(DEFAULT_DB_FILE_DATA)
        local_default_db_file_data['vaults']['default'] = copy.deepcopy(DEFAULT_VAULT_DATA['this_name'])
        return local_default_db_file_data