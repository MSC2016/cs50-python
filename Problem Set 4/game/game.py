import random


def main():
    # get a user input and assign it to level
    level = get_user_input('Level: ')
    # get a random number between 0 and level
    number = random.randint(0, level)
    # set the initial value of the guess to -1, 
    guess = -1
    # loop until the user guesses the number
    while guess != number:
        # get the user guess
        guess = get_user_input('Guess: ')
        # if the guess is smaller print too small
        if guess < number:
            print('Too small!')
        # if the guess is larger print too large
        elif guess > number:
            print('Too large!')
    # otherwise, print just right and exit
    print('Just right!')

    
def get_user_input(s='') -> int:
    '''
    Get an input from a user, 
    if a value for s is given, 
    it should be the prompt.
    '''
    # loop forever
    while True:
        # try catch block
        try:
            # get an input from the user and convert to int
            user_input = int(input(s))
            # raise an exception if input is zero or less, forcing a reprompt
            if user_input <= 1:
                raise Exception
            # if successfull, return it
            return user_input
        # catch all, and retry
        except:
            pass


if __name__ == '__main__':
    main()