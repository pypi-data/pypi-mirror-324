from PIL import Image

def show(image, size=None, title="Image"):
    """
    Display an image with optional resizing and title.

    :param image: PIL Image object
    :param size: Tuple (width, height) to resize the image before showing
    :param title: Title of the window
    """
    if size:
        image = image.resize(size)

    # Set the title for the image window (works on Windows & some Linux environments)
    try:
        image.show(title=title)
    except TypeError:  # Pillow < 9.1.0 does not support `title`
        print(f"Showing image: {title}")
        image.show()