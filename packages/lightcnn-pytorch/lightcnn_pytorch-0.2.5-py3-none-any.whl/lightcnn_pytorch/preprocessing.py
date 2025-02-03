import cv2
import dlib
import numpy as np
from typing import Union, Optional, Tuple

# Initialize dlib's face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("weights/shape_predictor_68_face_landmarks.dat")


def get_face_landmarks(image: np.ndarray) -> Optional[dlib.full_object_detection]:
    """Detect face and get landmarks"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if not faces:
        return None
    return predictor(gray, faces[0])


def align_face(image: np.ndarray, landmarks: dlib.full_object_detection) -> np.ndarray:
    """Align face using eye landmarks"""
    left_eye = np.mean(
        [
            (landmarks.part(36).x, landmarks.part(36).y),
            (landmarks.part(37).x, landmarks.part(37).y),
            (landmarks.part(38).x, landmarks.part(38).y),
            (landmarks.part(39).x, landmarks.part(39).y),
            (landmarks.part(40).x, landmarks.part(40).y),
            (landmarks.part(41).x, landmarks.part(41).y),
        ],
        axis=0,
    )

    right_eye = np.mean(
        [
            (landmarks.part(42).x, landmarks.part(42).y),
            (landmarks.part(43).x, landmarks.part(43).y),
            (landmarks.part(44).x, landmarks.part(44).y),
            (landmarks.part(45).x, landmarks.part(45).y),
            (landmarks.part(46).x, landmarks.part(46).y),
            (landmarks.part(47).x, landmarks.part(47).y),
        ],
        axis=0,
    )

    # Calculate angle
    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle = np.degrees(np.arctan2(dy, dx))

    # Rotate image
    center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    aligned = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return aligned


def crop_face(image: np.ndarray, landmarks: dlib.full_object_detection) -> np.ndarray:
    """Crop face using landmarks"""
    x = [landmarks.part(i).x for i in range(68)]
    y = [landmarks.part(i).y for i in range(68)]

    x1, y1 = int(min(x)), int(min(y))
    x2, y2 = int(max(x)), int(max(y))

    # Add padding
    padding = 30
    h, w = image.shape[:2]
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(w, x2 + padding)
    y2 = min(h, y2 + padding)

    return image[y1:y2, x1:x2]


def preprocess_face(
    image: Union[str, np.ndarray], align: bool = True
) -> Optional[np.ndarray]:
    """Preprocess face image for LightCNN"""
    # Load image if path is provided
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise ValueError("Could not load image")

    # Get landmarks
    landmarks = get_face_landmarks(image)
    if landmarks is None:
        return None

    if align:
        # Align face
        image = align_face(image, landmarks)

    # Crop face
    face_crop = crop_face(image, landmarks)

    # Resize to 128x128
    face_resized = cv2.resize(face_crop, (128, 128))

    # Normalize
    face_normalized = face_resized.astype(np.float32) / 255.0

    # Convert to torch format (C, H, W)
    face_chw = np.transpose(face_normalized, (2, 0, 1))

    return face_chw
