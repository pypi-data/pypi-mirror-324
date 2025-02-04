import os
import gdown
from tqdm import tqdm


def download_weights():
    """Download model weights if not present"""
    weights_dir = os.path.join(os.path.dirname(__file__), "weights")
    os.makedirs(weights_dir, exist_ok=True)

    files = {
        "shape_predictor_68_face_landmarks.dat": "https://drive.google.com/uc?id=17gmEzXQKU7Ushl2lw0JQ4nuDXCf43ME4",
        "LightCNN-V4_checkpoint.pth.tar": "https://drive.google.com/uc?id=1rLFXCIz3Mg-8zLnwa7X2_3u10Nolwgbo",
        "LightCNN_29Layers_V2_checkpoint.pth.tar": "https://drive.google.com/uc?id=1rADnLoPAUeCKrUhYlMUajDyXSn_EI0eZ"
    }

    for filename, url in files.items():
        filepath = os.path.join(weights_dir, filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            try:
                # First try with newer gdown version
                gdown.download(url, filepath, quiet=False)
            except TypeError:
                # Fallback for older gdown versions
                gdown.download(url, filepath)
            print(f"Downloaded {filename}")

    return weights_dir
