# src/visualizer.py
import cv2
import numpy as np # Moved to the top for clean code
from config import GEOFENCE_COORDS

def draw_all_elements(frame, detections, predicted_path, is_threat):
    """
    Draws all visual elements onto the frame: detection boxes, geofence,
    predicted path, and an alert message.
    """
    # 1. Draw the Geofence
    # Convert list of tuples to a NumPy array for drawing
    pts = np.array(GEOFENCE_COORDS, np.int32)
    # Reshape is necessary for cv2.polylines
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 255), thickness=2) # Yellow color

    # 2. Draw Detection Boxes
    for detection in detections:
        x1, y1, x2, y2 = detection['coords']
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # Green color
        
        # Optional: Display Class Name and Confidence
        class_name = detection.get('class', 'Animal')
        conf = detection.get('confidence', 0.0)
        label = f"{class_name}: {conf:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    # 3. Draw Predicted Path 
    if predicted_path and len(predicted_path) > 1:
        # Draw the path connecting all predicted points
        for i in range(len(predicted_path) - 1):
            p1 = predicted_path[i]
            p2 = predicted_path[i+1]
            # Draw line segments
            cv2.line(frame, p1, p2, (255, 0, 0), 2) # Blue color
            # Draw circles at prediction steps (optional)
            cv2.circle(frame, p2, 3, (0, 0, 255), -1) # Red dot for next step

    # 4. Draw an Alert Banner if there is a threat
    if is_threat:
        cv2.putText(
            frame, 
            "!!! PRAHAR PURV SUCHANA: THREAT ALERT !!!", 
            (20, 50), # Changed position slightly
            cv2.FONT_HERSHEY_SIMPLEX, 
            1.2, # Slightly smaller font
            (0, 0, 255), # Red color
            3
        )

    return frame