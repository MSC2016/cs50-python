def main():
    # get user input
    user_input = input("camelCase: ")

    # create variable to hold the result
    snake_case = ""

    # iterate trough every character the user input
    for i in range(0, len(user_input)):

        # character is uppercase
        if user_input[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            # after the first letter add the underscore and the lowercase letter
            if i > 0:
                snake_case = snake_case + "_" + user_input[i].lower() 

            # at index zero, just make the letter lowercase, we dont want underscores here
            else:
                snake_case = snake_case + user_input[i].lower()

        # if the character is lowercase just add it as is
        else:
            snake_case = snake_case + user_input[i]

    # print the snake_case version
    print("snake_case:", snake_case)


main()