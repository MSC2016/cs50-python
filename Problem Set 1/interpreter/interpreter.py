def main():
    # get the user input
    user_input = input("Expression: ")

    # parse the user input
    user_input = user_input.strip().split(' ')

    # assign user input to variables, converting values to float
    a = user_input[0]
    op = user_input[1]
    b = user_input[2]

    # call the do_math function 
    result = do_math(op, a, b)
    
    # print the result
    print(result)


def do_math(op, a, b):

    a = float(a)
    b = float(b)

    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '/':
        return a / b
    elif op == '*':
        return a * b
    else:
        raise Exception("Unknown operation")


main()
