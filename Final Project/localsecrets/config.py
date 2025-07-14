from datetime import datetime

DATETIME = datetime.now().isoformat()
DEBUG = True

DEFAULT_DB_FILE_DATA = {
    'config' : {
        'soft_delete_secrets': True,
        'default_vault_name' : 'default'
    },
    'deleted_secrets': {},
    'vaults': {},
    'meta-data' : {
        'created': DATETIME,
        'accessed' : DATETIME,
        'moddified' : DATETIME,
    }
}

DEFAULT_VAULT_DATA = {
    'this_name': {
        'secrets' : {},
        'meta-data':{
            'created': DATETIME,
            'accessed' : DATETIME,
            'moddified' : DATETIME,
        }
    }
}

DEFAULT_SECRET_DATA = {
    'secret_name' : {
        'secret' : '',
        'meta-data':{
            'created': DATETIME,
            'accessed' : DATETIME,
            'moddified' : DATETIME,
        }
    }
}

DEFULT_DELETED_KEY = {
    'uuid': {
        'deleted' : DATETIME,
        'data' : {},
    }
}