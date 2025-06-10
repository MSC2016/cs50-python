def main():
    # list of months in year
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
        
    # start the user input loop
    while True:
        # get  the user input
        user_input = input("Date: ")
        try:
            # pass the user input and month list to the format_date function
            result = format_date(user_input, months)
            # variable that string to print
            output = ''
            # concatenate year, month and day to output, followed by '-', its easy to add now
            for item in result:
                output += item + '-'
            # remove the extra '-' that is added to the output
            output = output[:-1]
            # print the resulting string
            print(output)
            # exit the program
            return
        except Exception:
            # if there is any other exception, ask the user for another date
            continue


# parse the user input, check for errors, and format it
def format_date(date, calendar_months):
    # variable set to handle edge cases
    comma_in_date = False
    if ',' in date:
        comma_in_date = True
        # remove all comas
        while ',' in date:
            date = date.replace(',', '') 
    # split the date by '/'
    split_date = date.split('/')
    dashSeparator = True
    # if it doesnt result in three items split by spaces
    if len(split_date) != 3:
        split_date = date.split(' ')
        dashSeparator = False
    # if it doesnt result in three items raise value error
    if len(split_date) != 3:
        raise Exception("Can not split date, format is wrong")
    # if month is in the calendar, convert it to number
    for i in range(len(calendar_months)):
        if split_date[0].lower() == calendar_months[i].lower():
            split_date[0] = str(i+1)
            # format check, reject result in edge cases
            if dashSeparator or not comma_in_date:
                raise ValueError("Wrong Format, month in list and dash separator")
    # convert mm dd and yyyy to numeric values
    for i in range(3):
        try:
            # try conversion to ingeger 
            split_date[i] = int(split_date[i])
        except:
            # raise exception if input can not be converted to integer
            raise Exception("Date format is wrong, can not convert to number")
        # raise exception if input value is zero or negative
        if split_date[i] <= 0:
            raise Exception("Date format is wrong, number is zero or negative")
    # aditional checks
    if split_date[0] > 12:
        raise Exception("Month can not be more than 12")
    if split_date[1] > 31:
        raise Exception("Day can not be more tha 31")
    if split_date[2] > 9999:
        raise Exception("Year can not have mora than 4 digits")
    # convert values to string and padding with zeros
    split_date[0] = str(split_date[0]).zfill(2)
    split_date[1] = str(split_date[1]).zfill(2)
    split_date[2] = str(split_date[2]).zfill(4)
    # change order from MM,DD,YYYY to YYYY,MM,DD and return
    return [split_date[2], split_date[0], split_date[1]]
    

main()
