# pages/3_🧬_Crop_Disease_Detector.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from PIL import Image
from Agents.crop_disease_detector import analyze_crop_image

st.set_page_config(page_title="🧬 Crop Disease Detector", layout="centered")

# Streamlit UI
st.set_page_config(page_title="🧬 Gemini Disease Detector", layout="centered")
st.title("🧬 Crop Disease Detector (Gemini Vision)")

st.markdown("Upload a leaf image to detect any signs of disease or pest using **Gemini AI** (multi-modal model).")

uploaded_file = st.file_uploader("📤 Upload Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing image with Gemini..."):
        result = analyze_crop_image(uploaded_file)
        st.subheader("📋Diagnosis Result")
        st.markdown(result)
