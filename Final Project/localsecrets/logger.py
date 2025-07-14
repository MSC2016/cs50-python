import inspect
from datetime import datetime
from localsecrets.config import DEBUG

def log(message: str, level: str = 'info'):
    if not DEBUG:
        return

    level = level.upper()
    if level not in {'INFO', 'WARN', 'ERROR', 'DEBUG'}:
        level = '_INFO'

    COLORS = {
        'INFO': '\033[94m',   # Blue
        'WARN': '\033[93m',   # Yellow
        'ERROR': '\033[91m',  # Red
        'DEBUG': '\033[90m',  # Grey
        'END': '\033[0m'
    }

    frame = inspect.currentframe()
    outer_frame = frame.f_back
    func_name = outer_frame.f_code.co_name
    local_vars = outer_frame.f_locals
    class_name = local_vars['self'].__class__.__name__ if 'self' in local_vars else None
    location = f'{class_name}.{func_name}()' if class_name else f'{func_name}()'
    timestamp = datetime.now().isoformat().split('.')[0].replace('T', ' ')

    # Log message
    color = COLORS[level]
    end = COLORS['END']
    print(f'{color}[{timestamp}] [{level}] [{location}] {message}{end}')
