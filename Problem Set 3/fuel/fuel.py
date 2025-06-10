def main():
    # start a loop
    while True:
        try:
            # get the user input
            user_input = input('Fraction: ')
            # split it int a and b
            a, b = user_input.split('/')
            # convert a and b to integers
            a = int(a)
            b = int(b)
            # calculate the tank level percentage
            r = round(a/b*100)
            # match r agains possible results
            # prompt user if r is negative
            if r < 0:
                continue
            # prompt user if r ia above 100
            elif r > 100:
                continue
            # print F if tank is above 95%
            elif r > 95:
                print('F')
                return
            # print E if tank is bellow 5%
            elif r < 5:
                print('E')
                return
            # print percentage if r is between 5 and 95%
            else:
                print(f'{r:g}%')
                return
        # As specified, every error should make us promp the user again
        # so i will just use general exception go back to the begining 
        except Exception:
            continue


# call main function
main()
