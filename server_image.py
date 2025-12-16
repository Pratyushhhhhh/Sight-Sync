# server_yolo.py
from flask import Flask, request, jsonify
import os, datetime
from yolo_pipeline import process_image
import threading

app = Flask(__name__)

UPLOAD_DIR = os.path.join(os.getcwd(), "received_images")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return "✅ Flask YOLO Receiver is running."

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file found in request'}), 400

        image_file = request.files['image']
        timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        filename = f"img_{timestamp}.jpg"
        save_path = os.path.join(UPLOAD_DIR, filename)
        image_file.save(save_path)
        print(f"[📥] Received image -> {save_path}")

        threading.Thread(target=process_image, args=(save_path,)).start()
        return jsonify({'status': 'ok', 'saved_as': filename}), 200

    except Exception as e:
        print(f"[❌] Server error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
