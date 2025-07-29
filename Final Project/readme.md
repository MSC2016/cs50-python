# LocalSecrets — A Simple Secret Manager

#### Video Demo:

#### Description:
LocalSecrets is a Python-based secret manager that securely stores, manages, and retrieves sensitive information (API keys, passwords, tokens) organized into multiple vaults. It supports adding user data, soft-deleting items, restoring deleted secrets, and searching across vaults.

This project was developed as a final project for **CS50’s Introduction to Programming with Python**.

## Features
- Create multiple vaults to organize passwords and api keys
- Add, rename, and delete secrets within vaults
- Soft delete secrets with the option to restore later
- Add custom user data to secrets
- Search secrets by name or metadata
- Save and load secrets securely from an encrypted database file

### Running the demo
```bash
python project.py
