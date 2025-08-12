from localsecrets.logger import log
from filelock import FileLock
import os

class FileIO:
    def __init__(self, file_path : str):
        self._file_path = file_path
        self._lock_path = f"{file_path}.lock"
        self._backup_path = f"{file_path}.backup"
        self._lock = FileLock(self._lock_path)

    def file_exists(self):
        '''
        Checks whether the secrets file exists.

        Returns:
            bool: True if the file exists.
        '''
        return os.path.exists(self._file_path)

    def read_data(self) -> bytes | None:
        '''
        Reads and returns binary data from the file.

        Returns:
            bytes | None: The file contents if read successfully, otherwise None.
        '''
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
        '''
        Saves data to the file.

        Returns:
            bool: True if the data was saved and validated successfully.
        '''
        try:
            with self._lock:
                self._backup_file()
                with open(self._file_path, 'wb') as f:
                    f.write(data)
                    log(f'{len(data)} bytes saved to {self._file_path}')

                with open(self._file_path, 'rb') as f:
                    if f.read() == data:
                        log('Validation successful: saved data matches input', 'debug')
                        if os.path.exists(self._backup_path):
                            os.remove(self._backup_path)
                            log(f'Removed backup file {self._backup_path}', 'debug')
                        self._delete_lock_file()
                        return True

                log('Validation failed: written file does not match input', 'error')
                if os.path.exists(self._file_path):
                    os.remove(self._file_path)
                    self._restore_backup()

                return os.path.exists(self._file_path)
        except Exception as e:
            log(f'Save error: {e}', 'error')
            try:
                log('Trying to restore from backup after exception', 'warn')
                self._restore_backup()
            except Exception as restore_err:
                log(f"Failed to restore backup: {restore_err}", 'error')
            return False

    def _backup_file(self):
        if os.path.exists(self._file_path):
            os.replace(self._file_path, self._backup_path)
            log(f'{self._file_path} renamed to {self._backup_path}', 'debug')

    def _restore_backup(self):
        if os.path.exists(self._backup_path):
            os.replace(self._backup_path, self._file_path)
            log(f'Restored {self._file_path} from {self._backup_path}', 'debug')

    def _delete_lock_file(self):
        if os.path.exists(self._lock_path):
            os.remove(self._lock_path)
