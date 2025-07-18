from localsecrets.crypto import encrypt, decrypt
from localsecrets.fileio import FileIO
from localsecrets.logger import log
from localsecrets.vaults import VaultManager
from datetime import datetime
from  localsecrets.config import DEFAULT_DB_FILE_DATA
import json, copy, uuid

class SecretManager:
    def __init__(self, file_path: str, encryption_key =''):
        """
        
        """
        self._fileio = FileIO(file_path)
        self._file_path = file_path
        self._data = {}
        self._default_vault = "default"
        self._encryption_key = encryption_key
        self._no_encryption = encryption_key == None


        if self._fileio.file_exists():
            log(f'Found {self._file_path}')
            self.load_from_file()
        else:
            log(f'{self._file_path} does not exist, creating a new file...')
            self._data = self._create_new_file_data()
            self.save_db_file()

        self.vaults = VaultManager(
            self._data,
            self.get_default_vault,
            self.set_default_vault
            )

    @property
    def default_vault(self):
        return self.vaults[self._default_vault]

    # DB FILE METHODS

    def load_from_file(self) -> bool:
        data = self._fileio.read_data()
        log(f'Loaded {len(data)} bytes of data.')
        if not data:
            return False
        try:
            if self._no_encryption:
                self._data = json.loads(data.decode())
                return True
            else:
                data = decrypt(data, self._encryption_key)
                self._data = json.loads(data.decode())
                return True
        except Exception:
            log('Could not read/decrypt data, make sure to enter the right password.', 'error')
            raise IOError('Could not read/decrypt data, check the encryption key.')

    def save_db_file(self) -> bool:
        try:
            encoded = json.dumps(self._data, indent=4).encode()
            log(f'Encoded {len(encoded)} bytes of data.')
            if self._no_encryption:
                log(f'Saving {self._file_path} as a plain text file','warn')
                return self._fileio.save_data(encoded)
            else:
                data = encrypt(encoded, self._encryption_key)
                log(f'Saving {self._file_path} with encryption','info')
                return self._fileio.save_data(data)
        except Exception as e:
            log(f"Save failed: {e}", "error")
            return False
        
    def set_encryption_key(self, encryption_key = '') -> bool:
        if encryption_key == None:
            log(f'Encryption disabled, {self._file_path} will be saved as a plain text file.','warn')
            self._encryption_key = ''
            self._no_encryption = True
            return True
        if isinstance(encryption_key,str):
            self._no_encryption = False
            self._encryption_key = encryption_key
            log('Encryption enabled.', 'info')
            return True
        raise ValueError('Password must be "None" to save as plain text, or a string of any length')


    # VAULT RELATED METHODS
    
    def get_default_vault(self):
        return self._default_vault

    def set_default_vault(self, vault_name):
        if vault_name in self._data['vaults'].keys():
            self._default_vault = vault_name
            return True
        log(f'Could not set default vault to {vault_name}', 'error')
        return False
    
    def delete_vault(self, vault_name: str, permanent: bool = False) -> bool:
        return self.vaults.delete(vault_name, permanent)
    
    def rename_vault(self, old_name: str, new_name: str) -> bool:
        return self.vaults.rename(old_name, new_name)

    def has_vault(self, vault_name: str) -> bool:
        return vault_name in self._data['vaults']

    def list_items(self, vault_name: str = '') -> list:
        vault_name = vault_name or self._default_vault
        return self.vaults.list_items(vault_name)
    
    # ITEM RELATED METHODS
    def add_item(self, name: str, secret: str, vault: str = '') -> bool:
        vault = vault or self._default_vault
        return self.vaults.add_item(name, secret, vault)


    def get_item(self, item_name: str, vault_name: str = '') -> dict:
        vault_name = vault_name or self._default_vault

        if self.has_vault(vault_name):
            items = self._data['vaults'][vault_name]['items']
            if item_name in items:
                return items[item_name]['secret']
            log(f"Secret '{item_name}' not found in vault '{vault_name}'.", 'info')
        return None

    def rename_item(self, old_name: str, new_name: str, vault_name: str = '') -> bool:
        vault_name = vault_name or self._default_vault

        if not self.has_vault(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return False

        items = self._data['vaults'][vault_name]['items']

        if old_name not in items:
            log(f"Secret '{old_name}' does not exist in vault '{vault_name}'.", 'error')
            return False

        if new_name in items:
            log(f"Secret '{new_name}' already exists in vault '{vault_name}'.", 'error')
            return False

        items[new_name] = items.pop(old_name)

        log(f"Secret '{old_name}' renamed to '{new_name}' in vault '{vault_name}'.", 'info')
        return True

    def delete_item(self, item_name: str, vault_name: str = '', permanent: bool = False) -> bool:
        vault_name = vault_name or self._default_vault

        if not self.has_vault(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return False

        items = self._data['vaults'][vault_name]['items']

        if item_name not in items:
            log(f"Secret '{item_name}' does not exist in vault '{vault_name}'.", 'error')
            return False

        soft_delete_enabled = self._data.get('config', {}).get('soft_delete_items', False)

        if permanent or not soft_delete_enabled:
            del items[item_name]
            log(f"Secret '{item_name}' permanently deleted from vault '{vault_name}'.", 'info')
        else:
            secret_data = items.pop(item_name)
            deletion_uuid = str(uuid.uuid4())
            deletion_entry = {
                'deleted': datetime.now().isoformat(),
                'from': vault_name,
                'name': item_name,
                'data': secret_data
}
            self._data['deleted_items'][deletion_uuid] = deletion_entry
            log(f"Secret '{item_name}' moved to deleted_items from vault '{vault_name}'.", 'info')

        return True

    def update_item(self, item_name: str, item_secret: str, vault_name: str = '') -> bool:
        vault_name = vault_name or self._default_vault

        if self.has_vault(vault_name):
            items = self._data['vaults'][vault_name]
            if item_name in items:
                items[item_name]['secret'] = item_secret
                return True
        log(f"Failed to update secret '{item_name}' in vault '{vault_name}'.", 'error')
        return False

    def has_item(self, secret_name: str, vault_name: str = '') -> bool:
        vault_name = vault_name or self._default_vault
        
        if not self.has_vault(vault_name):
            log(f"Vault '{vault_name}' does not exist.", 'error')
            return False
        
        return secret_name in self._data['vaults'][vault_name]

    def copy_item(self, item_name: str, orig_vault: str, dest_vault: str) -> bool:
        if orig_vault not in self._data['vaults']:
            log(f"Source vault '{orig_vault}' does not exist.", 'error')
            return False

        if dest_vault not in self._data['vaults']:
            log(f"Target vault '{dest_vault}' does not exist.", 'error')
            return False

        orig_vault = self._data['vaults'][orig_vault]
        dest_vault = self._data['vaults'][dest_vault]

        if item_name not in orig_vault:
            log(f"Secret '{item_name}' not found in vault '{orig_vault}'.", 'error')
            return False

        # Avoid overwriting existing secret
        if item_name in dest_vault:
            log(f"Secret '{item_name}' already exists in target vault '{dest_vault}'.", 'error')
            return False

        # Deep copy the secret entry
        dest_vault[item_name] = copy.deepcopy(orig_vault[item_name])
        log(f"Copied secret '{item_name}' from '{orig_vault}' to '{dest_vault}'.", 'info')
        return True

    def move_item(self, secret_name: str, from_vault: str, to_vault: str) -> bool:
        if self.copy_item(secret_name, from_vault, to_vault):
            return self.delete_item(secret_name, from_vault)
        return False

    def search_item(self, query: str, vault_name: str = '') -> list:
        query = query.lower()
        results = []

        vaults = self._data['vaults']
        target_vaults = [vault_name] if vault_name else vaults.keys()

        for vname in target_vaults:
            if vname not in vaults:
                log(f"Vault '{vname}' does not exist.", 'error')
                continue

            for sname, entry in vaults[vname]:
                # Flatten all values into a string to check for match
                entry_str = f"{sname} {entry.get('secret', '')}".lower()

                for k, v in entry.get('user-data', {}).items():
                    entry_str += f" {k} {v}".lower()

                if query in entry_str:
                    results.append({
                        'vault': vname,
                        'name': sname,
                        'secret': entry.get('secret')
                    })

        return results


    # SOFT-DELETE/DELETE/RECOVERY RELATED
    def restore_secret_entry(self, deletion_id: str) -> bool:
        deleted_items = self._data.get('deleted_items', {})

        if deletion_id not in deleted_items:
            log(f"Deletion ID '{deletion_id}' not found.", 'error')
            return False

        deleted_entry = deleted_items[deletion_id]
        vault_name = deleted_entry['from']
        item_name = deleted_entry['name']
        item_secret = deleted_entry['data']

        if not self.has_vault(vault_name):
            log(f"Vault '{vault_name}' no longer exists. Creating it.", 'warn')
            self.create_vault(vault_name)

        items = self._data['vaults'][vault_name]

        if item_name in items:
            log(f"Secret '{item_name}' already exists in vault '{vault_name}'.", 'error')
            return False

        items[item_name] = item_secret
        del deleted_items[deletion_id]

        log(f"Secret '{item_name}' successfully restored to vault '{vault_name}'.", 'info')
        return True
    
    def list_deleted_items(self) -> list:
        deleted_items = self._data.get('deleted_items', {})
        result = []

        for deletion_id, entry in deleted_items.items():
            result.append({
                'uuid': deletion_id,
                'name': entry['name'],
                'from': entry['from'],
                'deleted': entry['deleted']
            })

        return result

    def permantly_delete_item(self, deletion_id: str) -> bool:
        deleted_items = self._data.get('deleted_items', {})

        if deletion_id in deleted_items:
            del deleted_items[deletion_id]
            log(f"Deleted secret with ID '{deletion_id}' permanently from deleted_items.", 'info')
            return True

        log(f"Secret with ID '{deletion_id}' not found in deleted_items.", 'error')
        return False

    def purge_deleted_items(self) -> int:
        count = len(self._data.get('deleted_items', {}))
        if count > 0:
            self._data['deleted_items'].clear()
            log(f"Purged {count} deleted secret(s).", 'info')
        else:
            log("No deleted items to purge.", 'info')
        return count


    # USERDATA
    def set_user_data(self, item_name: str, vault_name: str, user_data: dict) -> bool:
        vault_name = vault_name or self._default_vault

        if not isinstance(user_data, dict):
            log("User data must be a dictionary of key-value pairs.", "error")
            return False

        vault = self._data['vaults'].get(vault_name)
        if not vault:
            log(f"Vault '{vault_name}' does not exist.", "error")
            return False

        item = vault['items'].get(item_name)
        if not item:
            log(f"Item '{item_name}' not found in vault '{vault_name}'.", "error")
            return False

        item.setdefault('user-data', {}).update(user_data)
        log(f"Updated user-data for secret '{item_name}' in vault '{vault_name}'.", "info")
        return True

    def get_user_data(self, secret_name: str, vault_name: str) -> dict:
        vault_name = vault_name or self._default_vault
        vault = self._data['vaults'].get(vault_name)
        if not vault:
            log(f"Vault '{vault_name}' does not exist.", "error")
            return {}

        item = vault['items'].get(secret_name)
        if not item:
            log(f"item '{secret_name}' not found in vault '{vault_name}'.", "error")
            return {}

        return item.get('user-data', {})

    def list_user_data(self, secret_name: str, vault_name: str) -> list:
        vault_name = vault_name or self._default_vault
        user_data = self.get_user_data(secret_name, vault_name)
        return list(user_data.keys())

    def delete_user_data_entry(self, secret_name: str, vault_name: str, key: str) -> bool:
        vault_name = vault_name or self._default_vault
        user_data = self.get_user_data(secret_name, vault_name)

        if key not in user_data:
            log(f"User-data key '{key}' not found in secret '{secret_name}' of vault '{vault_name}'.", "error")
            return False

        del user_data[key]
        log(f"Deleted user-data key '{key}' from item '{secret_name}' in vault '{vault_name}'.", "info")
        return True

    def purge_user_data(self, item_name: str, vault_name: str) -> bool:
        vault_name = vault_name or self._default_vault

        vault = self._data['vaults'].get(vault_name)
        if not vault:
            log(f"Vault '{vault_name}' does not exist.", "error")
            return False

        item = vault['items'].get(item_name)
        if not item:
            log(f"Secret '{item_name}' not found in vault '{vault_name}'.", "error")
            return False

        item['user-data'] = {}
        log(f"Purged all user-data from secret '{item_name}' in vault '{vault_name}'.", "info")
        return True


    # PRIVATE
    def _create_new_file_data(self) -> dict:
        local_default_db_file_data = copy.deepcopy(DEFAULT_DB_FILE_DATA)
        local_default_db_file_data['vaults']['default'] = {}
        return local_default_db_file_data
    

