from core.camera import capture_image
from core.vision_ai import describe_scene
from core.tts_engine import speak
from deep_translator import GoogleTranslator

# 🌍 Choose your target language here
TARGET_LANG = "en"  # 'en', 'fr', 'es', 'hi', 'de', etc.

def main():
    print("[SightSync] Capturing image...")
    image_path = capture_image()

    print("[SightSync] Describing scene...")
    description = describe_scene(image_path)
    print(f"[ENGLISH] {description}")

    # Translate if language is not English
    if TARGET_LANG != "en":
        translated = GoogleTranslator(source="auto", target=TARGET_LANG).translate(description)
        print(f"[TRANSLATED] {translated}")
    else:
        translated = description

    print("[SightSync] Speaking description...")
    speak(translated, lang=TARGET_LANG)
    print("[SightSync] Done!")

if __name__ == "__main__":
    main()
