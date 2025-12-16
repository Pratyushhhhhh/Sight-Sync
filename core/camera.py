import cv2
import time
import os

def capture_image():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        raise RuntimeError("Camera not detected.")
    file_path = f"capture_{int(time.time())}.jpg"
    cv2.imwrite(file_path, frame)
    cam.release()
    return file_path
