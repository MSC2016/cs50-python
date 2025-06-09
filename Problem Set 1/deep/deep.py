def main():
    # get the user input
    user_input = input("What is the Answer to the Great Question of Life, the Universe, and Everything? ")

    # parse the user input
    user_input = user_input.strip().replace(" ","").replace("-","").lower()

    # create a list of aceptable answers, formatted as they should to make a good comparison
    aceptable_answers = ["fortytwo","42"]

    # print Yes or No, depending on user input
    if user_input in aceptable_answers:
        print("Yes")
    else:
        print("No")

main()