from PIL import Image
import numpy as np

def gamma_encoding(image, gamma=1.0):
    # Convert image to numpy array
    img_array = np.array(image).astype(np.float32) / 255.0  # Normalize to [0,1]

    # Apply gamma correction
    img_corrected = np.power(img_array, gamma) * 255.0  # Scale back to [0,255]

    # Convert back to uint8 and PIL image
    img_corrected = np.clip(img_corrected, 0, 255).astype(np.uint8)
    return Image.fromarray(img_corrected)



def gamma_decoding(image,gamma=1.0):
    # Convert image to numpy array
    img_array = np.array(image).astype(np.float32) / 255.0  # Normalize to [0,1]
    if(gamma==0):
        raise ValueError("Gamma must be greater than 0 to avoid division by zero.")
    # Apply gamma correction
    img_corrected = np.power(img_array, 1/gamma) * 255.0  # Scale back to [0,255]

    # Convert back to uint8 and PIL image
    img_corrected = np.clip(img_corrected, 0, 255).astype(np.uint8)
    return Image.fromarray(img_corrected)