# crop_advisor.py

import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Get weather info from WeatherAPI.com
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "days": 1,
        "aqi": "no",
        "alerts": "no"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        forecast = data["forecast"]["forecastday"][0]
        date = forecast["date"]
        day = forecast["day"]
        condition = day["condition"]["text"]
        max_temp = day["maxtemp_c"]
        min_temp = day["mintemp_c"]
        rain_chance = day.get("daily_chance_of_rain", "N/A")
        rain_expected = day.get("daily_will_it_rain", "N/A")

        print(f"Weather in {city} on {date}: {condition}, Max Temp: {max_temp}°C, Min Temp: {min_temp}°C, Rain Chance: {rain_chance}%, Rain Expected: {rain_expected}%")


        return f"Date: {date}, {condition},Max Temp: {max_temp}°C, Min Temp: {min_temp}°C,Rain Chance: {rain_chance}%, Rain Expected: {rain_expected}%, condition: {condition}"

    except Exception as e:
        print("❌ Weather API error:", e)
        return "Unknown weather"

# Generate crop advice using Gemini
def get_crop_advice(soil_type, location):
    weather = get_weather(location)

    prompt = f"""
You are an Agriculture expert.

Soil Type: {soil_type}
Weather: {weather}
Location: {location}

Suggest the 3 most suitable crops to grow at the suitable weather and soil. Also explain in 5-6 lines why each crop is suitable.
Suggestion should be given in 2 languages ENGLISH and HINDI.

Provide the response in a friendly and informative tone.
Format the response as follows:
1. Crop Name: [Crop Name] in English and Hindi both.
   Reason: English \n 
   Hindi in both language.
2. Crop Name: [Crop Name] in English and Hindi both.
   Reason: English \n 
   Hindi in both language
3. Crop Name: [Crop Name] in English and Hindi both.
   Reason: English \n 
   Hindi in both language

If no crops are suitable, respond with "No suitable crops found for the given conditions."

Give a motivational message about farming and motivates to grow the farming sector more , at the end.
English message \n
Hindi message.

Do not write text like **Motivational Message (Hindi):** , **Motivational Message (English):**,
only write the **Motivational Message**.
and Bold the crop names , and headings like Crop Name: and Reason: in the response.
and rest of the text should be in normal font.
    """

    response = model.generate_content(prompt)
    return response.text , weather

# Command-line interface
if __name__ == "__main__":
    print("🌾 Crop Advisor with WeatherAPI.com is Ready!")

    while True:
        print("\n👨‍🌾 Type 'exit' to quit at any time.")
        soil = input("👉 Enter soil type: ").strip()
        if soil.lower() == "exit":
            break

        city = input("📍 Enter city name: ").strip()
        if city.lower() == "exit":
            break

        print("\n🌤️ Fetching weather and generating crop advice...\n",get_weather)
        try:
            advice = get_crop_advice(soil, city)
            print("🤖 Advisor:\n")
            print(advice)
        except Exception as e:
            print("❌ Error:", e)

    print("\n👋 Thank you for using Crop Advisor. Happy Farming!")
