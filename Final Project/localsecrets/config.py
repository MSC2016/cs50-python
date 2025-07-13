from datetime import datetime

DEBUG = True

DEFAULT_DB_FILE_DATA = {
    'config': {
        'use_recycle_vault': True,
        'created': datetime.now().isoformat().split('.')[0].replace('T', ' '),
        'version': '1.0'
    },
    'default': {
        'created_at': datetime.now().isoformat().split('.')[0].replace('T', ' '),
        'accessed' : None,
        'moddified' : None
    },
    'recycle_bin': {
        'items': [],
        'created_at': datetime.now().isoformat().split('.')[0].replace('T', ' '),
        'accessed' : None,
        'moddified' : None
        }
}