import re

# set to true to get debug prints
DEBUG = False


def main():
    print(validate(input("IPv4 Address: ")))
    

def validate(ip):
    '''
    Get ip and return True if it is a valid ip address,
    otherwise return False
    '''
    # pattern string, accepts 4 sets of one to three digits separated by '.'
    # using ^ and $ to force match to the begining and end of the string
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

    # run the search and assign the result to matches
    matches = re.search(pattern, ip)

    # try/catch block, if there is an exception return false
    try:
        for group in matches.groups():
            if DEBUG:
                print(group)
            # return false if any of the groups starts with '0' or '00'
            if len(group) > 1 and (group.startswith('0') or group.startswith('00')):
                return False
            # return false if any of the integer converted groups is larger than 255
            if int(group) > 255:
                return False
    except Exception as e:
        if DEBUG:
            print(e)
        # returns false if any exception occurs, most likely: 'NoneType' object has no attribute 'groups'
        # meaning input didnt match the pattern, there are no matches therefor matches is of type None, 
        # and has no attribute named groups, making it fail to start the for loop
        return False
    # if nothing failed so far, returns true, input must be a valid ip address
    return True


if __name__ == "__main__":
    main()