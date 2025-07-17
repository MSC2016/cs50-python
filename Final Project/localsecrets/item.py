class Item:
    def __init__(self, data: dict):
        self._data = data

    @property
    def secret(self):
        return self._data.get("secret")

    @property
    def metadata(self):
        return self._data.get("metadata", {})

    @property
    def user_data(self):
        return self._data.get("user-data", {})
