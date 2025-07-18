class Item:
    def __init__(self, item_data: dict):
        self._data = item_data

    def set_data(self, key: str, value):
        self._data.setdefault("user-data", {})[key] = value

    def get_data(self, key: str, default=None):
        return self._data.get("user-data", {}).get(key, default)

    def __repr__(self):
        return self._data.get('secret')

