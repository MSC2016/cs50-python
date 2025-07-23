from localsecrets.utils import update_meta_data

class Vault:
    def __init__(self, vault_data: dict, update_db_meta, update_vault_meta):
        self._vault = vault_data
        self._update_db_meta = update_db_meta
        self._update_vault_meta = update_vault_meta

    def __getitem__(self, item):
        if item not in self._vault:
            raise KeyError(f"Item '{item}' not found in vault.")

        self._update_db_meta()
        self._update_vault_meta()

        self._vault[item]['metadata'] = update_meta_data(
            self._vault[item].get('metadata', {}),
            accessed=True
        )

        return self._vault[item]['secret']
