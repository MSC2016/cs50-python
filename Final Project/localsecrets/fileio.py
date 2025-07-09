import os
from localsecrets.logger import log
from filelock import FileLock

class FileIO:
    def __init__(self, file_path : str):
        self._file_path = file_path
        self._lock_path = f"{file_path}.lock"
        self._backup_path = f"{file_path}.backup"
        self._lock = FileLock(self._lock_path)

    def read_data(self) -> bytes | None:
        if not os.path.exists(self._file_path):
            log(f'Cannot read, {self._file_path} does not exist.', 'error')
            return None
        try:
            with self._lock:
                with open(self._file_path, 'rb') as f:
                    return f.read()
        except Exception as e:
            log(f"Failed to read data: {e}", "error")
            return None
        
    def save_data(self, data: bytes) -> bool:
        try:
            with self._lock:
                # Step 1: Backup current file if it exists
                self._backup_file()
                log(f'Prepared backup for {self._file_path}', 'debug')

                # Step 2: Write new data
                with open(self._file_path, 'wb') as f:
                    f.write(data)
                log(f'Wrote data to {self._file_path}', 'debug')

                # Step 3: Validate written content
                with open(self._file_path, 'rb') as f:
                    if f.read() == data:
                        log('Validation successful: written data matches input', 'debug')
                        if os.path.exists(self._backup_path):
                            os.remove(self._backup_path)
                            log(f'Removed backup file {self._backup_path}', 'debug')
                        return True

                # Step 4: Validation failed, restore backup
                log('Validation failed: written file does not match input', 'error')
                if os.path.exists(self._file_path):
                    os.remove(self._file_path)
                    log(f'Removed invalid file {self._file_path}', 'error')
                    self._restore_backup()
                
                if os.path.exists(self._file_path):
                    log(f'Restore successful', 'debug')
                else:
                    log(f'Restore failed - data may be lost', 'error')

        except Exception as e:
            log(f'Save error: {e}', 'error')
            try:
                self._restore_backup()
                log('Restored from backup after exception', 'error')
            except Exception as restore_err:
                log(f"Failed to restore backup: {restore_err}", 'error')
            return False

    def _backup_file(self):
        if os.path.exists(self._file_path):
            if os.path.exists(self._backup_path):
                os.remove(self._backup_path)
            os.rename(self._file_path, self._backup_path)

    def _restore_backup(self):
        if os.path.exists(self._backup_path):
            os.rename(self._backup_path, self._file_path)
