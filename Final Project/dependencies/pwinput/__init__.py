"""PWInput
A cross-platform Python module for password input with masking.
By Al Sweigart, unified logic and simplified for modern Python.
"""

__version__ = '1.0.5'

import sys

# Platform-specific setup for getch
if sys.platform == 'win32':
    from msvcrt import getch
else:  # Linux, macOS, WSL
    import tty
    import termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def pwinput(prompt='Password: ', mask='*'):
    if not isinstance(prompt, str):
        raise TypeError(f'prompt must be a str, not {type(prompt).__name__}')
    if not isinstance(mask, str):
        raise TypeError(f'mask must be a zero- or one-character str, not {type(mask).__name__}')
    if len(mask) > 1:
        raise ValueError('mask must be a zero- or one-character str')

    if mask == '' or sys.stdin is not sys.__stdin__:
        from getpass import getpass
        return getpass(prompt)

    entered_password = []
    sys.stdout.write(prompt)
    sys.stdout.flush()

    while True:
        key = ord(getch())
        if key == 13:  # Enter
            sys.stdout.write('\n')
            sys.stdout.flush()
            return ''.join(entered_password)
        elif key in (3, 26):  # Ctrl+C, Ctrl+Z
            raise KeyboardInterrupt("Ctrl+C or Ctrl+Z detected")
        elif key in (8, 127):  # Backspace/Del
            if entered_password:
                sys.stdout.write('\b \b')
                sys.stdout.flush()
                entered_password.pop()
        elif 0 <= key <= 31:  # Unprintable characters
            pass
        else:
            char = chr(key)
            sys.stdout.write(mask)
            sys.stdout.flush()
            entered_password.append(char)

if __name__ == '__main__':
    try:
        password = pwinput("Enter password: ")
        print("You entered:", password)
    except KeyboardInterrupt:
        print("\nInput interrupted.")