from localsecrets import vaults
from dependencies.pwinput import pwinput
from localsecrets.fileio import FileIO

def main():
    f = FileIO('/mnt/d/secrets.db')
    f.create_db_file()
    print(f.read_db_file())


def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()