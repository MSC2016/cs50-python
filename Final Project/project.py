from localsecrets.secretmanager import SecretManager
import os


def main():

    # The path is only in the project's root for testing purposes,
    # Encryption is set to None for easy debugging, the whole idea 
    # of this project is to prevent passwords and api keys from being
    # posted to github

    path = 'secrets.db'

    if os.path.exists(path):
        os.remove(path)

    sm = create_manager(path)

    sm.add_vault('work')
    sm.add_vault('personal')

    add_secret(sm, 'work', 'file-server-access', 'file-server-access-password', {'username_is': 'Company email addr'})
    add_secret(sm, 'personal', 'work-email', 'work-email-pass')
    add_secret(sm, 'personal', 'netflix', 'netflix-pass', {'Expires': '01/01/2026', 'user1': 'Living room TV', 'user2': 'Wife\'s cell phone'})

    # built in
    sm.item('netflix').set_user_data('user3', 'Bedroom TV')
    sm['work'].add_item('project one', 'api-key-for-project-one')
    print('Api key for project one is:', sm['work'].get_secret('project one'))

    if move_secret(sm, 'personal', 'work', 'work-email'):
        print('Moved email secret to personal vault.')
    else:
        print('Something went wrong')

    sm.add_item('Netflix Living Room TV', 'netflix-pass')
    sm.delete_item('Netflix Living Room TV', 'personal')
    query = 'TV'
    results = search_secrets(sm, query)
    print(f'Search results for "{query}":', results)

    delete_and_restore(sm, 'netflix', 'personal')
    print('Deleted and restored netflix secret.')

    print('Final vaults:', sm.list_vaults())

    sm.save_db_file()

def create_manager(path='secrets.db'):
    '''Initialize and return a SecretManager.'''
    return SecretManager(path, None)


def add_secret(manager: SecretManager, vault: str, name: str, secret: str, metadata: dict = None):
    '''Add a secret with optional metadata to a vault.'''
    manager.set_current_vault(vault)
    manager.add_item(name, secret, vault)
    if metadata:
        for key, value in metadata.items():
            manager.item(name).set_user_data(key, value)


def move_secret(manager: SecretManager, src_vault: str, dest_vault: str, name: str):
    '''Move a secret between vaults.'''
    return manager.move_item(name, src_vault, dest_vault)


def search_secrets(manager: SecretManager, keyword: str):
    '''Return list of secrets matching a keyword across all vaults.'''
    return [item for item in manager.item.search(keyword)]


def delete_and_restore(manager: SecretManager, name: str, vault: str):
    """Soft-delete a secret and restore it."""

    manager.delete_item(name, vault)
    deleted_items = manager.item.list_deleted()

    match = None
    for item in deleted_items:
        _uuid = item['uuid']
        _name = item['name']
        _vault = item['vault']

        if vault != _vault:
            continue

        if name == _name:
            match = _uuid  # most recent match

    if not match:
        print(f"No deleted item found for '{name}' in vault '{vault}'")
        return False
    
    return manager.item.restore_deleted(match)


if __name__ == '__main__':
    main()
