import cv2
import numpy as np
from mtcnn import MTCNN
from typing import Union, Optional

def preprocess_face(image: Union[str, np.ndarray]) -> Optional[np.ndarray]:
    """Preprocess face image for LightCNN"""
    # Initialize MTCNN
    detector = MTCNN()
    
    # Load image if path is provided
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise ValueError("Could not load image")
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detect face
    results = detector.detect_faces(image_rgb)
    if not results:
        return None
        
    # Get the first face
    face = results[0]
    
    # Get facial landmarks
    left_eye = face["keypoints"]["left_eye"]
    right_eye = face["keypoints"]["right_eye"]
    
    # Align face
    angle = np.degrees(np.arctan2(right_eye[1] - left_eye[1], 
                                 right_eye[0] - left_eye[0]))
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    aligned = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
    
    # Crop face
    x, y, w, h = face["box"]
    face_crop = aligned[y:y+h, x:x+w]
    
    # Resize to 128x128
    face_resized = cv2.resize(face_crop, (128, 128))
    
    # Normalize
    face_normalized = face_resized.astype(np.float32) / 255.0
    
    # Convert to torch format (C, H, W)
    face_chw = np.transpose(face_normalized, (2, 0, 1))
    
    return face_chw