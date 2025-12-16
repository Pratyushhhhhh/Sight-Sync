# ai_pipeline.py
from core.vision_ai import describe_scene
from core.tts_engine import speak
from deep_translator import GoogleTranslator

TARGET_LANG = "en"  # Change this if needed

def process_image(image_path: str):
    """Run the AI description + TTS on the provided image."""
    print("[AI] Describing scene...")
    description = describe_scene(image_path)
    print(f"[ENGLISH] {description}")

    if TARGET_LANG != "en":
        translated = GoogleTranslator(source="auto", target=TARGET_LANG).translate(description)
        print(f"[TRANSLATED] {translated}")
    else:
        translated = description

    print("[AI] Speaking description...")
    speak(translated, lang=TARGET_LANG)
    print("[AI] Done!")
