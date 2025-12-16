import socket
import cv2
import numpy as np
import io
import pyttsx3
from ultralytics import YOLO
from PIL import Image
import time

# Load YOLO models
model_coco = YOLO("yolov8n.pt")
model_pothole = YOLO("yolo/models/best.pt")

# Setup TTS
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

# Socket setup
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print(f"✅ Server listening on {HOST}:{PORT}")

def process_image(image):
    """Run YOLO + TTS processing"""
    results_coco = model_coco(image)
    results_pothole = model_pothole(image)

    detected = []
    for box in results_coco[0].boxes:
        cls = model_coco.names[int(box.cls)]
        if cls in ["person", "car", "truck", "bus"]:
            detected.append(cls)
    for box in results_pothole[0].boxes:
        cls = model_pothole.names[int(box.cls)]
        if cls == "pothole":
            detected.append("pothole")

    if detected:
        msg = "Caution! " + ", ".join(set(detected)) + " ahead."
    else:
        msg = "All clear."

    print("🗣 Speaking:", msg)
    engine.save_to_file(msg, "response.wav")
    engine.runAndWait()
    return "response.wav"

def recv_image(conn):
    """Receive image bytes and decode"""
    data = b''
    payload_size = 4
    size_info = conn.recv(payload_size)
    if not size_info:
        return None
    size = int.from_bytes(size_info, 'big')
    while len(data) < size:
        packet = conn.recv(4096)
        if not packet:
            return None
        data += packet
    image_data = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    return image

def send_audio(conn, filename):
    """Send audio file to client"""
    with open(filename, 'rb') as f:
        audio_data = f.read()
    size = len(audio_data)
    conn.sendall(size.to_bytes(4, 'big'))
    conn.sendall(audio_data)
    print("🎵 Sent audio response")

while True:
    conn, addr = sock.accept()
    print(f"📸 Connected with {addr}")
    try:
        while True:
            image = recv_image(conn)
            if image is None:
                print("❌ Client disconnected.")
                break
            audio_file = process_image(image)
            send_audio(conn, audio_file)
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()
