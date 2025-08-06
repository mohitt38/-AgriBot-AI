# Crop_Advisor.py
import sys
import os
sys.path.append(os.path.abspath(".."))

import streamlit as st
from Agents.crop_advisor import get_crop_advice

st.set_page_config(page_title="🌾 Crop Advisor", layout="centered")

st.title("🌱 Crop Advisor Agent")
st.markdown("Get the best crops to grow based on your **soil type** and **local weather** (auto-fetched).")

# Input fields
soil = st.text_input("🧪 Enter Soil Type", placeholder="e.g. Red, Black, etc.")
location = st.text_input("📍 Enter Your City / Region Name", placeholder="e.g Udaipur, Ahemdabad, Surat ,etc.")

# Button to generate advice
if st.button("🌾 Suggest Best Crops"):
    if soil and location:
        with st.spinner("🤖 Fetching weather and generating crop suggestions..."):
            try:
                advice, weather_info = get_crop_advice(soil, location)  # ⬅️ updated
                st.info(f"📊 **Weather Info for {location}:**\n\n{weather_info}")  # ⬅️ show weather
                st.markdown(advice, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Failed to generate advice: {e}")
    else:
        st.warning("⚠️ Please fill in both Soil Type and Location fields.")
