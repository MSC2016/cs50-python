import keyring

class KeyStore:
    def __init__(self, service_name: str = "localsecrets"):
        self._service_name = service_name

    def set_key(self, username: str, key: str) -> None:
        keyring.set_password(self._service_name, username, key)

    def get_key(self, username: str) -> str | None:
        return keyring.get_password(self._service_name, username)

    def delete_key(self, username: str) -> None:
        keyring.delete_password(self._service_name, username)

    def has_key(self, username: str) -> bool:
        return keyring.get_password(self._service_name, username) is not None