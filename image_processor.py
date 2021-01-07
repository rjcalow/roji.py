import PIL.Image
from exif import Image

def resize(img, img_out, width):
    img = PIL.Image.open(img) 
    wpercent = (width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((width,hsize), PIL.Image.ANTIALIAS)
    img.save(img_out)

def wipe_exif(img):
    with open(img, 'rb') as image_file:
        my_image = Image(image_file)
    
    if my_image.has_exif: 
        my_image.delete_all()

        with open(img, 'wb') as new_image_file:
            new_image_file.write(my_image.get_file())

def readexif(img): #testing
    with open(img, 'rb') as image_file:
        my_image = Image(image_file)
    dir(my_image)
