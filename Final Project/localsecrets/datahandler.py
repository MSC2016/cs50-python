import json
from localsecrets.crypto import encrypt, decrypt
from localsecrets.fileio import FileIO
from localsecrets.logger import log

class DataHandler:
    def __init__(self, file_path: str, password: str = None):
        self._fileio = FileIO(file_path)
        self._password = password

    def load(self) -> dict | None:
        raw_data = self._fileio.read_data()
        if raw_data is None:
            return None

        if self._password:
            try:
                raw_data = decrypt(raw_data, self._password)
            except Exception as e:
                log(f"Decryption failed: {e}", "error")
                return None

        try:
            return json.loads(raw_data.decode("utf-8"))
        except Exception as e:
            log(f"Failed to parse JSON: {e}", "error")
            return None

    def save(self, data: dict) -> bool:
        try:
            raw_data = json.dumps(data, indent=2).encode("utf-8")
            if self._password:
                raw_data = encrypt(raw_data, self._password)
            return self._fileio.save_data(raw_data)
        except Exception as e:
            log(f"Failed to save data: {e}", "error")
            return False

