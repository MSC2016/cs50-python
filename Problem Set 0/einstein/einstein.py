# define main function
def main():
    # set the conversion factor
    CONST_CONV_FACTOR = int(90000000000000000)
    # get the user input and assign it to mass
    mass = int(input("m: "))
    # multiply and print
    print("E:",CONST_CONV_FACTOR * mass)

# call main function
main()
