import emoji


# define main function
def main():
    # get the user input
    user_input = input("Input: ")
    # emojize and print output
    print("Output:", emoji.emojize(user_input, language="alias"))


if __name__ == "__main__":
    main()
