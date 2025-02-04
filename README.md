# Real-Time Footfall Tracking and Demographic Analysis

## Overview
This open-source project provides a **real-time footfall tracking and demographic analysis system** using **AI-based face detection, tracking, and unique identification**. It captures video streams from an **RTSP-enabled camera**, processes them using **YOLOv8 + DeepSORT + FaceNet**, and displays the results in a **real-time dashboard**.

## Features
- 🚀 **Real-time footfall counting** with unique identification
- 🎭 **Demographic analysis** (age & gender estimation)
- 📹 **RTSP camera support** for high-resolution face detection
- 🖥 **Live dashboard** using FastAPI & Dash
- 📦 **Containerized setup** for easy deployment
- 📊 **MongoDB integration** for data storage

## Tech Stack
- **AI/ML:** YOLOv8 (Object Detection), DeepSORT (Tracking), FaceNet (Embeddings)
- **Backend:** FastAPI (Python)
- **Frontend:** Dash (for real-time visualization)
- **Database:** MongoDB (for unique IDs & analytics)
- **Containerization:** Docker & Docker Compose

## Directory Structure
```
📦 real-time-footfall-tracking
 ├── 📂 camera_stream/         # RTSP Streaming Handler
 │   ├── rtsp_stream.py        # Script for capturing RTSP feed
 ├── 📂 detection/             # Face Detection & Tracking
 │   ├── face_detector.py      # YOLOv8 for Face Detection
 ├── 📂 embedding/             # Unique ID Matching
 │   ├── face_embedding.py     # FaceNet-based Embeddings
 ├── 📂 database/              # Database Handlers
 │   ├── mongo_handler.py      # MongoDB Integration
 ├── 📂 dashboard/             # Live Dashboard
 │   ├── app.py                # Dash Visualization
 ├── app.py                    # FastAPI Application Entry
 ├── requirements.txt           # Python Dependencies
 ├── Dockerfile                 # Containerization Setup
 ├── docker-compose.yml         # Multi-container Setup
 ├── 📂 config/                 # Configuration Files
 │   ├── config.yaml            # RTSP & System Config
 ├── 📂 tests/                  # Unit Tests
 ├── 📜 README.md               # Project Overview
 ├── 📜 CONTRIBUTING.md         # Contribution Guidelines
 ├── 📜 LICENSE                 # Open-source License
 ├── 📜 .gitignore              # Ignore Unnecessary Files
 ├── 📜 setup.sh                # Automated Setup Script
```

## Installation & Setup

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/real-time-footfall-tracking.git
cd real-time-footfall-tracking
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Configure RTSP Stream**
Edit `config/config.yaml` with your **camera RTSP URL**:
```yaml
RTSP_URL: "rtsp://USERNAME:PASSWORD@CAMERA_IP:PORT"
```

### **4. Run the Application (Standalone Mode)**
```bash
python app.py
```

### **5. Run the Application (Docker Mode)**
#### **Step 1: Build Docker Containers**
```bash
docker-compose build
```
#### **Step 2: Start Services**
```bash
docker-compose up -d
```
#### **Step 3: Check Running Containers**
```bash
docker ps
```

## API Endpoints
| Method | Endpoint         | Description                  |
|--------|----------------|------------------------------|
| GET    | `/`             | Health check                 |
| GET    | `/stats`        | Get real-time footfall stats |
| GET    | `/dashboard`    | Live visualization           |

## Contributing
We welcome contributions! Please check out the `CONTRIBUTING.md` file for details on how to contribute.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Authors & Credits
- **Sahil Lathwal** (@sahillathwal)
- Special thanks to the open-source community! 🚀

