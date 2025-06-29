import sys

from PIL import Image
from PIL import ImageOps


def main():

    # name of the shirt file
    shirt = 'shirt.png'

    # get the arguments and assign them to origin and destination variables
    origin, destination = get_args()

    shirt_data = None
    origin_data = None
    destination_data = None

    try:
        # opening all as file, because it simplifies
        # throwing file not found error.
        with Image.open (shirt) as file:
            shirt_data = file.copy()
            
        # open original image and assign data to origin_data
        with Image.open (origin) as file:   
            origin_data = file.copy()

        # assign the modiffied image to destination_data
        destination_data = overlay_shirt(shirt_data, origin_data)
        # save to hdd
        destination_data.save(destination)


    # if origin file doesnt exist exit with error code 1
    except FileNotFoundError as file:
        print(f'Could not read {file.filename}')
        sys.exit(1)

def overlay_shirt(shirt_img, original_img):
    '''
    Receives two PIL images as parameters and returns the shirt image,
    overlayed onto the original image.
    '''
    # resize original image
    original_img = ImageOps.fit(original_img, shirt_img.size)

    # paste the shirt onto the original image
    original_img.paste(shirt_img, mask = shirt_img)

    return  original_img


def get_args():
    '''
    Ensure only 2 arguments were passed and exit with code 1 
    and error message, in case the argument count is wrong, or
    file extentions are different.

    '''
    # return error and exit if the user entered too many arguments
    if len(sys.argv) > 3:
        print('Too many command-line arguments')
        sys.exit(1)

    # return error and exit if the user entered too few arguments
    if len(sys.argv) < 3:
        print('Too few command-line arguments')
        sys.exit(1)

    # get original picture filename and extension
    origin = sys.argv[1]
    split_origin = origin.split('.')

    # get destination picture filename and extension
    destination = sys.argv[2]
    split_destination = destination.split('.')

    # compare input and output file extension and exit with error if they are different
    if split_origin[-1] != split_destination[-1]:
        print('Input and output have different extensions')
        sys.exit(1)

    # return the params - filenames
    return origin, destination


# call the main function, only when the script is executed, not when its imported
if __name__ == '__main__':
    main()

