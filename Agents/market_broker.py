import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_market_broker_response(crop, location, quantity=None):
    prompt = f"""
    You are a smart agriculture marketing agent.

    A farmer has the following details:
    - Crop: {crop}
    - Location: {location}
    - Quantity: {quantity or 'Not specified'}

    Please suggest 2-3 best market platforms or local buyers where this crop can be sold at a good price which is trustable and researched on latest data.
    Include:
    - Buyer/market name or platform (e.g., local mandi, cooperative, or online platform like eNAM).
    - Why it's a good location to sell the crops.
    - Estimated price range (simulate realistically for this region and crop).
    Mention that the price is approximate and based on realistic market simulation.
    In both English \n 
    and Hindi in next line for better understanding.

    Be confident in your suggestions, simulate useful examples, and do not refuse to answer due to lack of data. Respond clearly and briefly.
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("🤝 Market Broker Agent Ready!")
    crop = input("🌾 Enter Crop Name: ")
    location = input("📍 Enter Location (City, District): ")
    quantity = input("📦 Enter Quantity (optional): ")

    result = get_market_broker_response(crop, location, quantity)
    print("\n📢 Suggested Market Options:\n")
    print(result)
# This code initializes a market broker agent that suggests market platforms or local buyers for selling crops based on user input.