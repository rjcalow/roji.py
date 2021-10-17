import PIL
from PIL import Image
import shutil
import pathlib

def IMG_process(width, source, path_to_save):
    path_to_save = pathlib.Path(path_to_save)
    if path_to_save.exists():
        return

    img = Image.open(source)
    if img.width > width and source.suffix != ".gif":
        wpercent = (width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((width, hsize), PIL.Image.ANTIALIAS)
        img.save(str(path_to_save),optimize=True, quality = 60)
        
    elif  (source.stat().st_size / 1024) > 200: 
        wpercent = (width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((width, hsize), PIL.Image.ANTIALIAS)
        img.save(str(path_to_save),optimize=True, quality = 50)

    else:
        shutil.copy(str(source), str(path_to_save))