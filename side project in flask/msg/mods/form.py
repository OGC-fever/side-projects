from io import BytesIO
from PIL import Image
from random import randint


def dummy_msg():
    char = list(set(range(0x3105, 0x3129)))
    msg = ''
    for i in range(randint(10, 50)):
        msg += chr(char[randint(0, len(char) - 1)])
    return msg


def check_file(filename):
    file_exts = ('jpg', 'jpeg', "jfif", "png", "gif", "webp")
    if filename and "." in filename:
        if filename.split(".")[-1].lower() in file_exts:
            return True
    else:
        return False


def get_file_ext(filename):
    ext = filename.split(".")[-1].upper()
    if ext in ("JPG", "JFIF"):
        ext = "JPEG"
    return ext


def resize_img(file, type):  # make thumbnail
    im_resize = [(1000, 1000), (400, 400)]
    buf = BytesIO()
    im = Image.open(file)
    if type == "image":
        im.thumbnail(im_resize[0])
    if type == "timg":
        im.thumbnail(im_resize[1])
    im.save(buf, get_file_ext(file.filename))
    return buf
