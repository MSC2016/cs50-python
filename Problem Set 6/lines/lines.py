import sys


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
    if filename.split('.')[1] != 'py':
        print('Not a Python file')
        sys.exit(1)
    # declaration of variable / empty list to hold data
    data = []
    try:
        # try to open the file, its inside a try catch block to 
        # catch FileNotFoundError and print corresponding message
        with open(filename) as file:
            # assign the lines read from the file to data
            data = file.readlines()
    # if the file doesnt exist, print error and exit
    except FileNotFoundError:
        print('File does not exist')
        sys.exit(1)
    # initialize the lines counter
    counter = 0
    # strip and rstrip all lines and assign result to l
    for line in data:
        l = line.strip().rstrip()
        # if the line is not empty and doesnt start with #, increment the counter
        if not l.startswith('#') and not l == '':
            counter += 1
    # print the result
    print(counter)


# call the main function, only when the script is executed, not when its imported
if __name__ == '__main__':
    main()
