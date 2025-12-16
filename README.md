# Sight_Sync

**AI-Powered Assistive Smart Glasses and Haptic Wristband for Navigation & Environmental Awareness**

## 1. Project Overview

Sight_Sync is an assistive technology system designed to enhance independent navigation and situational awareness for visually impaired users. The system consists of two tightly integrated wearable components:

- **Smart Glasses** — responsible for vision, perception, and audio guidance
- **Haptic Wristband** — responsible for tactile alerts and threat awareness

By combining computer vision, real-time audio feedback, and haptic signaling, Sight_Sync enables users to safely navigate environments, understand surroundings, and respond to nearby threats.

---

## 2. Smart Glasses Preview

### Prototype

![Sight_Sync Glasses](assets/images/protoype.jpg)

---

## 3. System Components

### 3.1 Smart Glasses (Primary Perception Unit)

| Component | Description |
|-----------|-------------|
| **Camera** | 5MP camera connected to Raspberry Pi Zero 2W |
| **Processor** | Raspberry Pi Zero 2W |
| **Audio Output** | TWS earphones for real-time voice feedback |
| **Input** | Three physical buttons |
| **Connectivity** | Wi-Fi + Bluetooth Low Energy (BLE) |

#### Functions:
- Obstacle and threat detection using YOLO
- Scene understanding and environment description
- Text recognition for books, newspapers, road signs
- Location awareness and navigation (in progress)
- Audio feedback using Text-to-Speech (TTS)

#### Buttons & Functional Mapping

| Button | Function |
|--------|----------|
| **Button 1** | Runs YOLO model for obstacle & threat detection and provides audio alerts |
| **Button 2** | Describes surroundings and reads text (books, articles, signs) |
| **Button 3** (WIP) | Single press: announces current location using Wi-Fi<br>Double press: navigates to a predefined location (e.g., home) |

### 3.2 Haptic Wristband (Threat Alert Unit)

| Component | Description |
|-----------|-------------|
| **Microcontroller** | ESP32 |
| **Actuator** | Vibration motor |
| **Communication** | Bluetooth Low Energy (BLE) |
| **Power** | Battery powered |

#### Functions:
- Receives threat alerts from smart glasses
- Provides tactile feedback based on threat severity

#### Vibration Alert Levels

| Threat Level | Feedback |
|--------------|----------|
| **Moderate** | Short vibration pulses |
| **High** | Continuous or intense vibration |

This ensures silent, immediate alerts, especially in noisy environments.

---

## 4. System Architecture

| Layer | Responsibility |
|-------|----------------|
| **Wearables** | Image capture, audio output, vibration alerts |
| **Server (PC)** | Heavy image processing, AI inference, message generation |
| **Communication** | Wi-Fi (Pi ↔ Server), BLE (Pi ↔ Wristband) |

### Data Flow

```
Camera → Raspberry Pi → PC Server
                   ↓
          AI Processing (YOLO, OCR, NLP)
                   ↓
        Audio & Alert Messages
                   ↓
    TWS Earphones & Wristband (ESP32)
```

---

## 5. Core Functionalities

### 5.1 Obstacle & Threat Detection
- YOLO-based real-time object detection
- Identifies obstacles, vehicles, animals, and moving threats
- Classifies threat levels (moderate / high)
- Sends alerts via audio and haptic feedback

### 5.2 Surroundings Description
- Scene understanding and object summarization
- Verbal description of nearby environment
- Useful for unfamiliar locations and indoor spaces

### 5.3 Text Reading Assistance
- Reads books, newspapers, articles
- Detects and reads road signs and labels
- Converts text to natural-sounding speech

### 5.4 Location & Navigation (Work in Progress)
- Wi-Fi–based location estimation
- Predefined destination navigation
- Audio-based turn guidance

---

## 6. Technology Stack

### Hardware
- Raspberry Pi Zero 2W
- 5MP Camera Module
- ESP32
- Vibration Motor
- TWS Earphones
- Physical Push Buttons

### Software
- Python
- OpenCV
- YOLO (Object Detection)
- OCR (Text Recognition)
- Text-to-Speech (TTS)
- Flask / Socket-based server
- Bluetooth Low Energy (BLE)

---

## 7. Project Structure

```
Sight_Sync/
│
├── server/
│   ├── vision_processing/
│   ├── yolo_model/
│   ├── ocr_module/
│   └── tts_engine/
│
├── raspberry_pi/
│   ├── camera_interface/
│   ├── button_handlers/
│   ├── ble_communication/
│   └── audio_output/
│
├── wristband/
│   ├── esp32_firmware/
│   └── vibration_control/
│
├── assets/
│   └── images/
│       └── glasses.jpg
│
└── README.md
```

---

## 8. Use Cases

- Independent outdoor navigation
- Obstacle avoidance in crowded areas
- Safe movement near roads and traffic
- Reading printed content hands-free
- Situational awareness in unfamiliar environments

---

## 9. Future Enhancements

- GPS-assisted navigation
- Cloud + edge hybrid inference
- Gesture-based controls
- Language translation
- Battery optimization and miniaturization

---

## 10. Impact

Sight_Sync aims to provide:

- Increased independence for visually impaired users
- Faster threat awareness through multimodal feedback
- Affordable and modular assistive technology

---

## 11. License

This project is released under the [MIT License](LICENSE).
