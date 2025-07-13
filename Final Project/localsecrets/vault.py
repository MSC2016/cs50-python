from localsecrets.key import Key
import datetime
import uuid

class Vault:
    def __init__(self, name, use_recycle_vault=True, recycle_vault=None):
        self.name = name
        self._keys = {}
        self.use_recycle_vault = use_recycle_vault
        self.recycle_vault = recycle_vault

    def get_secret(self, key_name):
        key = self._keys.get(key_name)
        if key:
            return key.get_secret()
        return None

    def create_key(self, key_name, secret):
        if key_name in self._keys:
            return False
        if isinstance(secret, Key):
            self._keys[key_name] = secret
        else:
            data = {"secret": secret}
            key = Key(name=key_name, data=data)
            self._keys[key_name] = key
        return True

    def delete_key(self, key_name, permanent=False):
        key = self._keys.get(key_name)
        if not key:
            return False

        if permanent or not self.use_recycle_vault or not self.recycle_vault:
            del self._keys[key_name]
            return True
        else:
            deleted_key = key.to_dict()
            deleted_key['_origin_vault'] = self.name
            deleted_key['_deleted_at'] = datetime.datetime.now().isoformat()
            deleted_key_obj = Key.from_dict(deleted_key)
            if deleted_key_obj:
                unique_name = f"{key_name}_{uuid.uuid4()}"
                self.recycle_vault.create_key(unique_name, deleted_key_obj)
            del self._keys[key_name]
            return True

    def has_key(self, key_name):
        return key_name in self._keys

    def list_keys(self):
        return list(self._keys.keys())

    def search(self, value):
        matches = []
        for key in self._keys.values():
            if key.matches(value):
                matches.append(key)
        return matches

    def to_dict(self):
        return {
            key_name: key.to_dict()
            for key_name, key in self._keys.items()
        }

    @classmethod
    def from_dict(cls, name, data, use_recycle_vault=True, recycle_vault=None):
        vault = cls(name, use_recycle_vault=use_recycle_vault, recycle_vault=recycle_vault)
        for key_name, key_data in data.items():
            key_obj = Key.from_dict(key_data, name=key_name)
            if key_obj:
                vault._keys[key_name] = key_obj
        return vault