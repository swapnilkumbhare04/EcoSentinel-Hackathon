# src/detector.py

from ultralytics import YOLO
import cv2
import numpy as np
from config import (
    MODEL_PATH, 
    CONFIDENCE_THRESHOLD,
    IGNORED_CLASSES, 
    TARGET_WILDLIFE_CLASSES 
)

# Global Variable for the model instance (Only load once)
yolo_model = None

def load_model():
    """Loads the YOLO model from the path specified in config.py."""
    global yolo_model
    if yolo_model is None:
        try:
            yolo_model = YOLO(MODEL_PATH)
            print(f"YOLO Model loaded successfully from: {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            yolo_model = False
    return yolo_model

def detect_animals(frame):
    """
    Processes a single video frame to detect wildlife and extract their coordinates.
    """
    model = load_model()
    if not model:
        return []

    # YOLO Inference: Use CONFIDENCE_THRESHOLD directly in the model call (efficient)
    # The results will ONLY contain objects above the defined threshold
    results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
    
    detections = []
    
    for r in results:
        boxes = r.boxes
        class_names = r.names 
        
        for box in boxes:
            
            x1, y1, x2, y2 = [int(x) for x in box.xyxy[0].tolist()]
            # Confidence is already above threshold, but we extract it for the dict
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = class_names[class_id]
            
            # --- IMPROVED FILTERING LOGIC ---
            
            is_ignored = class_id in IGNORED_CLASSES 
            is_target_wildlife = class_id in TARGET_WILDLIFE_CLASSES
            
            # Only track if the object is NOT ignored (e.g., human) AND IS a potential threat class
            if not is_ignored and is_target_wildlife:
                
                # Calculate the center point (Crucial for M3's tracking)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                
                detections.append({
                    'center': (center_x, center_y),
                    'coords': (x1, y1, x2, y2),
                    'class_id': class_id,
                    'class': class_name,
                    'confidence': confidence
                })

    return detections

# Run this section to test model loading
if __name__ == '__main__':
    # Ensure config.py is accessible for standalone testing
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    load_model()