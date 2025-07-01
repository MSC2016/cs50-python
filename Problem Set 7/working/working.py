import re
import sys

DEBUG = False


def main():
    print(convert(input("Hours: ")))
    

def convert(s):
    # pattern to search, the logic is equal on both sides of the word 'to', enforcing one or two digits,
    # optionally followed by ':' and one or two digits, followed by am or pm
    # i am not punishing the user for the way he uses spaces, either too many or to few 
    pattern = r' *(\d{1,2})(?::(\d{1,2}))? (am|pm) to (\d{1,2})(?::(\d{1,2}))? (am|pm) *$'

    # run the search and assign the result to matches
    matches = re.search(pattern, s, re.IGNORECASE)

    # raise ValueError if there are no matches
    if matches is None:
        raise ValueError(s.strip() + ' is not a valid input for conversion.')

    # append all captured values to a list
    capturedValues = []
    for match in matches.groups():
        capturedValues.append(match)

    # optional debug print of all the values in the list - check input
    if DEBUG:
        print('original values:', capturedValues)

    # convert None type to int(0) for minutes when not specified, and str(hours) to int(hours)
    for i in range(len(capturedValues)):
        if capturedValues[i] is None:
            capturedValues[i] = 0
        elif capturedValues[i].isdigit():
            capturedValues[i] = int(capturedValues[i])

    # optional debug print of all the values in the list - check conversion
    if DEBUG:
        print('Converted values:', capturedValues)

    # make sure input is within expected range, raise ValueError otherwise
    # minutes above 60
    if capturedValues[1] > 59 or capturedValues[4] > 59:
        raise ValueError(s.strip() + ' is not a valid input for conversion, minutes > 59.')
    # hours cant be 0
    if capturedValues[0] == 0 or capturedValues[3] == 0:
        raise ValueError(s.strip() + ' is not a valid input for conversion, hour == 0.')
    # hours cant be above 12
    if capturedValues[0] > 12 or capturedValues[3] > 12:
        raise ValueError(s.strip() + ' is not a valid input for conversion, hour > 12.')
    
    # convert FROM
    if capturedValues[2].lower() == 'am':
        if capturedValues[0] == 12:
            capturedValues[0] = 0        
    else:
        if capturedValues[0] != 12:
            capturedValues[0] += 12

     # convert TO
    if capturedValues[5].lower() == 'am':
        if capturedValues[3] == 12:
            capturedValues[3] = 0        
    else:
        if capturedValues[3] != 12:
            capturedValues[3] += 12

    # convert all integers back to strings with zero padding
    for i in range(len(capturedValues)):
        if isinstance(capturedValues[i], int):
            capturedValues[i] = f'{capturedValues[i]:02d}'

    # optional debug print of all the values in the list - check conversion
    if DEBUG:
        print('Converted values:', capturedValues)

    # return formatted string
    return f'{capturedValues[0]}:{capturedValues[1]} to {capturedValues[3]}:{capturedValues[4]}'


if __name__ == "__main__":
    main()
