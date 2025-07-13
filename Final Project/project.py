from localsecrets.config import DEFAULT_DB_FILE_DATA
from localsecrets.datahandler import DataHandler
from localsecrets.vaults import Vaults

def main():
    dh = DataHandler('/share/code/db/secrets.db', 'password')
    
    raw_data = dh.load()  # This returns the dict, or None
    if raw_data is None:
        print("No data found or failed to load.")
        return
    
    vaults = Vaults()
    vaults.load_from_dict(raw_data)
    
    print(vaults.list_vaults())



def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()