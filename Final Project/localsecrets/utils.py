import sys
from dependencies.pwinput import pwinput
from localsecrets.config import now
from localsecrets.logger import log


def get_password(message = "Enter password: ", mask="*"):
    try:
        return pwinput(message, mask)
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

def update_meta_data(meta_data, created = False, accessed = False, modified = False):
    if not isinstance(meta_data, dict):
        raise ValueError('meta_data must be of tipe dict.')
    
    obj_created = meta_data.get('created',now())
    obj_modified = meta_data.get('modified',now())
    obj_accessed = meta_data.get('accessed',now())

    if created or accessed or modified:
        if created:
            obj_created = now()
            obj_modified = now()
            obj_accessed = now()
        if accessed:
            obj_accessed = now()
        if modified:
            obj_modified = now()
        meta_data.update({
            'created': obj_created,
            'accessed': obj_accessed,
            'modified': obj_modified
        })
        return meta_data
    else:
        log('Nothing to modify, you need to set created, modified or accessed to true', 'warn')
        return meta_data