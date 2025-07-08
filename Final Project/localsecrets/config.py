from datetime import datetime

DEBUG = True

DEFAULT_DB_FILE_DATA = {
    'config': {
        'use_recycle_vault': True,
        'created_at': datetime.now().isoformat(),
        'version': '1.0'
    },
    'vaults': {
        'default': {},
        'recycle_bin': {'items': []}
    }
}