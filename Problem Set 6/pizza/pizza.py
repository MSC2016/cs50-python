import sys
import csv
from tabulate import tabulate


def main():
    # return error and exit if the user entered too many arguments
    if len(sys.argv) > 2:
        print('Too many command-line arguments')
        sys.exit(1)
    # return error and exit if the user entered too few arguments
    if len(sys.argv) < 2:
        print('Too few command-line arguments')
        sys.exit(1)
    # return error and exit if the filename doesnt end with .py
    filename = sys.argv[1]
    if filename.split('.')[1] != 'csv':
        print('Not a csv file')
        sys.exit(1)
    try:
        # try to open the file, its inside a try catch block to 
        # catch FileNotFoundError and print corresponding message
        with open(filename) as file:
            # create a dictionary reader
            reader = csv.DictReader(file)
            # convert data to a list
            table = list(reader)
        # print the result with tabulate
        print(tabulate(table, headers='keys', tablefmt="grid"))
    # if the file doesnt exist, print error and exit
    except FileNotFoundError:
        print('File does not exist')
        sys.exit(1)


# call the main function, only when the script is executed, not when its imported
if __name__ == '__main__':
    main()
