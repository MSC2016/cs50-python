from PIL import Image
from PIL import ImageFilter

# import PILImage, this helps with intellisense and code hints
from PIL.Image import Image as PILImage 

def main():
    with Image.open('image1.jpg') as img:
        # tell python img is of type PILImage
        img: PILImage
        
        print(img.size)
        print(img.format)
        #img.filter(ImageFilter.BLUR)
        img.rotate(180)
        img.save('output.jpg')
        print(img.getexif())


if __name__ == "__main__":
    main()
