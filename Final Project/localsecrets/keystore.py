import keyring

class KeyStore:
    def __init__(self, service_name: str = "localsecrets"):
        self._service_name = service_name

    def set_key(self, entry_name: str, key: str) -> None:
        keyring.set_password(self._service_name, entry_name, key)

    def get_key(self, entry_name: str) -> str | None:
        return keyring.get_password(self._service_name, entry_name)

    def delete_key(self, entry_name: str) -> None:
        keyring.delete_password(self._service_name, entry_name)

    def has_key(self, entry_name: str) -> bool:
        return keyring.get_password(self._service_name, entry_name) is not None