# app.py (Final Version with Professional UI)

# --- 1. Imports ---
import streamlit as st
import cv2
import tempfile
import os

# Import our custom modules
from src.detector import detect_animals
from src.tracker import update_track, predict_future_path
from src.geofence import create_geofence, is_inside_geofence
from src.visualizer import draw_all_elements

# --- 2. Page Configuration (Set this once at the top) ---
st.set_page_config(
    page_title="Prahar Purv Suchana | EcoSentinel",
    page_icon="🐅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. Sidebar ---
with st.sidebar:
    st.image("assets/logo.jpg", width=100) # Replace with your team logo if you have one
    st.title("🛡 EcoSentinel")
    st.markdown("---")
    st.header("About The Project")
    st.info(
        "Prahar Purv Suchana is an AI-powered early warning system designed to "
        "reduce human-wildlife conflict by predicting animal movement and alerting "
        "communities before a potential threat crosses safety boundaries."
    )
    st.markdown("---")
    st.header("👥 Team Members")
    st.write("Swapnil Kumbhare")
    st.write("Sanchi Borkar")
    st.write("Suyog Madavi")
    st.write("Sayukta Giradkar")

# --- 4. Main UI Header ---
st.title("Prahar Purv Suchana (The Pre-Attack Alert)")
st.caption("A project for the Innovating for Coexistence Hackathon")
st.markdown("---")

# --- 5. Video Uploader ---
uploaded_video = st.file_uploader(
    "Upload a video of wildlife movement:",
    type=["mp4", "mov", "avi"]
)

# --- 6. Main Logic Block ---
if uploaded_video is not None:
    
    # --- Step A: Save the Uploaded Video to a Temporary File ---
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_video.read())
    video_path = tfile.name
    
    # --- Step B: Create Placeholders for Dashboard and Video ---
    st.markdown("### 📊 Live Analysis Dashboard")
    
    # Create 3 columns for metrics
    kpi1, kpi2, kpi3 = st.columns(3)

    # Create placeholders for the metrics
    with kpi1:
        st.markdown("*System Status*")
        status_placeholder = st.empty()
    with kpi2:
        st.markdown("*Detected Object*")
        object_placeholder = st.empty()
    with kpi3:
        st.markdown("*Confidence Score*")
        confidence_placeholder = st.empty()
    
    st.markdown("---")
    
    # Create placeholders for video feeds
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 📸 Original Video Feed")
        st.video(uploaded_video)
    
    with col2:
        st.markdown("##### 🔬 AI Processed Feed")
        analysis_placeholder = st.empty()
         
    # --- Step C: Video Processing Loop ---
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Error: Could not open the video file.")
    else:
        # Get total frames for progress bar
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = 0
        progress_bar = st.progress(0, text="Analyzing video...")
        
        # Initialize the geofence
        create_geofence()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                progress_bar.progress(100, text="Analysis Complete!")
                break
            
            frame_count += 1

            # 1. DETECTION
            detections = detect_animals(frame)
            
            # 2. TRACKING
            update_track(detections)
            predicted_path = predict_future_path()
            
            # 3. GEOFENCE ANALYSIS
            is_threat = False
            if predicted_path and detections:
                last_predicted_point = predicted_path[-1]
                if is_inside_geofence(last_predicted_point):
                     is_threat = True

            # 4. VISUALIZATION
            annotated_frame = draw_all_elements(frame, detections, predicted_path, is_threat)
            
            # 5. DISPLAY THE RESULT
            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            analysis_placeholder.image(frame_rgb, channels="RGB")
            
            # --- Step D: Update Dashboard Metrics ---
            if is_threat:
                status_placeholder.error("🚨 THREAT DETECTED")
            else:
                status_placeholder.success("✅ SAFE")
            
            if detections:
                detected_class = detections[0].get('class', 'N/A').upper()
                confidence = detections[0].get('confidence', 0)
                object_placeholder.info(detected_class)
                confidence_placeholder.info(f"{confidence:.2f}")
            else:
                object_placeholder.write("---")
                confidence_placeholder.write("---")
                
            # Update Progress Bar
            progress_percent = int((frame_count / total_frames) * 100)
            progress_bar.progress(progress_percent, text=f"Analyzing... {progress_percent}%")

        # --- Step E: Cleanup ---
        cap.release()
        tfile.close()
        os.unlink(tfile.name)