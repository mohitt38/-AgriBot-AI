import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini Vision model
model = genai.GenerativeModel("gemini-1.5-flash")

# Analyze crop image
def analyze_crop_image(uploaded_file):
    try:
        # Read bytes from UploadedFile
        image_data = uploaded_file.getvalue()

        # Check if data is empty
        if not image_data:
            return "❌ Error: Uploaded image data is empty. Please upload a valid image."

        prompt = """
        This is a crop leaf image taken by a farmer.
        Please analyze if there are any visible signs of plant disease or pest.
        If yes:
        - Name the crop disease (if possible).
        - Mention symptoms seen in the image.
        - Suggest treatment or preventive remedy.
        - Mention whether it's serious or mild.
        - Mention if it can be treated at home or requires professional help.
        - Help the farmer understand the issue clearly.
        - Provide a friendly and informative response.
        If the image is not clear or no disease is detected, say please provide a clearer image.
        If no disease is detected, say it's healthy.
        explain in hindi and english both.
        """

        # Send to Gemini
        response = model.generate_content([
            prompt,
            {
                "mime_type": uploaded_file.type,  # e.g., "image/jpeg"
                "data": image_data
            }
        ])
        return response.text

    except Exception as e:
        return f"❌ Error: {e}"



# Run the agent
if __name__ == "__main__":
    print("🌿 Crop Disease Detection Agent")
    image_path = input("Enter the path of image : ").strip().strip('"')


    result = analyze_crop_image(image_path)
    print("\n📋 Diagnosis Result:\n")
    print(result)
