# src/geofence.py

from shapely.geometry import Polygon, Point
from config import GEOFENCE_COORDS

# Global variable to hold our geofence polygon object
geofence_polygon = None

def create_geofence():
    """
    Creates a Shapely Polygon object from the coordinates defined in config.py.
    This function is called once at the start of the application.
    """
    global geofence_polygon
    if geofence_polygon is None:
        try:
            # GEOFENCE_COORDS comes from config.py
            geofence_polygon = Polygon(GEOFENCE_COORDS)
            print("Geofence polygon created successfully.")
        except Exception as e:
            print(f"Error creating geofence polygon: {e}")
            geofence_polygon = False
    return geofence_polygon

def is_inside_geofence(point_coords):
    """
    Checks if a given point (e.g., predicted animal location) is inside the geofence.
    
    Args:
        point_coords (tuple): A tuple (x, y) representing the point's coordinates.
        
    Returns:
        bool: True if the point is inside the geofence, False otherwise.
    """
    # Ensure the geofence is created before checking
    fence = create_geofence()
    if not fence:
        # If fence creation failed, assume unsafe or return failure
        return False 

    # Create a Shapely Point object
    point = Point(point_coords)
    
    # Use Shapely's built-in 'contains' method to check
    return fence.contains(point)


# --- Quick Test Section (Cleaned up) ---
if __name__ == '__main__':
    # Temporary fix for module not found error during standalone testing
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    print("Testing Geofence Module...")
    create_geofence()
    
    test_point_inside = (500, 500)
    print(f"Is {test_point_inside} inside? -> {is_inside_geofence(test_point_inside)}") 
    
    test_point_outside = (50, 50)
    print(f"Is {test_point_outside} inside? -> {is_inside_geofence(test_point_outside)}")