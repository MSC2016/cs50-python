from localsecrets import vaults
from dependencies.pwinput import pwinput
from localsecrets.fileio import FileIO
from localsecrets.config import DEFAULT_DB_FILE_DATA
from localsecrets.datahandler import DataHandler

def main():
    dh = DataHandler('/mnt/d/db/secrets.db', 'kkk')
    dh2 = DataHandler('/mnt/d/db/secrets2.db', 'kkk')
    dh3 = DataHandler('/mnt/d/db/secrets3.db')

    dh.save('aaa')
    print(dh.load())

    dh2.save('aaa')
    print(dh2.load())

    dh3.save('aaa')
    print(dh3.load())

def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()