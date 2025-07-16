from localsecrets.secret_manager import SecretManager
import pprint

def main():
    pp = pprint.PrettyPrinter(indent=2)
    sm = SecretManager('/share/code/db/secrets.db', None)

    sm.create_vault('emails')
    sm.create_vault('work')
    sm.set_default_vault('emails')

    sm.add_secret_entry("gmail_addr", "g-password")
    sm.add_secret_entry("yahoo_addr", "y-password")
    sm.add_secret_entry("protonmail_addr", "p-password")

    pp.pprint(sm.list_secret_entries())

    print("Getting secrets individually...")
    pp.pprint(sm.get_secret("gmail_addr"))
    pp.pprint(sm.get_secret("yahoo_addr"))

    print("Renaming a secret...")
    sm.rename_secret_entry("yahoo_addr", "yahoo-mail")
    print('Renamed =', sm.secret_exists("yahoo-mail"))

    print("Updating secret...")
    sm.update_secret("gmail_addr", "new_gmail_pass")

    print("Copying secret to second vault...")
    sm.copy_secret("gmail_addr", 'emails', 'work')

    print("Moving secret to second vault...")
    sm.move_secret("protonmail_addr", 'emails', 'work')

    print("Setting 'work' as default and listing...")
    sm.set_default_vault('work')
    pp.pprint(sm.list_secret_entries())

    print("Searching secrets with 'proton' in name...")
    pp.pprint(sm.search_secrets("proton"))

    print("Secret metadata...")
    pp.pprint(sm.get_secret_metadata("gmail_addr", 'work'))

    print("Adding user data to secret...")
    sm.set_user_data("gmail_addr", 'work', {"note": "Very important", "backup": "proton_addr"})

    print("Reading user data...")
    pp.pprint(sm.get_user_data("gmail_addr", 'work'))

    print("Listing user data keys...")
    pp.pprint(sm.list_user_data("gmail_addr", 'work'))

    print("Deleting user data entry...")
    sm.delete_user_data_entry("gmail_addr", 'work', "backup")
    pp.pprint(sm.list_user_data("gmail_addr", 'work'))

    print("Purging user data...")
    sm.purge_user_data("gmail_addr", 'work')
    pp.pprint(sm.list_user_data("gmail_addr", 'work'))

    print("Deleting a secret entry (to recycle bin)")
    pp.pprint(sm.list_secret_entries('work'))
    sm.delete_secret_entry("gmail_addr", 'work')
    pp.pprint(sm.list_secret_entries('work'))

    print("Deleted secrets:")
    pp.pprint(sm.list_deleted_secrets())

    print("Restoring deleted 'gmail_addr'")
    deleted = sm.list_deleted_secrets()
    gmail_entry = next((entry for entry in deleted if entry.get('name') == 'gmail_addr'), None)

    if gmail_entry:
        sm.restore_secret_entry(gmail_entry['uuid'])  # or 'deletion_id' if that's the actual field
    else:
        print("No deleted secret named 'gmail_addr' found.")

    print("Deleting secret permanently...")
    sm.delete_secret_entry("gmail_addr", 'work', permanent=True)
    pp.pprint(sm.list_secret_entries('work'))
    pp.pprint(sm.list_deleted_secrets())
    
    print("Purging all deleted secrets...")
    sm.purge_deleted_secrets()
    pp.pprint(sm.list_deleted_secrets())

    print("Vault metadata:")
    pp.pprint(sm.get_vault_metadata('work'))

    print("Saving to file...")
    sm.save_to_file()

    print("DB Metadata:")
    pp.pprint(sm.get_db_metadata())

    print("Final vault list:")
    pp.pprint(sm.list_vaults())

    print("Renaming a vault...")
    sm.rename_vault('work', "work_renamed")
    pp.pprint(sm.list_vaults())

    print("Deleting a vault...")
    sm.set_default_vault('default')
    sm.delete_vault("work_renamed", permanent=True)

    sm.save_to_file()

if __name__ == '__main__':
    main()
