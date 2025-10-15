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

from config import PREDICTION_STEPS, SMOOTHING_WINDOW_SIZE
import numpy as np
# ... (track_history and update_track are the same) ...

def predict_future_path(track_id=0):
    """
    Predicts the future path using the average velocity over the last N points (Smoothing).
    """
    history = track_history.get(track_id, [])
    predicted_path = []
    
    # --- FIX: Prediction should only start if there are enough points ---
    # At least 2 points are needed for ANY prediction
    if len(history) < 2:
        return []

    # 1. Determine points for smoothing (Use the available history, or the window size)
    # This ensures we use all available points if history is smaller than the window
    n_points = min(len(history), SMOOTHING_WINDOW_SIZE)
    smooth_points = np.array(history[-n_points:]) 

    # 2. Calculate Average Velocity
    delta_points = smooth_points[1:] - smooth_points[:-1]
    
    # Calculate the AVERAGE velocity vector
    average_velocity_vector = np.mean(delta_points, axis=0)
    
    # If the average velocity is nearly zero (animal stopped), stop prediction
    if np.linalg.norm(average_velocity_vector) < 1.0: 
        return []

    # 3. Linear Prediction 
    current_point = np.array(history[-1])
    
    # Predict PREDICTION_STEPS number of points
    for _ in range(PREDICTION_STEPS):
        next_point = current_point + average_velocity_vector
        
        # Add the new point (must be tuple of integers for OpenCV drawing)
        predicted_path.append( (int(next_point[0]), int(next_point[1])) )
        
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