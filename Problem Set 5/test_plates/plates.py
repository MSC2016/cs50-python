def main():

    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    
    # return false if length is out of spec
    if len(s) > 6 or len(s) < 2:
        return False
    
    # return false if the first two character are not letters
    if not (s[0].isalpha() and s[1].isalpha()):
        return False
    
    # variable to store if a number was found
    found_number = False

    # iterate trough every character in the string
    for i in range(0, len(s)):

        # return false if any of the characters is not a letter or a number
        if not (s[i].isalpha() or s[i].isdigit()):
            return False
        
        # return false if a number was previously found, and current character is a letter
        if found_number and s[i].isalpha():
            return False
        
        # set the found_number flag to true, when the first digit is found
        if not found_number:
            found_number = s[i].isdigit()

            # return false if the first number we found is a zero
            if found_number and s[i] == '0':
                return False

    # return true, if no problems were detected in the for loop
    return True


if __name__ == "__main__":
    main()
