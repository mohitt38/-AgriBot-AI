# pages/2_🤝_Market_Broker_Agent.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from Agents.market_broker import get_market_broker_response

st.set_page_config(page_title="🤝 Market Broker Agent", layout="centered")

st.title("🤝 Market Broker Agent")

st.markdown("""
Help farmers discover the **Best platforms or Buyers** to sell their crops based on location and crop type.
""")

with st.form("market_form"):
    crop = st.text_input("🌾 Enter Crop Name", placeholder="e.g., Wheat, Onion")
    location = st.text_input("📍 Enter Location (City, District)", placeholder="e.g., Indore, Madhya Pradesh")
    quantity = st.text_input("📦 Enter Quantity (Optional)", placeholder="e.g., 100 kg")

    submitted = st.form_submit_button("Get Market Suggestions")

if submitted:
    with st.spinner("Fetching market insights..."):
        try:
            response = get_market_broker_response(crop, location, quantity)
            st.subheader("📢 Suggested Market Options")
            st.markdown(response)
        except Exception as e:
            st.error(f"❌ Failed to get suggestions: {e}")
