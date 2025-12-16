import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def describe_scene(image_path: str):
    """Send an image to Gemini and return a concise description."""
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # You can use gemini-1.5-flash or gemini-1.5-pro depending on your key
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            {"text": "Describe this image vividly and clearly for a visually impaired person in 1-2 sentences."}
        ])

        return response.text.strip() if response.text else "No description received."

    except Exception as e:
        return f"[Error] {e}"
