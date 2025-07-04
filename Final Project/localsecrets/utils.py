import sys
from pwinput import pwinput

def cli_get_password():
    try:
        return pwinput.pwinput("Enter your vault password: ", mask="*")
    except KeyboardInterrupt:
        sys.exit('\n\nUser Abort -- Keyboard Interrupt\n')


def cli_create_password(message = "Create a master password: ", mask = '*'):
    try:
        password = pwinput("Create a master password: ", mask)
        password_confirm = pwinput("Confirm master password: ", mask)
        if password != password_confirm:
            print("❌ Passwords do not match!")
            return False
        else:
            return password 
    except KeyboardInterrupt:
        sys.exit('\n\nUser Abort -- Keyboard Interrupt\n')
