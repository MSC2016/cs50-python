import inspect
from localsecrets.config import DEBUG, now

def log(message: str, level: str = 'info'):
    if not DEBUG:
        return

    level = level.upper()
    if level not in {'INFO', 'WARN', 'ERROR', 'DEBUG'}:
        level = 'INFO'

    COLORS = {
        'INFO': '\033[94m',
        'WARN': '\033[93m',
        'ERROR': '\033[91m',
        'DEBUG': '\033[90m',
        'END': '\033[0m'
    }

    frame = inspect.currentframe()
    outer_frame = frame.f_back
    func_name = outer_frame.f_code.co_name
    local_vars = outer_frame.f_locals
    class_name = local_vars['self'].__class__.__name__ if 'self' in local_vars else None
    location = f'{class_name}.{func_name}()' if class_name else f'{func_name}()'
    timestamp = now()

    print(f"{COLORS[level]}[{timestamp}] [{level}] [{location}] {message}{COLORS['END']}")
