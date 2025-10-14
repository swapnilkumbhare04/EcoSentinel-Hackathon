# app.py

# --- 1. Imports ---
import streamlit as st
import tempfile
import os # Best practice to import, though not used yet

# --- 2. Page Configuration (Set this at the very top) ---
# This sets the page to a wide layout for better video display
st.set_page_config(layout="wide")

# --- 3. UI Header ---
st.title("🐯 Prahar Purv Suchana (The Pre-Attack Alert)")
st.subheader("Leveraging AI to Reduce Human-Wildlife Conflict")

# --- 4. Video Uploader Widget ---
# This part is always visible on the screen
uploaded_video = st.file_uploader(
    "Upload a video of wildlife movement near conflict zones (MP4 recommended):",
    type=["mp4", "mov", "avi"]
)

# --- 5. Main Logic Block ---
# This entire block will ONLY run AFTER a user has uploaded a video.
# This prevents all NameError issues.
if uploaded_video is not None:
    
    # --- Step A: Read and Save the Uploaded Video ---
    video_bytes = uploaded_video.read()
    
    # Create a temporary file on the disk to store the video
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_bytes)
    video_path = tfile.name  # This path will be used by Member 4 (Integrator)
    
    st.success("Video uploaded successfully! Starting analysis...")
    
    # --- Step B: Create the Two-Column Layout ---
    # This layout will show the original video and the analyzed video side-by-side
    col1, col2 = st.columns(2)
    
    # --- Step C: Display the Original Video in the First Column ---
    with col1:
         st.markdown("##### Original Video Feed")
         st.video(video_bytes) # Now this will work because video_bytes is defined
    
    # --- Step D: Create a Placeholder for the Analyzed Video in the Second Column ---
    with col2:
         st.markdown("##### Live Analysis (Predicted Path)")
         # This is an empty box that we will fill with processed frames later
         analysis_placeholder = st.empty()
         
    # --- Step E: Placeholder for the Processing Loop ---
    # Member 4 (Integrator) will add the main video processing code here.
    # The code will:
    # 1. Read the video from `video_path`.
    # 2. Loop through each frame.
    # 3. Call the detector, tracker, and visualizer.
    # 4. Update the `analysis_placeholder` with the new, annotated frame.
    
    st.info("Processing loop will be integrated here by Member 4.")