# importing inflect
import inflect


def main():
    # initialize inflect engine and assign it to ie
    ie = inflect.engine()
    # variable to store the list of names to print
    names = []
    # try catch block to capture EOF
    try:
        # while loop to get Inputs
        while True:
            # get one name
            name = input('Name: ') 
            # add the name to names list
            names.append(name)
    # when EOF is captured
    except EOFError:
        # variable to hold the final sentence plus the joined list of names
        sentence = 'Adieu, adieu, to ' + ie.join(names)
        # print the result
        print(sentence)


if __name__ == '__main__':
    main()