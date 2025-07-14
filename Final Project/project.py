from localsecrets.secret_manager import SecretManager

def main():

    sm = SecretManager('/share/code/db/secrets.db','')
    sm.set_password(' ')
    sm.save_file()

if __name__ == '__main__':
    main()