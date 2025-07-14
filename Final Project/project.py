from localsecrets.config import DEFAULT_DB_FILE_DATA
from localsecrets.secret_manager import SecretManager

def main():

    sm = SecretManager('/share/code/db/secrets.db','')
    sm.set_pw('')
    sm.save()


if __name__ == '__main__':
    main()