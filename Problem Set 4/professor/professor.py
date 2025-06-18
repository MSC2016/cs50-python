import random


def main():
    # keep track of the score
    score = 0
    # get the level from the user
    level = get_level()
    # generate the problem list
    problems = generate_problem(level)
    # loop trough each problem
    for problem in problems:
        # set the number of tries
        tries_left = 3
        # mark the problem as unsolved
        solved = False
        # unpack the tuple
        x, y = problem
        # loop until problem is solved, or there are no tries left
        while not solved:
            # decrement the counter
            tries_left -= 1
            # get the user input
            user_input = get_user_input(f'{x} + {y} = ')
            # if the answer is correct
            # mark the problem as solved and update score
            if user_input == x + y:
                solved = True
                score += 1
            else:
                # otherwise print EEE
                print('EEE')
            # if the user cant figure it out after tries limit is reached
            if tries_left < 1:
                # give him the solution
                print(f'{x} + {y} = {x + y}')
                # mark as solved and move on, without updating the score
                solved = True
    # print the score before exiting
    print(f'Score: {score}')


def generate_problem(level):
    '''
    returns a list of tuples with values
    acording to the selected difficulty
    '''
    # initialize an empty list
    problem_list = []
    # while loop to generate 10 different problems
    while len(problem_list) < 10:
        # create one tuple
        problem = (generate_integer(level), generate_integer(level))
        # check if no equal tuples exist in the list
        # i dont care if the same values apear in different order
        if problem not in problem_list:
            # add problem to the list
            problem_list.append(problem)
    # return the list
    return problem_list


def get_level() -> int:
    '''
    prompts the user for a number between
    one and three, and returns the value
    '''
    # get a user input to select the level
    return get_user_input('Level: ', True)


def generate_integer(level) -> int:
    '''
    Gets a level as input and returns a random
    integer between 0 and x digits level
    '''
    # if level 1 returns random integer between 0 and 9
    if level == 1:
        return random.randint(0, 9)
    # otherwise return number between 10 to the power of (level -1)  
    # and 10 to the power of level -1 
    else:
        return random.randint(10**(level - 1), 10**level - 1)


def get_user_input(s='', get_level=False) -> int:
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
            # handle special case get_level
            if get_level:
                # ensure value is in range 1..3
                if user_input <= 0 or user_input > 3:
                    raise ValueError
                # reprompt if level input is negative
                if user_input <= 0:
                    raise Exception
            # if successfull, return it
            return user_input
        # catch all, and retry
        except:
            # print EEE if there is a problem converting the answer to int
            if not get_level:
                print('EEE')


if __name__ == '__main__':
    main()