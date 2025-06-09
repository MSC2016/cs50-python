def main():
    dollars = dollars_to_float(input("How much was the meal? "))
    percent = percent_to_float(input("What percentage would you like to tip? "))
    tip = dollars * percent
    print(f"Leave ${tip:.2f}")


def dollars_to_float(d):
    # parse the string and convert it to float
    result = float(d.strip().replace(" ", "").replace("$", "").replace("€", ""))
    # return result
    return result


def percent_to_float(p):
    # parse the string and convert it to float
    result = float(p.strip().replace(" ", "").replace("%", ""))
    # divide by 100 to get something to multiply with the amount
    result = result/100
    # return result
    return result


main()