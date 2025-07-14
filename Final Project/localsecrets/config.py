from datetime import datetime

DEBUG = True

DEFAULT_DB_FILE_DATA = {
    'meta-data' : {
        'created': datetime.now().isoformat(),
        'accessed' : datetime.now().isoformat(),
        'moddified' : datetime.now().isoformat(),
    },
    'config' : {
        'soft_delete_secrets': True,
    },
    'vaults': {},
    'deleted_secrets': {},
}

DEFAULT_VAULT_DATA = {
    'this_name': {
        'meta-data':{
            'created': datetime.now().isoformat(),
            'accessed' : datetime.now().isoformat(),
            'moddified' : datetime.now().isoformat(),
        },
        'secrets' : {}
    }
}
