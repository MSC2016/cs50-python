from localsecrets import vaults
from dependencies.pwinput import pwinput
from localsecrets.fileio import FileIO
from localsecrets.config import DEFAULT_DB_FILE_DATA
from localsecrets.datahandler import DataHandler

def main():
    dh = DataHandler('/share/code/db/secrets.db', 'password')
    dh2 = DataHandler('/share/code/db/secrets2.db', 'kkk')
    dh3 = DataHandler('/share/code/db/secrets3.db')

    dh.save(DEFAULT_DB_FILE_DATA)
    print(dh.load())
    print(dh2.load())
    print(dh3.load())

def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()