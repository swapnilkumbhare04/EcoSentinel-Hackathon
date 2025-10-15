# config.py

import os
from ultralytics.utils import ASSETS # Ultralytics' utility to find default files

# --- 1. Model Configuration ---
# Path to the YOLOv8 model file (.pt)
# Tumhi 'models/' folder madhye thevla ahe, mhanun ha path:
MODEL_PATH = os.path.join("models", "best.pt") 
# Note: For hackathon, if using YOLO default, ASSETS / 'yolov8n.pt' might also work

# --- 2. Data Paths ---
VIDEO_SAVE_PATH = "temp_video.mp4" 
SAMPLE_VIDEO_PATH = os.path.join("sample_data", "sample_video.mp4")

# --- 3. Thresholds and Settings ---
CONFIDENCE_THRESHOLD = 0.50 # Detection sathi minimum confidence
PREDICTION_STEPS = 5        # Pudhche kiti steps predict karayche

SMOOTHING_WINDOW_SIZE = 5

# --- 4. Geofence Coordinates (M3 will use this) ---
# Example: Simple 4-point rectangle area
# (x, y) coordinates for the safety zone (normalized to 0-1000 for simplicity initially)
# Note: These need to be scaled to actual video resolution later.
GEOFENCE_COORDS = [
    (200, 300),
    (700, 300),
    (700, 600),
    (200, 600)
]
# # --- 5. Wildlife Filtering ---
# # COCO dataset classes to ignore (Person is ID 0)
# IGNORED_CLASSES = [0] 

# # COCO dataset classes considered as potential wildlife threats.
# # Adjust these based on your model's classification output for better accuracy.
# # (e.g., Cat=15, Dog=16, Horse=17, Sheep=18, Cow=19, Elephant/Bear are often customized)
# # For YOLOv8n (COCO), use:
# TARGET_WILDLIFE_CLASSES = [15, 16, 17, 18, 19, 20, 21] 
# # (These IDs map to common large objects like Cat, Dog, Horse, Cow, Bear, Elephant/Giraffe etc. which can represent a threat)

# config.py (M2/M4 ne change karaycha)
# --- 5. Wildlife Filtering ---
IGNORED_CLASSES = []  # No one to ignore, as only tiger is detected
TARGET_WILDLIFE_CLASSES = [0] # Only the 'tiger' class ID (ID is 0 in this new model)
