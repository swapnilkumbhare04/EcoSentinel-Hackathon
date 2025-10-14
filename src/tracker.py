# src/tracker.py

from config import PREDICTION_STEPS
import numpy as np

# This dictionary stores the history of each tracked animal's center point.
# Format: { track_id: [(x1, y1), (x2, y2), ...] }
track_history = {}

def update_track(detections):
    """
    Updates the track history with the latest center point detection.
    """
    if detections:
        # Simple tracking: Use the first detected object (ID 0)
        track_id = 0 
        center_point = detections[0]['center']
        
        if track_id not in track_history:
            track_history[track_id] = []
        
        # Add the new center point to the history
        track_history[track_id].append(center_point)
        
        # Keep the history from getting too long (last 20 positions are enough)
        if len(track_history[track_id]) > 20: 
            track_history[track_id].pop(0)

def predict_future_path(track_id=0):
    """
    Predicts the future path based on simple linear velocity derived from the last two points.
    """
    history = track_history.get(track_id, [])
    predicted_path = []
    
    # Needs at least 2 points to calculate velocity
    if len(history) < 2:
        return []

    # Get the last two known points
    p1 = np.array(history[-2])
    p2 = np.array(history[-1])
    
    # Calculate the velocity vector
    velocity_vector = p2 - p1
    
    current_point = p2
    
    # Predict PREDICTION_STEPS number of points (from config)
    for _ in range(PREDICTION_STEPS):
        # Predict the next point based on constant velocity
        next_point = current_point + velocity_vector
        
        # Add the new point (must be tuple of integers for OpenCV drawing)
        predicted_path.append( (int(next_point[0]), int(next_point[1])) )
        
        # Update current_point for the next iteration
        current_point = next_point
        
    # print(f"Predicted path of length: {len(predicted_path)}") # Debugging check
    return predicted_path

# --- Quick Test Section ---
if __name__ == '__main__':
    # Temporary fix for module not found error during standalone testing
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    print("Testing Tracker Module...")
    
    # Simulate movement
    detections_frame1 = [{'center': (100, 100)}]
    detections_frame2 = [{'center': (105, 105)}]
    detections_frame3 = [{'center': (110, 110)}]
    
    update_track(detections_frame1)
    update_track(detections_frame2)
    update_track(detections_frame3)
    
    path = predict_future_path()
    print(f"Predicted Path: {path}") 
    # Expected: [(115, 115), (120, 120), (125, 125), (130, 130), (135, 135)] (if PREDICTION_STEPS=5)