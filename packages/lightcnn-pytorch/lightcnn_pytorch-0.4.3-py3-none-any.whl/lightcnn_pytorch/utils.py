import os
import gdown
from tqdm import tqdm

WEIGHT_URLS = {
    "shape_predictor_68_face_landmarks.dat": "https://drive.google.com/uc?id=17gmEzXQKU7Ushl2lw0JQ4nuDXCf43ME4",
    "LightCNN-V4_checkpoint.pth.tar": "https://drive.google.com/uc?id=1rLFXCIz3Mg-8zLnwa7X2_3u10Nolwgbo",
    "LightCNN_29Layers_V2_checkpoint.pth.tar": "https://drive.google.com/uc?id=1rADnLoPAUeCKrUhYlMUajDyXSn_EI0eZ&confirm=t"
}

def download_weights():
    """Download model weights if not present"""
    weights_dir = os.path.join(os.path.dirname(__file__), "weights")
    os.makedirs(weights_dir, exist_ok=True)

    for filename, url in WEIGHT_URLS.items():
        weight_path = os.path.join(weights_dir, filename)
        if not os.path.exists(weight_path):
            print(f"Downloading {filename}...")
            gdown.download(url, weight_path, quiet=False)

    return weights_dir
