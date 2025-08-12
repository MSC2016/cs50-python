from localsecrets.secretmanager import SecretManager
import sys
import os

def main():

    path = 'secrets.db'
    sm = create_manager(path)

    if sm.export_no_encryption('/root/secrets_backup.json'):
        print('saved to root dir')
    else:
        print('As expected, trying to save to the root dir, w/out root privileges didnt work.')

    # add an item and some user data to the default vault
    sm.add_item('test','my test api key')
    sm.item('test').set_user_data('expires','tomorrow')
    # get the item
    print(sm['default'].get_item('test'))
    # get the secret using three different methods, these are redundant but intentional,
    # i want to interact with the secret manager using whatever syntax style suits me, and they all work.
    print(sm.get_secret('test'))
    print(sm['default'].get_secret('test'))
    print(sm['default']['test'].secret)

    # Add secrets to two vaults
    add_secret(sm, 'work', 'email', 'work-email-pass')
    add_secret(sm, 'work', 'slack', 'slack-api-key')
    add_secret(sm, 'personal', 'netflix', 'netflix-password')

    sm.move_item('slack','work','personal')
    print(sm['personal']['slack'].secret)
    sm.move_item('slack','personal','work')

    sm.set_current_vault('personal')
    print(sm.item('netflix').secret)

    # Move item from one vault to another
    move_item(sm, 'personal', 'archived', 'netflix')

    # Add and get user-defined metadata
    sm.set_current_vault('work')
    sm.item.set_user_data('email', 'note', 'Used for internal comms')
    note = sm.item.get_user_data('email', 'note')
    print('Note on work email:', note)

    # Search for all items containing a keyword
    results = search_items(sm, 'slack')
    print(f'Search for "slack":', [result for result in results])

    # Delete and restore an item into a recovery vault
    delete_and_restore(sm, 'work', 'slack', 'recovery')

    # Final state
    print('Vaults:', sm.list_vaults())
    print('Work vault items:', list_items_in_vault(sm, 'work'))
    print('Recovery vault items:', list_items_in_vault(sm, 'recovery'))
    print('Archived vault items:', list_items_in_vault(sm, 'archived'))


    sm.save_db_file()

def create_manager(path: str, encryption_key=None) -> SecretManager:
    """
    Creates a new SecretManager instance, replacing any existing file at the given path.

    Returns:
        SecretManager: A new instance with a fresh database.
    """
    if os.path.exists(path):
        os.remove(path)
    return SecretManager(path, encryption_key)

def add_secret(manager: SecretManager, vault: str, item: str, secret: str) -> bool:
    """
    Adds a secret to the specified vault in the SecretManager.
    Creates the vault if it does not exist, sets it as current,
    and adds the item with the given secret.

    Returns:
        bool: True if the secret was added successfully, False otherwise.
    """
    if vault not in manager._vaults:
        manager.add_vault(vault)
    manager.set_current_vault(vault)
    return manager.add_item(item, secret)

def list_items_in_vault(manager: SecretManager, vault: str = None) -> list[str]:
    """
    Lists all item keys in the specified vault.
    If no vault is provided, uses the current vault set in the manager.

    Returns:
        list[str]: A list of item keys in the vault.
    """
    if vault:
        manager.set_current_vault(vault)
    return manager.item.list_()

def move_item(manager: SecretManager, vault_from: str, vault_to: str, item_name: str) -> bool:
    """
    Moves an item from one vault to another within the SecretManager.
    Performs a soft delete in the source vault and restores the item into the destination vault.

    Returns:
        bool: True if the item was successfully moved, False otherwise.
    """
    manager.set_current_vault(vault_from)
    manager.item.delete(item_name, permanent=False)
    deleted = manager.item.list_deleted()
    if not deleted:
        return False
    uuid = deleted[0]['uuid']
    manager.add_vault(vault_to)
    return manager.item.restore_deleted(uuid, vault_to)

def delete_and_restore(manager: SecretManager, vault: str, item_name: str, recovery_vault: str) -> bool:
    """
    Soft-deletes an item from a vault and restores it into a different vault.
    Useful for testing recovery or moving items via soft delete and restore.

    Returns:
        bool: True if the item was successfully deleted and restored, False otherwise.
    """
    manager.set_current_vault(vault)
    manager.item.delete(item_name, permanent=False)
    deleted = manager.item.list_deleted()
    if not deleted:
        return False
    uuid = deleted[0]['uuid']
    manager.add_vault(recovery_vault)
    return manager.item.restore_deleted(uuid, recovery_vault)

def search_items(manager: SecretManager, keyword: str) -> list[dict]:
    """
    Searches for items in the db file matching the given keyword.

    Returns:
        list[dict]: A list of matching items with their associated data.
    """
    return manager.item.search(keyword)

if __name__ == '__main__':
    main()

