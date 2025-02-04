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
        "LightCNN_29Layers_V2_checkpoint.pth.tar": "https://drive.google.com/uc?id=1rADnLoPAUeCKrUhYlMUajDyXSn_EI0eZ&confirm=t"
    }

    for filename, url in files.items():
        filepath = os.path.join(weights_dir, filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            try:
                gdown.download(url, filepath, quiet=False, fuzzy=True)
                
                # Verify file is not HTML/error page
                with open(filepath, 'rb') as f:
                    first_bytes = f.read(10)
                    if b'<!DOCTYPE' in first_bytes or b'<html' in first_bytes:
                        print(f"Invalid file downloaded for {filename}, removing...")
                        os.remove(filepath)
                        raise RuntimeError(f"Failed to download {filename}")
                        
                print(f"Downloaded {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise

    return weights_dir
