# app.py

# --- 1. Imports (All imports should be at the top) ---
import streamlit as st
import cv2
import tempfile
import os

# Import our custom modules
from src.detector import detect_animals
from src.tracker import update_track, predict_future_path
from src.geofence import create_geofence, is_inside_geofence
from src.visualizer import draw_all_elements

# --- 2. Initialize Session State (NEW - for permanent alert flag) ---
# Check if the threat status is already defined
if 'threat_status' not in st.session_state:
    st.session_state.threat_status = False

# --- 3. Page Configuration ---
st.set_page_config(layout="wide")

# --- 4. UI Header ---
st.title("🐯 Prahar Purv Suchana (The Pre-Attack Alert)")
st.subheader("Leveraging AI to Reduce Human-Wildlife Conflict")

# --- 5. Real-time Alert Banner (NEW) ---
# This banner will persist even if the frame changes
if st.session_state.threat_status:
    st.error("🚨 THREAT IMMINENT! WILDLIFE DETECTED CROSSING SAFETY PERIMETER. 🚨")
else:
    st.success("STATUS: Safe. No immediate threat detected.")

# --- 6. Video Uploader Widget ---
uploaded_video = st.file_uploader(
    "Upload a video of wildlife movement near conflict zones (MP4 recommended):",
    type=["mp4", "mov", "avi"]
)

# --- 7. Main Logic Block ---
if uploaded_video is not None:
    
    # --- Reset threat status when a new video is uploaded ---
    st.session_state.threat_status = False
    
    # --- Step A: Save the Uploaded Video to a Temporary File ---
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_video.read())
    video_path = tfile.name
    
    st.info("Video uploaded successfully! Starting analysis...") # Changed success to info

    # --- Step B: Create the Two-Column Layout ---
    col1, col2 = st.columns(2)
    
    # [Rest of UI setup is the same]
    with col1:
         st.markdown("##### Original Video Feed")
         st.video(uploaded_video)
    
    with col2:
         st.markdown("##### Live Analysis (Predicted Path)")
         analysis_placeholder = st.empty()
         
    # --- Step C: Video Processing Loop ---
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Error: Could not open the video file.")
    else:
        create_geofence()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                # After video finishes, keep the final threat status
                break

            # 1. DETECTION
            detections = detect_animals(frame)
            
            # 2. TRACKING
            update_track(detections)
            predicted_path = predict_future_path()
            
            # 3. GEOFENCE ANALYSIS
            is_threat = False # Check threat status for THIS frame
            if predicted_path and detections: # Check if we are actively tracking something
                last_predicted_point = predicted_path[-1]
                if is_inside_geofence(last_predicted_point):
                     is_threat = True
            
            # --- UPDATE GLOBAL THREAT STATE (NEW) ---
            if is_threat:
                 st.session_state.threat_status = True # Set permanent alert
                 
            # 4. VISUALIZATION: Pass the current threat status to the visualizer
            annotated_frame = draw_all_elements(frame, detections, predicted_path, st.session_state.threat_status)
            
            # 5. DISPLAY THE RESULT
            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            analysis_placeholder.image(frame_rgb, channels="RGB")

        # --- Step D: Cleanup ---
        cap.release()
        tfile.close()
        os.unlink(tfile.name)
        # Force a refresh to show the final alert status
        st.rerun()