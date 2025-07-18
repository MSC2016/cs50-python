from localsecrets.secretmanager import SecretManager
from localsecrets.utils import get_password
from pprint import pprint

def main():

    # Initialize SecretManager (unencrypted)
    sm = SecretManager('/share/code/db/secrets.db',None)

    print("Vaults after init")
    pprint(sm.vaults.list())

    sm.vaults.add('default')
    sm.vaults.add('emails')
    sm.vaults.add('work')
    sm.vaults.add('temp')
    pprint(sm.vaults.list())

    sm.add_item('my_gmail_addr','my_gmail_password')
    sm.save_db_file()

    sm.vaults['default']['my_gmail_addr'].set_data('today','friday')
    sm.vaults['default']['my_gmail_addr'].set_data('tomorrow','saturday')
    sm.vaults['default']['my_gmail_addr'].get_data('today')


    sm.vaults['default'].add_item('gmail_addr2', secret='me@gmail.com')
    sm.vaults['default'].add_item('github_token', secret='ghp_ABC123')
    sm.vaults['emails'].add_item('yahoo_addr', secret='me@yahoo.com')
    sm.vaults['work'].add_item('slack_pwd', secret='slack_pass')
    sm.add_item('test_727','secret_727','work')
    sm.vaults['work'].add_item('test_728','secret_728')
    sm.save_db_file()

    print("Items per vault:")
    for vault in sm.vaults.list():
        print(f"{vault}: {sm.vaults[vault].list_items()}")

    print("Access secrets:")
    print(sm.vaults['default']['my_gmail_addr'])
    print(sm.vaults['emails']['yahoo_addr'])
    print(sm.vaults['emails']['yahoo_addr'])

    sm.vaults['default'].delete_item('gmail_addr')
    sm.vaults['default'].delete_item('github_token')
    print("After deleting all items from 'default':")
    print(sm.vaults['default'].list_items())

    print("Attempting to non existing vaults")
    sm.vaults.delete('temp')

    sm.vaults['emails'].delete()

    print("Vaults after deletions:")
    pprint(sm.vaults.list())

    print('Renaming vaults')
    sm.vaults.add('aa')
    sm.rename_vault('aa', 'bb')
    sm.vaults['bb'].rename('cc')
    sm.vaults.rename('cc', 'dd')
    pprint(sm.vaults.list())

    print("Vault existence checks:")
    print("Has 'dd':", sm.has_vault('dd'), sm.vaults.has('dd'))
    print("Has 'ghost':", sm.has_vault('ghost'), sm.vaults.has('ghost'))

    print("Items in all vaults:")
    for v in sm.vaults.list():
        print(f"{v}: {sm.vaults[v].list_items()}")
    sm.save_db_file()

if __name__ == "__main__":
    main()