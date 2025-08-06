# Agents/crop_alert.py

import os
import pandas as pd
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Initial static data
initial_data = [
    {"crop": "wheat", "disease": "rust", "location": "udaipur", "report_date": "2025-07-31"},
    {"crop": "rice", "disease": "false smut", "location": "jaipur", "report_date": "2025-07-30"},
]

# In-memory user reports
user_reports = []

def get_combined_dataframe():
    return pd.concat([pd.DataFrame(initial_data), pd.DataFrame(user_reports)], ignore_index=True)

def check_disease_alert(crop, location, is_alert, disease_name=None, date=None):
    try:
        if is_alert:
            prompt = f"""
You are an agricultural assistant. please note the alert for the farmer.
- A recent crop disease alert has been reported.
- give the response for crop disease and solution what to do.
- Write a serious but helpful message for the farmer.
- Encourage them to inspect the field or consult experts.
- Provide clear and actionable advice.
- Mention the crop disease name and its symptoms.
- give the solution for the crop disease.
- Keep it concise and informative.
- Suggest medicines/pesticides.
- First in English, then in Hindi.

Do not give response in report format, just write a message.

Remark - Always first explain in English, then explain in Hindi.
"""
        elif not is_alert:
            prompt = f"""
You are an agricultural assistant. please note the alert for the farmer.
- No recent crop disease alerts have been reported.
- Write a cheerful and motivating message for the farmer.
- Encourage them to use our app..
- First in English, then in Hindi.

Do not give response in report format, just write a message.
Remark - Always first explain in English, then explain in Hindi.    
"""    
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini Error: {e}"

def collect_user_report(crop, disease, location):
    today = datetime.today().strftime("%Y-%m-%d")
    user_reports.append({
        "crop": crop.lower(),
        "disease": disease.lower(),
        "location": location.lower(),
        "report_date": today
    })
    gemini_msg = check_disease_alert(crop, location, True, disease, today)
    return gemini_msg

