import os
import json
from localsecrets.logger import log
from localsecrets.config import DEFAULT_DB_FILE_DATA
from filelock import FileLock

class FileIO:
    def __init__(self, file_path : str):
        self._file_path = file_path
        self._lock_path = f"{file_path}.lock"
        self._backup_path = f"{file_path}.backup"
        self._lock = FileLock(self._lock_path)


    def create_db_file(self) -> bool:
        if os.path.exists(self._file_path):
            log(f'Cant create DB, {self._file_path} already exists', 'error')
            return False
        return self.save_db_file(DEFAULT_DB_FILE_DATA)


    def read_db_file(self) -> dict:
        if not os.path.exists(self._file_path):
            log(f'Cant read DB, {self._file_path} doesnt exist.', 'error')
            return None
        try:
            with self._lock:
                with open(self._file_path, 'rb') as f:
                    data = f.read()
                return json.loads(data.decode('utf-8'))
        except Exception:
            return False
        

    def save_db_file(self, data: dict) -> bool:
        try:
            log("Attempting to acquire file lock...", "debug")
            with self._lock.acquire():
                log("Lock acquired.", "debug")
                # Create backup if file exists
                if os.path.exists(self._file_path):
                    log(f'{self._file_path} already exists, creating backup.')
                    if os.path.exists(self._backup_path):
                        log(f'{self._backup_path} already exists, deleting.')
                        os.remove(self._backup_path)
                    log(f'Renaming {self._file_path} to {self._backup_path}')
                    os.rename(self._file_path, self._backup_path)
                
                # Write new data
                with open(self._file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                    log(f'{self._file_path} open in write mode, data saved.')
                
                # Validate by reading back
                with open(self._file_path, 'r') as f:
                    log(f'Reading content of {self._file_path}')
                    saved_data = json.load(f)
                
                if saved_data == data:
                    # Remove backup on success
                    log('Data match')
                    if os.path.exists(self._backup_path):
                        log(f'Removing {self._backup_path}')
                        os.remove(self._backup_path)
                    return True
                else:
                    # Restore backup on validation failure
                    log(f'Data in {self._file_path} is wrong', 'error')
                    if os.path.exists(self._file_path):
                        log(f'Deleting {self._file_path}', 'warn')
                        os.remove(self._file_path)
                    if os.path.exists(self._backup_path):
                        log(f'Restoring {self._file_path} from {self._backup_path}')
                        os.rename(self._backup_path, self._file_path)
                    else:
                        log(f'{self._backup_path} not found, data was lost', 'error')
                    return False

        except Exception as e:
            log(e)
            # Restore backup on any error
            if os.path.exists(self._backup_path):
                os.rename(self._backup_path, self._file_path)
            return False
        
