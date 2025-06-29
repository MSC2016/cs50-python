import sys
import csv


def main():
    # get the arguments and assign them to origin and destination variables
    origin, destination = parse_args()

    try:
        # open both files, the destination file with the w flag because we want to write to it
        with open(origin) as o_file, open(destination, 'w') as d_file:

            # create a dictionary reader
            reader = csv.DictReader(o_file)

            # create a dictionary writer
            writer = csv.DictWriter(d_file, fieldnames=['first', 'last', 'house'])

            # write headers in the destination file
            writer.writeheader()

            # iterate trough all rows in reader and write them to the destination file
            for row in reader:
                writer.writerow(
                    {
                        'first': row['name'].split(',')[1].strip(),
                        'last': row['name'].split(',')[0].strip(),
                        'house': row['house'],
                    }
                )

    # if origin file doesnt exist exit with error code 1
    except FileNotFoundError:
        print(f'Could not read {origin}')
        sys.exit(1)


def parse_args():
    '''
    Ensure only 2 arguments were passed,
    exit with code 1 and error message otherwise.

    '''
    # return error and exit if the user entered too many arguments
    if len(sys.argv) > 3:
        print('Too many command-line arguments')
        sys.exit(1)

    # return error and exit if the user entered too few arguments
    if len(sys.argv) < 3:
        print('Too few command-line arguments')
        sys.exit(1)

    # get origin filename
    origin = sys.argv[1]
    # get destination filename
    destination = sys.argv[2]
    # return the params - filenames
    return origin, destination


# call the main function, only when the script is executed, not when its imported
if __name__ == '__main__':
    main()
