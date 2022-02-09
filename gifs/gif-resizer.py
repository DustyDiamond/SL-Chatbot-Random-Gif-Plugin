import os, sys
from PIL import Image

basewidth = 800
root = os.path.dirname(__file__)


def resize(name):
    img = Image.open(name) 
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(name)

for path, subdirs, files in os.walk(root):
    for name in files:
        if name == "blank.gif" or name == "blank-backup.gif" or name == "gif-resizer.py":
            continue

        file = os.path.join(path, name)
        resize(file)
        print(file)
