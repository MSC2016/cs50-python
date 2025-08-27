# Secure Secret Manager – CS50 Python Final Project

## Project Overview

**Secure Secret Manager** is a Python application designed to store, manage, and retrieve secrets such as passwords, API keys, and personal notes. It uses a vault-based system to organize secrets and supports features like metadata, soft-deletion, restoration, and keyword-based searching.

---

## Features

- **Vault Management**: Create multiple vaults to categorize secrets.
- **Secret Storage**: Add secrets to vaults, with optional user-defined metadata.
- **Flexible Retrieval**: Retrieve secrets using multiple syntaxes (`sm.get_secret()`, `sm[vault].get_secret()`, or `sm[vault][item].secret`).
- **Search**: Find secrets containing specific keywords across all vaults.
- **Move Secrets**: Transfer secrets between vaults easily.
- **Soft Deletion & Recovery**: Delete items without permanent loss and restore them later.
- **Persistent Storage**: Data stored in an encrypted Json file.

---

## Usage Examples

### 1. Creating a SecretManager

```python
from localsecrets.secretmanager import SecretManager

# Encryption_key set to None ensures the file is stored as plaintext
sm = SecretManager('secrets.db', None)

# If a string is entered the resulting file is encrypted
sm = SecretManager('secrets.db', 'None')

# If nothing is entered, an encryption key is derived from an empty string
sm = SecretManager('secrets.db')

```

---

### 2. Adding Secrets & Metadata

```python
# Add secrets to vaults
sm.add_vault('work')
sm.add_vault('personal')

sm.add_item('email', 'work-email-pass')  # create the item in the current vault
sm.add_item('email', 'work-email-pass', 'work-vault')  # create the item in the work-vault

# A vault named 'default' is always present and can not be deleted, if no vault is provided when performing any operation, the current vault is used

sm.set_current_vault('work-vault') # Set the current vault
sm.item('email').set_user_data('note', 'Used for internal comms') # Add user data to an item named 'email' in the 'work-vault'


```

---

### 3. Retrieving Secrets

```python
# Multiple syntaxes supported - the next examples return only the secret
print(sm.get_secret('email'))
print(sm['default'].get_secret('email'))
print(sm['default']['email'].secret)
```

---

### 4. Moving Secrets Between Vaults

```python
sm.move_item('email', 'work-vault', 'default') # move 'email' from 'work-vault' to 'default' vault
print(sm['default']['email'].secret) # print the secret
```

---

### 5. Soft Deletion & Recovery

```python
# Soft delete an item without permanent loss
sm.item.delete('email', permanent=False)


# Restore into a recovery vault
deleted = sm.item.list_deleted()
uuid = deleted[0]['uuid']
sm.item.restore_deleted(uuid, 'recovered') # move an item with a given uuid to the 'recovered' vault

# If no vault is specified, the item will be recovered to its original vault, returns false if the destination vault has an item with the same name
```

---

### 6. Searching Secrets

```python
results = sm.item.search('TV')  # returns list of dicts
for r in results:
    print('FOUND:', r)

# EXAMPLES:
# FOUND: {'type': 'vault', 'vault': 'personal', 'item_name': 'netflix', 'uuid': None, 'data': {'secret': 'netflix-pass', 'user-data': {'Expires': '01/01/2026', 'user1': 'Living room TV', 'user2': "Wife's cell phone", 'user3': 'Bedroom TV'}}}
# FOUND: {'type': 'deleted', 'vault': 'personal', 'item_name': 'Netflix Living Room TV', 'uuid': 'e0c0c49c-4cbb-408b-8ac0-7acea29ded41', 'data': {'secret': 'netflix-pass'}}
# type 'vault' means its a normal item, type 'deleted' means the item was found in the deleted items
# uuid is only assigned to deleted items, this avoids name collisions when deleting items

```

---

### 7. Listing Items in the current vault

```python

sm.set_current_vault('work')
items = sm.item.list_()
print(items)  # ['email', 'slack', ...]
```

---

## Final Thoughts / Todo List

- The goal of this project is to avoid hardcoding passwords. Currently, SecretManager requires a password to decrypt the file. If no password is entered, the file is encrypted with a key derived from an empty string, which is not secure. Prompting for a password via the CLI proved tedious during development. In the future, I plan to add support for storing the master password in the OS keyring, allowing it to be retrieved automatically across Windows, WSL, and Ubuntu. The implementation is still a work in progress, but it’s usable as-is with room for improvement.
---