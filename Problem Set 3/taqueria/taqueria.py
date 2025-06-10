def main():
    # felipe's menu
    menu = {
            "Baja Taco": 4.25,
            "Burrito": 7.50,
            "Bowl": 8.50,
            "Nachos": 11.00,
            "Quesadilla": 8.50,
            "Super Burrito": 8.50,
            "Super Quesadilla": 9.50,
            "Taco": 3.00,
            "Tortilla Salad": 8.00
            }
    
    # total price
    total = 0.
    # input loop
    while True:
        try:
            # get user input
            item = input('Item: ').lower().title()
            # if the item exists in the menu
            if item in menu:
                # add its value to the total
                total += float(menu[item])
                # print the total
                print(f'Total: ${total:.2f}')

        # runs if the user pressed ctrl+D
        except EOFError:
            # prints an empty line
            print()
            # ends the program
            return
        # if the item is not in the menu
        except KeyError:
            # get another user input
            continue


main()