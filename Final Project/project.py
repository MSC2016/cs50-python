from localsecrets.secretmanager import SecretManager
import sys
def main():
    sm = SecretManager('/share/code/db/secrets.db', None)

    print("Vaults:", sm.vaults.list())
    print("Items:", sm.vaults['default'].list_items())

    sm.vaults['default'].delete_item('gmail_addr')
    print("items:", sm.vaults['default'].list_items())

    sm.vaults['default'].delete_item('github_token')
    print("items:", sm.vaults['default'].list_items())
    print("items:", sm.vaults.list_items('default'))


    print(sm.current_vault['yahoo_addr'].secret)
    print(sm.current_vault['yahoo_addr']['secret'])
    print(sm.current_vault['yahoo_addr'])

    print("Vaults:", sm.vaults.list())
    sm.vaults.delete('aa')
    print("Vaults:", sm.vaults.list())
    sm.vaults['emails'].delete()
    print("Vaults:", sm.vaults.list())
    sm.delete_vault('TEST-VAULT-777')
    print("Vaults:", sm.vaults.list())

    sm.vaults.add('aa')
    print("Vaults:", sm.vaults.list())
    sm.rename_vault('aa', 'bb')
    print("Vaults:", sm.vaults.list())
    sm.vaults['bb'].rename('cc')
    print("Vaults:", sm.vaults.list())
    sm.vaults.rename('cc','dd')
    print("Vaults:", sm.vaults.list())

    vaultname = 'dd'
    print(sm.has_vault(vaultname))
    print(sm.vaults.has(vaultname))

    vaultname = 'd2'
    print(sm.has_vault(vaultname))
    print(sm.vaults.has(vaultname))

    print(sm.vaults.list_items('default'))
    print(sm.vaults['default'].list_items())
    print(sm.list_items('default'))


if __name__ == "__main__":
    main()