import cv2
import numpy as np
from facenet_pytorch import MTCNN  # Changed import
from typing import Union, Optional


def preprocess_face(image: Union[str, np.ndarray]) -> Optional[np.ndarray]:
    """Preprocess face image for LightCNN"""
    # Initialize MTCNN
    detector = MTCNN(keep_all=False)

    # Load image if path is provided
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise ValueError("Could not load image")

    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect face
    boxes, probs = detector.detect(image_rgb)

    if boxes is None or len(boxes) == 0:
        return None

    # Get the first face
    box = boxes[0]
    x, y, x2, y2 = [int(b) for b in box]

    # Crop face
    face_crop = image[y:y2, x:x2]

    # Resize to 128x128
    face_resized = cv2.resize(face_crop, (128, 128))

    # Normalize
    face_normalized = face_resized.astype(np.float32) / 255.0

    # Convert to torch format (C, H, W)
    face_chw = np.transpose(face_normalized, (2, 0, 1))

    return face_chw
