import re

def main():
    print(parse(input("HTML: ")))


def parse(s):
    # pattern to search
    pattern = r'^<iframe .*src="https?://(?:www.)?youtube\.com/embed/(.{11}).+</iframe>$'

    # run the search and assign the result to matches
    matches = re.search(pattern, s, re.IGNORECASE)
    # if there is a match, concatenate the url and return it
    if matches:
        return 'https://youtu.be/' + matches.group(1)
    # return 'None' if no match was found
    return 'None'


if __name__ == "__main__":
    main()