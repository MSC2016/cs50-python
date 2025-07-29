from localsecrets.secretmanager import SecretManager
import os

def main():
    path = "secrets.db"
    sm = create_manager(path)

    # Add secrets to two vaults
    add_secret(sm, "work", "email", "work-email-pass")
    add_secret(sm, "work", "slack", "slack-api-key")
    add_secret(sm, "personal", "netflix", "netflix-password")

    # Move item from one vault to another
    move_item(sm, "personal", "archived", "netflix")

    # Add and get user-defined metadata
    sm.set_current_vault("work")
    sm.item.set_user_data("email", "note", "Used for internal comms")
    note = sm.item.get_user_data("email", "note")
    print("Note on work email:", note)

    # Search for all items containing a keyword
    results = search_items(sm, "slack")
    print("Search for 'slack':", [r["item_name"] for r in results])

    # Delete and restore an item into a recovery vault
    delete_and_restore(sm, "work", "slack", "recovery")

    # Final state
    print("Vaults:", sm.list_vaults())
    print("Work vault items:", list_items_in_vault(sm, "work"))
    print("Recovery vault items:", list_items_in_vault(sm, "recovery"))
    print("Archived vault items:", list_items_in_vault(sm, "archived"))

    sm.save_db_file()

def create_manager(path: str, encryption_key=None) -> SecretManager:
    if os.path.exists(path):
        os.remove(path)
    return SecretManager(path, encryption_key)

def add_secret(manager: SecretManager, vault: str, item: str, secret: str) -> bool:
    if vault not in manager._vaults:
        manager.add_vault(vault)
    manager.set_current_vault(vault)
    return manager.add_item(item, secret)

def list_items_in_vault(manager: SecretManager, vault: str = None) -> list[str]:
    if vault:
        manager.set_current_vault(vault)
    return manager.item.list_()

def move_item(manager: SecretManager, vault_from: str, vault_to: str, item_name: str) -> bool:
    manager.set_current_vault(vault_from)
    manager.item.delete(item_name, permanent=False)
    deleted = manager.item.list_deleted()
    if not deleted:
        return False
    uuid = deleted[0]["uuid"]
    manager.add_vault(vault_to)
    return manager.item.restore_deleted(uuid, vault_to)

def delete_and_restore(manager: SecretManager, vault: str, item_name: str, recovery_vault: str) -> bool:
    manager.set_current_vault(vault)
    manager.item.delete(item_name, permanent=False)
    deleted = manager.item.list_deleted()
    if not deleted:
        return False
    uuid = deleted[0]["uuid"]
    manager.add_vault(recovery_vault)
    return manager.item.restore_deleted(uuid, recovery_vault)

def search_items(manager: SecretManager, keyword: str) -> list[dict]:
    return manager.item.search(keyword)


if __name__ == "__main__":
    main()
