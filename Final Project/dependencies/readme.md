# pwinput (Modified Version)

## Why this dependency?

I selected **pwinput** because I want to have some visual feedback while typing passwords, showing `*` instead of plain text. This improves the user experience during password input.

## Why this isn’t in `requirements.txt`

After installing pwinput via `pip`, I realized it lacked the ability to abort input with **Ctrl+C** (or **Ctrl+Z**). This is important to let users cancel password input.

## What I changed

I added two lines of code in the main input loops (for both Linux/macOS and Windows):

```python
elif key in (3, 26):  # Ctrl+C or Ctrl+Z
    raise KeyboardInterrupt("Ctrl+C or Ctrl+Z detected")
´´´´

This allows the user to abort input by pressing Ctrl+C or Ctrl+Z, raising a KeyboardInterrupt which can be caught and handled by the program.