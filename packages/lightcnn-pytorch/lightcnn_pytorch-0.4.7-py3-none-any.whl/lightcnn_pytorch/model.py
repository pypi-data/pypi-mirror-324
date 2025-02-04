import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import cv2
from scipy.spatial.distance import cosine
from typing import Union, Tuple, Literal
import os
from .preprocessing import preprocess_image, get_face_landmarks, align_face
from .architectures import LightCNN_V4, LightCNN_29Layers_v2, resblock
from .utils import download_weights

ModelType = Literal["LightCNN-V4", "LightCNN_29Layers_V2"]

class LightCNN:
    def __init__(self, model_name: ModelType = "LightCNN-V4", device: str = None):
        self.model_name = model_name
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        download_weights()
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
                new_state_dict = {k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items() if "fc2" not in k}
                model.load_state_dict(new_state_dict, strict=False)
            else:
                raise ValueError("Invalid checkpoint format")
        except Exception as e:
            print(f"Error loading weights: {e}")
            raise

        return model

    def get_features(self, image: Union[str, np.ndarray], align: bool = True) -> np.ndarray:
        """Extract features from a face image"""
        if isinstance(image, str):
            image = cv2.imread(image)
            if image is None:
                raise ValueError("Could not load image")

        if align:
            landmarks = get_face_landmarks(image)
            if landmarks is None:
                raise ValueError("No face detected")
            image = align_face(image, landmarks)

        img_tensor = preprocess_image(image, self.model_name)
        img_tensor = img_tensor.to(self.device)

        with torch.no_grad():
            features = self.model(img_tensor)
            
            # Handle tuple output from 29Layers model
            if isinstance(features, tuple):
                features = features[0]  # Take first element (embeddings)
            
            features = F.normalize(features, p=2, dim=1)

        return features.cpu().numpy().flatten()

    def verify(
        self,
        image1: Union[str, np.ndarray],
        image2: Union[str, np.ndarray],
        align: bool = True,
    ) -> Tuple[float, bool]:
        """Verify if two face images belong to the same person"""
        feat1 = self.get_features(image1, align=align)
        feat2 = self.get_features(image2, align=align)
        
        similarity = 1 - cosine(feat1, feat2)
        is_same = similarity > 0.5
        
        return similarity, is_same

# Global model cache
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
