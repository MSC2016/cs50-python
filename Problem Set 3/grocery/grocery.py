def main():
    # dictionary that holds the grocery list
    groceries = {}
    # user input loop
    while True:
        try:
            # get the user input
            user_input = input()
            # if item already exists, update quantity
            if user_input in groceries:
                groceries[user_input] += 1
            # if its a new item add it to the grocery list
            else:
                groceries[user_input] = 1
        # if user is finished
        except EOFError:
            print("")
            # sort the dictionary by key
            groceries = dict(sorted(groceries.items()))
            # iteratr trough all items in dictionary, getting key and value
            for k, v in groceries.items():
                # print value and uppercase key
                print(v, k.upper())
            # ends the program
            return 


# call main function
main()