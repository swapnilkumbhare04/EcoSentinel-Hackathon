# src/tracker.py

from config import PREDICTION_STEPS, SMOOTHING_WINDOW_SIZE # <--- NAVIN IMPORT ADD KELA
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
    Predicts the future path using the average velocity over the last N points (Smoothing).
    """
    history = track_history.get(track_id, [])
    predicted_path = []
    
    # Needs at least 2 points to calculate velocity
    if len(history) < 2:
        return []

    # --- CORE REFINEMENT LOGIC (Smoothing) ---
    
    # 1. Get the points for smoothing (use last SMOOTHING_WINDOW_SIZE points)
    # The minimum of history size or the window size
    smooth_points = np.array(history[-SMOOTHING_WINDOW_SIZE:]) 

    # 2. Calculate Average Velocity
    if len(smooth_points) < 2:
        return [] # Safety check

    # Calculate difference between consecutive points (Delta_X, Delta_Y)
    delta_points = smooth_points[1:] - smooth_points[:-1]
    
    # Calculate the AVERAGE velocity vector from all delta points
    average_velocity_vector = np.mean(delta_points, axis=0)
    
    # If the average velocity is nearly zero (animal stopped), stop prediction
    if np.linalg.norm(average_velocity_vector) < 1.0: # 1.0 is a small threshold
        return []

    # 3. Linear Prediction (Starting from the very last known point)
    current_point = np.array(history[-1])
    
    # Predict PREDICTION_STEPS number of points
    for _ in range(PREDICTION_STEPS):
        # Predict the next point based on average velocity
        next_point = current_point + average_velocity_vector
        
        # Add the new point (must be tuple of integers for OpenCV drawing)
        predicted_path.append( (int(next_point[0]), int(next_point[1])) )
        
        # Update current_point for the next iteration
        current_point = next_point
        
    return predicted_path

# --- Quick Test Section ---
if __name__ == '_main': # <-- __name_ la main madhe badalle
    # Temporary fix for module not found error during standalone testing
    import sys
    import os
    # Assuming the config.py is in the parent directory
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    print("Testing Tracker Module with Smoothing...")
    
    # Simulate slightly noisy movement
    detections_frame1 = [{'center': (100, 100)}]
    detections_frame2 = [{'center': (105, 106)}]
    detections_frame3 = [{'center': (109, 111)}]
    detections_frame4 = [{'center': (115, 115)}]
    detections_frame5 = [{'center': (121, 120)}]
    
    update_track(detections_frame1)
    update_track(detections_frame2)
    update_track(detections_frame3)
    update_track(detections_frame4)
    update_track(detections_frame5)
    
    path = predict_future_path()
    print(f"Predicted Path (Smoothed): {path}")