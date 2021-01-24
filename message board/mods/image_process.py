from io import BytesIO
from PIL import Image
from random import randint


def verify():
    verify_len = 6
    text = ""
    for i in range(verify_len):
        text += str(randint(0, 9))
    return text


def check_file(filename):
    file_exts = {'jpg', 'jpeg', "jfif", "png", "gif", "webp"}
    if filename and "." in filename:
        if filename.split(".")[-1].lower() in file_exts:
            return True
    else:
        return False


def get_file_ext(filename):
    ext = filename.split(".")[-1].upper()
    if ext == ("JPG" or "JFIF"):
        ext = "JPEG"
    return ext


def make_timg(file, type):  # make thumbnail
    image_size = [(1000, 1000), (300, 300)]
    buf = BytesIO()
    im = Image.open(file)
    if type == "image":
        im.thumbnail(image_size[0])
    if type == "timg":
        im.thumbnail(image_size[1])
    im.save(buf, get_file_ext(file.filename))
    return buf
