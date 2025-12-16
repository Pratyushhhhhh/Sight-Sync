# yolo_pipeline.py
import os
import cv2
import time
from ultralytics import YOLO
import pyttsx3
import traceback
import threading
import requests

# ================= SETTINGS =================
DIST_LIMIT_OBSTACLE = 8.0
DIST_LIMIT_POTHOLE = 5.0
FOCAL_LENGTH_MM = 3.6
SENSOR_HEIGHT_MM = 2.76  # mm, adjust for your camera

# Motor control endpoints (Pi or motor controller)
MOTOR_ON_URL = "http://192.168.112.2/motor/on"
MOTOR_OFF_URL = "http://192.168.112.2/motor/off"
MOTOR_TIMEOUT = 3  # seconds for HTTP requests

# Vibration durations
MOTOR_RUN_WARNING = 5   # seconds when warning (pothole)
MOTOR_RUN_CAUTION = 2   # seconds when caution (obstacle)

KNOWN_HEIGHTS = {
    "person": 1.7,
    "car": 1.5,
    "motorcycle": 1.2,
    "bicycle": 1.1,
    "bus": 3.0,
    "truck": 3.0,
    "dog": 0.6,
    "cat": 0.3,
    "chair": 1.0,
    "bottle": 0.25,
    "traffic light": 2.5,
    "bench": 1.0,
    "handbag": 0.4,
    "backpack": 0.5,
    "helmet": 0.3,
    "trolley": 0.8,
    "pothole": 0.15
}

# ================= INITIALIZE =================
print("🚀 Starting YOLO Object Detection + TTS + Motor System...")

tts_lock = threading.Lock()  # Prevent simultaneous TTS access

try:
    model_coco = YOLO("yolov8n.pt")
    model_pothole = model_coco  # use same model if pothole one not available
    print("✅ YOLO models loaded successfully.")
except Exception as e:
    print("❌ Error loading YOLO models:", e)
    raise

# ================= HELPERS =================
def calculate_distance(real_height_m, bbox_height_px, image_height_px):
    if bbox_height_px <= 0:
        return None
    D = (real_height_m * FOCAL_LENGTH_MM * image_height_px) / (bbox_height_px * SENSOR_HEIGHT_MM)
    return round(D, 2)

def get_direction(center_x, frame_width):
    third = frame_width / 3
    if center_x < third:
        return "left"
    elif center_x < 2 * third:
        return "center"
    else:
        return "right"

def trigger_motor(run_seconds):
    """Turn motor ON, wait run_seconds, then turn OFF (runs in thread)."""
    try:
        print(f"[MOTOR] ON for {run_seconds}s → {MOTOR_ON_URL}")
        try:
            requests.get(MOTOR_ON_URL, timeout=MOTOR_TIMEOUT)
        except Exception as e:
            print(f"[MOTOR] Error sending ON: {e}")

        time.sleep(run_seconds)

        print(f"[MOTOR] OFF → {MOTOR_OFF_URL}")
        try:
            requests.get(MOTOR_OFF_URL, timeout=MOTOR_TIMEOUT)
        except Exception as e:
            print(f"[MOTOR] Error sending OFF: {e}")
    except Exception as e:
        print(f"[MOTOR] Unexpected motor error: {e}")

# ================= MAIN FUNCTION =================
def process_image(image_path: str):
    """Run YOLO detection + TTS for a single image and trigger motor accordingly."""
    print(f"[🧠 YOLO] Processing {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        print(f"[⚠️] Could not read image: {image_path}")
        return

    height_px, width_px, _ = image.shape
    detected_vehicles = []
    detected_potholes = []

    try:
        results_coco = model_coco(image)
    except Exception as e:
        print(f"❌ YOLO (COCO) failed for {image_path}: {e}")
        traceback.print_exc()
        return

    # Optional pothole detection (currently same model)
    try:
        results_pothole = model_pothole(image)
    except Exception:
        results_pothole = None

    # Parse COCO detections
    for box in results_coco[0].boxes:
        cls = model_coco.names[int(box.cls)]
        if cls not in KNOWN_HEIGHTS:
            continue
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        bbox_height = abs(y2 - y1)
        distance = calculate_distance(KNOWN_HEIGHTS[cls], bbox_height, height_px)
        if not distance:
            continue
        if cls != "traffic light" and distance <= DIST_LIMIT_OBSTACLE:
            direction = get_direction((x1 + x2) / 2, width_px)
            detected_vehicles.append(f"{cls} {distance} meters {direction}")

    # Parse pothole detections (if any)
    if results_pothole:
        for box in results_pothole[0].boxes:
            cls = model_pothole.names[int(box.cls)]
            if cls != "pothole":
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            bbox_height = abs(y2 - y1)
            distance = calculate_distance(KNOWN_HEIGHTS[cls], bbox_height, height_px)
            if not distance:
                continue
            if distance <= DIST_LIMIT_POTHOLE:
                direction = get_direction((x1 + x2) / 2, width_px)
                detected_potholes.append(f"Pothole {distance} meters {direction}")

    # ================== TTS + MOTOR ==================
    messages = []
    motor_time = 0

    if detected_potholes:
        messages.append("Warning! " + ", ".join(detected_potholes))
        motor_time = MOTOR_RUN_WARNING
    elif detected_vehicles:
        messages.append("Caution! " + ", ".join(detected_vehicles))
        motor_time = MOTOR_RUN_CAUTION
    else:
        messages.append("All clear ahead")
        motor_time = 0

    # Start motor thread if needed
    if motor_time > 0:
        try:
            threading.Thread(target=trigger_motor, args=(motor_time,), daemon=True).start()
            print(f"[MOTOR] Triggered for {motor_time}s.")
        except Exception as e:
            print(f"[MOTOR] Could not start motor thread: {e}")

    # Speak messages safely
    with tts_lock:
        for msg in messages:
            print(f"🗣 Speaking: {msg}")
            try:
                local_engine = pyttsx3.init()
                local_engine.setProperty('rate', 160)
                local_engine.setProperty('volume', 1.0)
                local_engine.say(msg)
                local_engine.runAndWait()
                local_engine.stop()
                del local_engine
            except Exception as e:
                print(f"[TTS error] {e}")

# ================= END =================
print("✅ YOLO + TTS + Motor system ready.")
