from localsecrets.secretmanager import SecretManager
from localsecrets.config import DEBUG
from pprint import pprint

def main():
    # Initialize with plaintext (unencrypted)
    sm = SecretManager('/share/code/db/secrets.db', None)
    sm._use_soft_delete = False

    sm.add_vault('v2')
    sm.add_item('teste','segredo')
    sm.set_current_vault('v2')
    print(sm['default']['teste'])
    print(sm.get_item('teste', 'default'))

    sm.add_item('belongs to v2', 'sss')
    print(sm.get_item('belongs to v2'))
    sm.save_db_file()


if __name__ == "__main__":
    main()
