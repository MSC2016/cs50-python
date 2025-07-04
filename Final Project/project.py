from localsecrets import vault
from pwinput import pwinput

def main():
    pw = pwinput()
    print(pw)
    print(vault.test_vault())


def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()