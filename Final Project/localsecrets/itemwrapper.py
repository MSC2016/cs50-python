class ItemWrapper:
    def __init__(self, data: dict):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return repr(self._data)
    
    @property
    def secret(self):
        return self._data.get("secret")

    @property
    def metadata(self):
        return self._data.get("meta-data", {})

    @property
    def user_data(self):
        return self._data.get("user-data", {})
