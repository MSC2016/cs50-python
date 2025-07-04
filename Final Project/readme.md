# LocalSecrets API Fetcher

#### Video Demo: <URL HERE>
#### Description:

**LocalSecrets API Fetcher** is a Python command-line application that securely stores sensitive information (like API keys) locally on your computer using encryption, and uses them to interact with various public APIs. 

The project was developed as a final submission for Harvard's CS50P (Introduction to Programming with Python) and demonstrates both secure secret management and real-world API integrations in a simple, modular, and testable Python codebase.

---

## Features

- 🔐 **Encrypted Secret Vault**: Stores API keys and secrets in a locally encrypted file.
- 🔓 **Session Unlocking**: Unlock your secret vault once per session using a master password.
- 🌤️ **Weather API Integration**: Get real-time weather data from OpenWeatherMap.
- 📰 **News API Integration**: Fetch the latest headlines from NewsAPI.
- 🐙 **GitHub Integration**: Pull basic info about GitHub users or repos.
- 🧪 **Unit Tested**: Core logic is unit-tested using `pytest`.

---

## File Overview

| File              | Purpose                                                      |
|-------------------|--------------------------------------------------------------|
| `project.py`      | Main script. Provides the CLI, handles user interaction.     |
| `vault_core.py`   | Core encryption/decryption and secret management logic.      |
| `test_project.py` | Tests for key functions in `project.py` using `pytest`.      |
| `requirements.txt`| Required Python packages.                                    |
| `vault.json.enc`  | Encrypted vault file (generated at runtime).                 |
| `README.md`       | This documentation file.                                     |

---

## How It Works

1. When you first run the program, you're prompted to **create a master password**.
2. Your secrets (API keys) are stored in a local file, encrypted using that password.
3. On subsequent runs, you can **unlock the vault once per session**.
4. The CLI allows you to call different APIs using your stored keys.

Example usage:

```bash
$ python project.py --weather
Current weather in Berlin: 19°C, Partly Cloudy

$ python project.py --news
Top headlines:
- AI Beats Humans at Math!
- Python 4.0 Announced

$ python project.py --github octocat
User 'octocat': 8 repositories
