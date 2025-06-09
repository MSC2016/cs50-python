def main():
    # set the price
    price = 50

    # accepted coins
    accepted_coins = [25, 10, 5]

    # store amount paid
    paid = 0

    # get user input
    print("Amount Due: 50")

    # while the machine still wants more money
    while paid < price:

        # get the coin value from the user
        coin = int(input("Insert Coin: "))
        
        # if the coin is valid, add its value to paid amount
        if coin in accepted_coins:
            paid += coin
        
        # tell the user how mutch he owes
        if price - paid > 0:
            print("Amount Due:", price - paid)
        
    # print change
    print("Change Owed:", paid - price)


# call the main function
main()
