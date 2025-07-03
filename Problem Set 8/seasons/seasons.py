from datetime import date
import inflect
import re
import sys


def main():
    # get the user input
    b_date = input('Date of Birth: ')

    # get the user birth date as a date object
    birth_date = get_user_birth_date(b_date)

    # get today's date as a date object
    today = date.today()

    # get the difference as a timedelta object
    minutes = get_minutes_delta(today,birth_date)

    # print the result
    print(convert_to_text(minutes))


def convert_to_text(minutes):
    # initialize the inflect engine object
    p = inflect.engine()
    # return the number of minutes as text, capitalizing the first letter 
    # and suppressing the 'and' word
    return f"{p.number_to_words(minutes, andword='').capitalize()} minutes"


def get_minutes_delta(date_a, date_b):
    '''
    Returns the number of minutes that separates date_a from date_b
    '''
    return abs((date_a-date_b).days * 1440)


def get_user_birth_date(birth_date):
    '''
    Gets an input from the user, expecting a date of birth formatted as YYYY-MM-DD
    Returns a date object with the given date, or exits the program if the user input
    is not in the speciffied format and therefore cant be parsed, or 
    '''

    # search pattern, expects date provided acording to spec, tolerating 
    # space characters in the begining or end of the string and single digit 
    # month or day
    pattern = r'^\s*(\d{4})-(\d{1,2})-(\d{1,2})\s*$'
    # search the user input for the data
    search_results = re.search(pattern, birth_date)
    # if we get usable data
    if search_results:
        try:
            # unpack the tupple 
            year, month, day = search_results.groups()
            # use the unpacked data as input to create a date object
            # and return it
            return date(int(year), int(month), int(day))
        except:
            # do nothing in case an exception occurs
            pass
    # if execution reaches this, the user's input either didnt match the regex 
    # pattern, or matched the pattern but couldnt be converted to a valid date, 
    # in either case we exit with error code.
    sys.exit('Invalid date')


if __name__ == "__main__":
    main()