import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Load an image, convert it to grayscale, and resize it.
    """
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (224, 224))  # Resize for EfficientNet
        img = np.stack((img,)*3, axis=-1) # EfficientNet expects 3 channels
        img = img.astype('float32') / 255.0
        return img
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None