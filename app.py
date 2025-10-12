import streamlit as st
import numpy as np
import cv2

st.title("✅ EcoSentinel Setup Successful!")

st.write("Congratulations! Your environment is working correctly.")
st.write("All libraries are installed.")

# Just a small test to see if libraries are usable
try:
    st.write(f"Streamlit version: {st.__version__}")
    st.write(f"NumPy version: {np.__version__}")
    st.write(f"OpenCV version: {cv2.__version__}")
    st.success("Test Passed! You are ready for the hackathon.")
except Exception as e:
    st.error(f"Something went wrong: {e}")