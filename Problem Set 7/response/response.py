from validator_collection import validators


def main():
    print(validate_email(input("What's your email address? : ")))


def validate_email(s):
    '''
    Returns Valid if a valid email address is provided as input,
    otherwise returns Invalid
    '''
    # validators raise a ValueError if an invalid email is provided
    # if there is an exception in this try/except block the function 
    # returns Invalid, otherwise return valid
    try:
        if validators.email(s):
            return 'Valid'
    except Exception:
        return 'Invalid'


if __name__ == "__main__":
    main()