def main():

    # get the user input
    user_input = input("Input: ")
    print(shorten(user_input))


def shorten(word):
    # list of characters to remove
    vowels = 'aeiou'
    # for every character in vowels, remove it from the user input
    for i in range(0, len(vowels)):
        word = word.replace(vowels[i].lower(), "")
        word = word.replace(vowels[i].upper(), "")
    
    # print tweet ready version of the user input
    return word


if __name__ == '__main__':
    main()
