# pages/4_⚠️_Crop_Alert_Agent.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from datetime import datetime
from orchestrator import run_orchestrator

st.set_page_config(page_title="🌾 Smart Crop Alert System", layout="centered")

st.title("🚨 Autonomous Crop Disease Alert System")

# User input
st.markdown("### 📋 Report Crop Issue or Check Alerts")
crop = st.text_input("🌾 Enter crop name:")
location = st.text_input("📍 Enter your location (village/city):")
image = st.file_uploader("🖼️ Upload a crop leaf image (JPEG/PNG)", type=["jpg", "jpeg", "png"])
submit = st.button("🚀 Submit & Diagnose")

if submit:
    if not all([crop, location, image]):
        st.error("⚠️ Please fill in all fields and upload an image.")
    else:
        try:
            # Save uploaded image temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(image.read())
                image_path = tmp.name

            st.info("🧠 Running Autonomous Diagnosis and Alert Agent...")

            # Run orchestrator logic
            result = run_orchestrator(crop=crop, location=location, image_path=image_path)

            st.success("✅ Process Complete!")
            st.markdown("### 🤖 Gemini's Advice:")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ Orchestrator Error: {e}")
