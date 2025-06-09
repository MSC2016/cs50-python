def main():

    # get the user input
    user_input = input("Input: ")

    # list of characters to remove
    vowels = 'aeiou'

    # for every character in vowels, remove it from the user input
    for i in range(0, len(vowels)):
        user_input = user_input.replace(vowels[i], "")
        user_input = user_input.replace(vowels[i].upper(), "")
    
    # print tweet ready version of the user input
    print(user_input)


main()
