from PIL import Image
import numpy as np

def logarithmic_transform(image, c=1):
    # Convert image to numpy array
    image_array = np.array(image, dtype=np.float32)
    
    # Normalize the input image to the range [0, 1]
    image_normalized = image_array / 255.0
    
    # Apply logarithmic transformation
    transformed_array = c * np.log1p(image_normalized)
    
    # Normalize the output to the range [0, 255]
    transformed_array = 255 * (transformed_array / np.max(transformed_array))
    
    # Convert to uint8
    transformed_array = np.uint8(transformed_array)
    
    # Convert back to PIL Image
    return Image.fromarray(transformed_array)


def exponential_transform(image, c=1):
    # Convert image to numpy array
    image_array = np.array(image, dtype=np.float32)
    
    # Normalize the input image to the range [0, 1]
    image_normalized = image_array / 255.0
    
    # Apply exponential transformation
    transformed_array = c * (np.exp(image_normalized) - 1)
    
    # Normalize the output to the range [0, 255]
    transformed_array = 255 * (transformed_array / np.max(transformed_array))
    
    # Convert to uint8
    transformed_array = np.uint8(transformed_array)
    
    # Convert back to PIL Image
    return Image.fromarray(transformed_array)