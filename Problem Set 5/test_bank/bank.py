def main():
    # get the user input
    user_input = input("Greeting: ")
    # print the result
    print(f'${value(user_input)}')


def value(greeting) -> int:
    # if user input starts with hello print $0
    if greeting.strip().lower().startswith("hello"):
        return 0
    # if user input starts with h print $20
    elif greeting.strip().lower().startswith("h"):
        return 20
    # if none of the above print $100
    else:
        return 100


if __name__ == "__main__":
    main()
