def main():
    # get the user input
    user_input = input("Greeting: ")

    # parse the user input
    user_input = user_input.strip().replace(" ", "").lower()

    # if user input starts with hello print $0
    if "hello" in user_input[:5]:
        print("$0")
    # if user input starts with h print $20
    elif "h" in user_input[:1]:
        print("$20")
    # i fnone of the above print $100
    else:
        print("$100")


main()
