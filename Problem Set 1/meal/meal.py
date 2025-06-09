def main():
    # get user input
    time_as_float = convert(input("What time is it? "))
    
    # check if its breakfast time
    if time_as_float >= 7 and time_as_float <= 8:
        print("breakfast time")

    # check if its lunch time
    if time_as_float >= 12 and time_as_float <= 13:
        print("lunch time")

    # check if its dinner time
    if time_as_float >= 18 and time_as_float <= 19:
        print("dinner time")


def convert(time):
    # remove spaces and dots
    time = time.strip().replace(" ", "").replace(".", "")

    # check if 12 hour format is being used and pm
    is_pm = time.endswith("pm")

    # check if 12 hour format is being used and am
    is_am = time.endswith("am")

    # remove am and pm from the string, if they exist
    time = time.replace("am", "").replace("pm", "")

    # assign hours to h and minutes to m
    h, m = time.split(":")

    # convert h and m to floats
    h = float(h)
    m = float(m)

    if m > 60:
        raise Exception("minutes > 60")

    # translate minutes to decimal units
    m = m / 60

    # small input protection
    if is_am or is_pm and h < 13:

        # make 12 am midnight, or 0 hours
        if h == 12 and is_am:
            h = 0
        
        # subtract 12 hours if is_pm
        if h < 12 and is_pm:
            h += 12
        
    # return hours + minutes to get time in decimal format
    return float(h) + float(m)


if __name__ == "__main__":
    main()
