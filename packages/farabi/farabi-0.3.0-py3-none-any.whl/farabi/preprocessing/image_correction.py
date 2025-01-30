from PIL import Image
import numpy as np

def gamma_correction(image, gamma=1.0):
    # Convert image to numpy array
    img_array = np.array(image).astype(np.float32) / 255.0  # Normalize to [0,1]

    # Apply gamma correction
    img_corrected = np.power(img_array, gamma) * 255.0  # Scale back to [0,255]

    # Convert back to uint8 and PIL image
    img_corrected = np.clip(img_corrected, 0, 255).astype(np.uint8)
    return Image.fromarray(img_corrected)
