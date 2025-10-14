# src/visualizer.py

import cv2
import numpy as np
from config import GEOFENCE_COORDS

def draw_all_elements(frame, detections, predicted_path, is_threat):
    """
    Draws all visual elements onto the frame: detection boxes, geofence,
    predicted path, and an alert message.
    """
    
    # Define colors based on Threat Status
    GEOFENCE_COLOR = (0, 0, 255) if is_threat else (0, 255, 255) # Red if threat, Yellow if safe (BGR format)

    # 1. Draw the Geofence (Color is now dynamic)
    pts = np.array(GEOFENCE_COORDS, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=GEOFENCE_COLOR, thickness=3) # Thickness increased to 3

    # 2. Draw Detection Boxes
    for detection in detections:
        x1, y1, x2, y2 = detection['coords']
        BOX_COLOR = (0, 0, 255) if is_threat else (0, 255, 0) # Red box if threat
        cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
        
        # Display Class Name and Confidence
        class_name = detection.get('class', 'Animal')
        conf = detection.get('confidence', 0.0)
        label = f"{class_name.upper()} {conf:.2f}" # ALL CAPS for clarity
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, BOX_COLOR, 2)


    # 3. Draw Predicted Path 
    # Path color should be the same as Geofence color for consistency
    PATH_COLOR = GEOFENCE_COLOR
    if predicted_path and len(predicted_path) > 1:
        for i in range(len(predicted_path) - 1):
            p1 = predicted_path[i]
            p2 = predicted_path[i+1]
            cv2.line(frame, p1, p2, PATH_COLOR, 2)
            cv2.circle(frame, p2, 4, PATH_COLOR, -1) # Circle is slightly bigger for visibility

    # 4. Draw Alert Text (This is the final text on the frame)
    if is_threat:
        cv2.putText(
            frame, 
            "!!! PRAHAR PURV SUCHANA: THREAT ALERT !!!", 
            (20, 30), # Varti thevle
            cv2.FONT_HERSHEY_DUPLEX, # Thoda bold font
            1.0, 
            (0, 0, 255), # Red color
            2
        )
    else:
         cv2.putText(
            frame, 
            "STATUS: Safe Zone Monitoring", 
            (20, 30), 
            cv2.FONT_HERSHEY_DUPLEX, 
            1.0, 
            (0, 255, 0), # Green color
            2
        )


    return frame