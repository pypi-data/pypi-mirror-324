from PIL import Image

def read_image(path):
    return Image.open(path)

def save_image(image, path):
    image.save(path)