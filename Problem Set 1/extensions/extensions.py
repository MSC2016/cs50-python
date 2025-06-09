def main():
    # get the user input
    user_input = input("File name: ")

    # parse the user input
    user_input = user_input.strip().lower()
    # split the string by "."
    split_str = user_input.split('.')
    # get the last item
    extension = split_str[-1]

    # create a dictionary with the required values
    ext_dict = {
        "gif" : "image/gif",
        "jpg" : "image/jpeg",
        "jpeg": "image/jpeg",
        "png" : "image/png",
        "pdf" : "application/pdf",
        "txt" : "text/plain",
        "zip" : "application/zip"
    }

    # if extension exists in dictionary, print its value
    if extension in ext_dict:
        print(ext_dict[extension])
    # if none of the above, print the default value
    else:
        print("application/octet-stream")

main()
