from datetime import datetime

DEBUG = True
version = 1.0

def now():
    return datetime.now().isoformat().split('.')[0].replace('T', ' ')
