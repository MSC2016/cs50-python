from localsecrets.crypto import encrypt, decrypt
from localsecrets.fileio import FileIO
from localsecrets.logger import log
from localsecrets.config import DEFAULT_DB_FILE_DATA
import json

class SecretManager:
    def __init__(self, file_path, password=''):
        self._fileio = FileIO(file_path)
        self._file_path = file_path
        self._data = {}
        self._current_vault = "default"
        self._password = password

        if self._fileio.file_exists():
            log(f'{self._file_path} exists, loading...')
            self.load()
        else:
            log(f'{self._file_path} does not exist, creating a new file...')
            self._data = DEFAULT_DB_FILE_DATA
            self.save()

    def load(self):
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

    def save(self):
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

    def set_pw(self, password=''):
        if self.load():
            self._password = password
        else:
            log('Can not change password, unless file was open with the right password', 'error')
            raise IOError('Can not change password, unless file was open with the right password')




