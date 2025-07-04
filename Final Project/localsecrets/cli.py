import argparse
from localsecrets import utils
from localsecrets.vault import create_vault_file, load_vault_file

def main():
    parser = argparse.ArgumentParser(
        prog="localsecrets",
        description=(
            "🔐 LocalSecrets - A simple local encrypted key vault\n\n"
            "Examples:\n"
            "  python3 -m localsecrets.cli --create myvault.db\n"
            "  python3 -m localsecrets.cli --load myvault.db\n"
            "  python3 -m localsecrets.cli --info myvault.db\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create', action='store_true', help="Create a new encrypted secrets vault")
    group.add_argument('--load', action='store_true', help="Load an existing secrets vault")
    group.add_argument('--info', action='store_true', help="Show info about a vault file (to be implemented)")

    parser.add_argument('file', help="Vault file path")

    args = parser.parse_args()

    if args.create:
        password = utils.cli_create_password()
        create_vault_file(args.file, password)
        print(f"✅ Vault created at {args.file}.")

    elif args.load:
        password = utils.cli_get_password()
        vault = load_vault_file(args.file, password)
        if vault:
            print(f"✅ Vault loaded from {args.file}.")
        else:
            print("❌ Failed to load vault. Wrong password or corrupted file.")

    elif args.info:
        # Placeholder for future implementation
        print(f"ℹ️  Info requested for {args.file} (feature not implemented yet).")

if __name__ == "__main__":
    main()
