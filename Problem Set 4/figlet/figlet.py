import sys
import pyfiglet
from random import choice


# define main function
def main():

    # get the font list
    fonts = pyfiglet.FigletFont.getFonts()

    # switch to adjust behaviour acording to argument's length
    match (len(sys.argv)):

        # no parameters - random font
        case 1:
            # select a random font
            font = choice(fonts)
            # get the input from the user
            user_input = get_user_input()
            # render the text
            text = pyfiglet.figlet_format(user_input, font=font)
            # print rendered text
            print(text)

        # user entered 2 parameters
        case 3:
            # check if first argument is -f or --font
            if sys.argv[1].lower() in ['-f', '--font']:
                # check if font exists
                if sys.argv[2].lower() in fonts:
                    # get the input from the user
                    user_input = get_user_input()
                    # render the text
                    text = pyfiglet.figlet_format(user_input, font=sys.argv[2])
                    # print rendered text
                    print(text)
                else:
                    # font not listed
                    terminate_program(3)
            else:
                # wrong first argument
                terminate_program(2)

        # catch all - exit if number of parameters is wrong
        case _:
            terminate_program(1)

# get user input
def get_user_input():
    inp = input('Input: ')
    return inp

# End the program with the specified error code
def terminate_program(n=0):
    print('Invalid usage')
    sys.exit(n)


if __name__ == '__main__':
    main()
