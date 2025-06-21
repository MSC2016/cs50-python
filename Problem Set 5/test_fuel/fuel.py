import sys


def main():
  # start a loop
    while True:
        try:
            # get the user input
            user_input = input('Fraction: ')

            # calculate the tank level percentage
            percentage = convert(user_input)

            print(gauge(percentage))
            sys.exit(0)
        # As specified, every error should make us promp the user again
        # so i will just use general exception go back to the begining 
        except Exception:
            continue


def convert(fraction):
    '''
    receives a string with a fraction, splits the string by '/' and
    returns an integer that represents the fraction as a percentage
    '''
    try:
        # split fraction into a and b
        a, b = fraction.split('/')
        # convert a and b to integers
        a = int(a)
        b = int(b)
    # raise exception if a or b are not integers, or the string is not properly formatted
    except (ValueError):
        raise ValueError('Input must be formatted as a/b, where a and b are integers')
    # raise ZeroDivisionError if b is zero
    if b == 0:
        raise ZeroDivisionError('Can not divide by zero')
    # raise ValueError if the tank is above 100%
    if a > b:
        raise ValueError('Fraction result is more than one, a can not be larger than b')
    # raise ValueError if a or b are negative
    if a < 0 or b < 0:
        raise ValueError("Fraction result can not be negative")
    # calculate percentage and return it
    return round((a / b) * 100)


def gauge(percentage):
    '''
    receives a percentage value, and returns:
    E for an empty tank,
    F for a full tank, or
    a formatted string that represents how full the tank is
    '''
    if percentage <= 1:
        return 'E'
    elif percentage >= 99:
        return 'F'
    return f'{percentage:g}%'
    

if __name__ == "__main__":
    main()
