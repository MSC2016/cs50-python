from localsecrets.secret_manager import SecretManager
import json

def test_secret_manager():
    sm = SecretManager('/share/code/db/secrets.db', None)

    vault = 'emails'
    sm.create_vault(vault)
    sm.set_default_vault(vault)


    secrets = sm.list_secret_entries()
    print(f'Secrets in "{vault}": {secrets}')

    for secret in secrets:
        print(sm.get_secret(secret))


    sm.save_to_file()

if __name__ == '__main__':
    test_secret_manager()
