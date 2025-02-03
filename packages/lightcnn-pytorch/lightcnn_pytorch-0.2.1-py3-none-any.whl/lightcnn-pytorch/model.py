import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from scipy.spatial.distance import cosine
from .preprocessing import preprocess_face
from typing import Union, Tuple
import os


class mfm(nn.Module):
    """Max-Feature-Map activation"""

    def __init__(
        self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, type=1
    ):
        super(mfm, self).__init__()
        self.out_channels = out_channels
        if type == 1:
            self.filter = nn.Conv2d(
                in_channels,
                2 * out_channels,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding,
            )
        else:
            self.filter = nn.Linear(in_channels, 2 * out_channels)

    def forward(self, x):
        x = self.filter(x)
        out = torch.split(x, self.out_channels, 1)
        return torch.max(out[0], out[1])


class resblock_v1(nn.Module):
    """Residual block with MFM activation"""

    def __init__(self, in_channels, out_channels):
        super(resblock_v1, self).__init__()
        self.conv1 = mfm(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.conv2 = mfm(out_channels, out_channels, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        res = x
        out = self.conv1(x)
        out = self.conv2(out)
        out = out + res
        return out


class network(nn.Module):
    """LightCNN network architecture"""

    def __init__(self, block, layers):
        super(network, self).__init__()
        self.conv1 = mfm(3, 48, 3, 1, 1)

        self.block1 = self._make_layer(block, layers[0], 48, 48)
        self.conv2 = mfm(48, 96, 3, 1, 1)
        self.block2 = self._make_layer(block, layers[1], 96, 96)
        self.conv3 = mfm(96, 192, 3, 1, 1)
        self.block3 = self._make_layer(block, layers[2], 192, 192)
        self.conv4 = mfm(192, 128, 3, 1, 1)
        self.block4 = self._make_layer(block, layers[3], 128, 128)
        self.conv5 = mfm(128, 128, 3, 1, 1)

        self.fc = nn.Linear(8 * 8 * 128, 256)
        nn.init.normal_(self.fc.weight, std=0.001)

    def _make_layer(self, block, num_blocks, in_channels, out_channels):
        layers = []
        for i in range(0, num_blocks):
            layers.append(block(in_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = F.max_pool2d(x, 2) + F.avg_pool2d(x, 2)

        x = self.block1(x)
        x = self.conv2(x)
        x = F.max_pool2d(x, 2) + F.avg_pool2d(x, 2)

        x = self.block2(x)
        x = self.conv3(x)
        x = F.max_pool2d(x, 2) + F.avg_pool2d(x, 2)

        x = self.block3(x)
        x = self.conv4(x)
        x = self.block4(x)
        x = self.conv5(x)
        x = F.max_pool2d(x, 2) + F.avg_pool2d(x, 2)

        x = torch.flatten(x, 1)
        fc = self.fc(x)

        return fc


class LightCNN:
    def __init__(self, device: str = None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.model = self._load_model()
        self.model.eval()
        self.model.to(self.device)

    def _load_model(self):
        model = network(resblock_v1, [1, 2, 3, 4])
        weights_path = os.path.join(
            os.path.dirname(__file__), "weights", "LightCNN-V4_checkpoint.pth.tar"
        )
        checkpoint = torch.load(weights_path, map_location=self.device)
        new_state_dict = {
            k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items()
        }
        model.load_state_dict(new_state_dict)
        return model

    def get_features(self, image: Union[str, np.ndarray]) -> np.ndarray:
        """Extract features from a face image"""
        # Preprocess image
        processed_img = preprocess_face(image)
        if processed_img is None:
            raise ValueError("No face detected in the image")

        # Convert to tensor
        img_tensor = torch.from_numpy(processed_img).unsqueeze(0).to(self.device)

        # Extract features
        with torch.no_grad():
            features = self.model(img_tensor)
            features = F.normalize(features, p=2, dim=1)

        return features.cpu().numpy().flatten()

    def verify(
        self, image1: Union[str, np.ndarray], image2: Union[str, np.ndarray]
    ) -> Tuple[float, bool]:
        """Verify if two face images belong to the same person"""
        feat1 = self.get_features(image1)
        feat2 = self.get_features(image2)

        similarity = 1 - cosine(feat1, feat2)
        is_same = similarity > 0.5

        return similarity, is_same


# Create singleton instance
_model = None


def get_model(device: str = None) -> LightCNN:
    global _model
    if _model is None:
        _model = LightCNN(device)
    return _model


def verify(
    image1: Union[str, np.ndarray], image2: Union[str, np.ndarray]
) -> Tuple[float, bool]:
    """Convenience function for face verification"""
    model = get_model()
    return model.verify(image1, image2)


def get_features(image: Union[str, np.ndarray]) -> np.ndarray:
    """Convenience function for feature extraction"""
    model = get_model()
    return model.get_features(image)
