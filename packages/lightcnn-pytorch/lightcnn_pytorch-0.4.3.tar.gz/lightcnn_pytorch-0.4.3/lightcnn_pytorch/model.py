import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from scipy.spatial.distance import cosine
from .preprocessing import preprocess_face
from typing import Union, Tuple, Literal
import os
from .utils import download_weights
from .architectures import LightCNN_V4, LightCNN_29Layers_v2

ModelType = Literal["LightCNN-V4", "LightCNN_29Layers_V2"]

class LightCNN:
    def __init__(self, model_name: ModelType = "LightCNN-V4", device: str = None):
        self.model_name = model_name
        download_weights()
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.model = self._load_model()
        self.model.eval()
        self.model.to(self.device)

    def _load_model(self):
        if self.model_name == "LightCNN-V4":
            model = LightCNN_V4()
            weights_file = "LightCNN-V4_checkpoint.pth.tar"
        else:  # LightCNN_29Layers_V2
            model = LightCNN_29Layers_v2()
            weights_file = "LightCNN_29Layers_V2_checkpoint.pth.tar"
        
        weights_path = os.path.join(
            os.path.dirname(__file__), 
            "weights", 
            weights_file
        )
        
        try:
            checkpoint = torch.load(weights_path, map_location=self.device)
            if "state_dict" in checkpoint:
                new_state_dict = {k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items()}
                if self.model_name == "LightCNN_29Layers_V2":
                    new_state_dict = {k: v for k, v in new_state_dict.items() if "fc2" not in k}
                model.load_state_dict(new_state_dict, strict=False)
            else:
                raise ValueError("Invalid checkpoint format")
        except Exception as e:
            print(f"Error loading weights: {e}")
            if os.path.exists(weights_path):
                os.remove(weights_path)
            download_weights()
            checkpoint = torch.load(weights_path, map_location=self.device)
            if "state_dict" in checkpoint:
                new_state_dict = {k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items()}
                if self.model_name == "LightCNN_29Layers_V2":
                    new_state_dict = {k: v for k, v in new_state_dict.items() if "fc2" not in k}
                model.load_state_dict(new_state_dict, strict=False)
            else:
                raise ValueError("Invalid checkpoint format")
        
        return model

    def get_features(self, image: Union[str, np.ndarray], align: bool = True) -> np.ndarray:
        processed_img = preprocess_face(image, align=align, model_name=self.model_name)
        if processed_img is None:
            raise ValueError("No face detected in the image")

        img_tensor = torch.from_numpy(processed_img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            if self.model_name == "LightCNN_29Layers_V2":
                _, features = self.model(img_tensor)
            else:
                features = self.model(img_tensor)
            features = F.normalize(features, p=2, dim=1)

        return features.cpu().numpy().flatten()

    def verify(self, image1: Union[str, np.ndarray], image2: Union[str, np.ndarray], align: bool = True) -> Tuple[float, bool]:
        feat1 = self.get_features(image1, align)
        feat2 = self.get_features(image2, align)
        similarity = 1 - cosine(feat1, feat2)
        return similarity, similarity > 0.5

_models = {}

def get_model(model_name: ModelType = "LightCNN-V4", device: str = None) -> LightCNN:
    global _models
    key = f"{model_name}_{device}"
    if key not in _models:
        _models[key] = LightCNN(model_name=model_name, device=device)
    return _models[key]

def verify(
    image1: Union[str, np.ndarray], 
    image2: Union[str, np.ndarray], 
    model_name: ModelType = "LightCNN-V4",
    align: bool = True
) -> Tuple[float, bool]:
    model = get_model(model_name)
    return model.verify(image1, image2, align=align)

def get_features(
    image: Union[str, np.ndarray], 
    model_name: ModelType = "LightCNN-V4",
    align: bool = True
) -> np.ndarray:
    model = get_model(model_name)
    return model.get_features(image, align=align)
