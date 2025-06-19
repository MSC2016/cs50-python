import sys
import requests


def main():
    # get an input from the user
    qty = get_arguments()
    # created a few variables with the data needed
    api_key = ''
    coin_id = 'bitcoin'
    url = f'https://rest.coincap.io/v3/assets/{coin_id}'
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        # get the response, using authentication 
        response = requests.get(url, headers=headers).json()
        # get the piece of data we are interested in
        price = float(response['data']['priceUsd'])
        # calculate the price for the given ammount and print
        print(f'${qty * price:,.4f}')
    # print any exceptions 
    except Exception as e:
        print(e)


def get_arguments():
    '''
    Returns the argument as a float if there is
    only one command argument, and it is a float,
    otherwise exit the program after displaying the
    corresponding error message
    '''
    # exit if the user sent too few arguments
    if len(sys.argv) < 2:
        print('Missing command-line argument')
        sys.exit(1)
    # exit if the user sent too many arguments
    elif len(sys.argv) > 2:
        print('Too many command-line arguments')
        sys.exit(1)
    # if there is one argument
    else:
        # try/catch block to handle arguments that can't be parsed to floats
        try:
            # try to convert to float and return the result
            qty = float(sys.argv[1])
            return qty
        # if conversion to float fails, exit with error message
        except:
            print('Command-line argument is not a number')
            sys.exit(1)


if __name__ == '__main__':
    main()
