import os
import gtts
import pygame
import time

def speak(text: str, lang: str = "en"):
    """Speak text aloud in the specified language using gTTS + pygame."""
    try:
        filename = f"tts_{int(time.time())}.mp3"
        tts = gtts.gTTS(text=text, lang=lang)
        tts.save(filename)

        # Initialize pygame mixer safely
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        print(f"[Audio] Speaking in '{lang}'...")

        # Wait until the speech finishes
        while pygame.mixer.music.get_busy():
            time.sleep(0.3)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

        # Give Windows time to release file handle before removing
        time.sleep(0.3)
        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
        print(f"[TTS Error] {e}")
