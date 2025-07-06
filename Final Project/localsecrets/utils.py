import sys
from dependencies.pwinput import pwinput

def get_password(message = "Enter password: ", mask="*"):
    try:
        return pwinput.pwinput(message, mask)
    except KeyboardInterrupt:
        sys.exit('\n\nUser Abort -- Keyboard Interrupt\n')


def create_password(message1 = "Create password: ", message2 = "Confirm password: ", mask = '*'):
    try:
        password = pwinput(message1, mask)
        password_confirm = pwinput(message2, mask)
        if password != password_confirm:
            return False
        else:
            return password 
    except KeyboardInterrupt:
        sys.exit('\n\nUser Abort -- Keyboard Interrupt\n')
