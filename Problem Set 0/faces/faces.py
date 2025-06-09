# define main function
def main():
    # get user input
    message = input("")
    
    # call convert and assign result to output
    output = convert(message)

    # print output
    print(output)

# define convert functionm
def convert(str):
    # replace text and return it
    return str.replace(":)","🙂").replace(":(","🙁")

# call main function
main()