class Key:
    def __init__(self, name, data):
        self._name = name
        if "secret" not in data:
            raise ValueError("Missing required 'secret' field in key data.")
        self._data = data

    @property
    def name(self):
        return self._name

    def get_secret(self):
        return self._data.get("secret")

    def set_secret(self, value, force=False):
        if "secret" in self._data and self._data["secret"] and not force:
            return False
        self._data["secret"] = value
        return True

    def get_data(self, field_name):
        if field_name == "secret":
            return self.get_secret()
        return self._data.get(field_name)

    def set_data(self, field_name, value):
        if field_name == "secret":
            raise ValueError("Use set_secret() to update the secret field.")
        self._data[field_name] = value

    def delete_data(self, field_name):
        if isinstance(field_name, str):
            field_name = [field_name]

        for field in field_name:
            if field == "secret":
                return False
            if field in self._data:
                del self._data[field]
            else:
                return False
        return True

    def list_data_fields(self):
        return [key for key in self._data if key != "secret"]

    def to_dict(self):
        return {
            "name": self.name,
            **self._data
        }

    def matches(self, value):
        return any(value in str(v) for v in self._data.values())

    @classmethod
    def from_dict(cls, data, name=""):
        if not isinstance(data, dict) or "secret" not in data:
            return None
        key_name = name or data.get("name", "")
        key_data = {k: v for k, v in data.items() if k != "name"}
        return cls(name=key_name, data=key_data)


    @staticmethod
    def validate(data):
        return isinstance(data, dict) and "secret" in data

    def save_to(self, vault):
        if vault.has_key(self.name):
            return False
        return vault.create_key(self.name, self)
