

FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev git wget \
    libgl1-mesa-glx ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon0 \
    libx11-xcb1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libopencv-dev \
    x11-apps \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*
# Install YOLOv8, DeepSORT, DeepFace, OpenCV with CUDA
RUN pip install ultralytics
RUN pip install deepface[tensorflow]
RUN pip install opencv-contrib-python-headless
RUN pip install deep_sort_realtime
RUN pip install pymongo

RUN pip install uvicorn fastapi
# Set the working directory

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


WORKDIR /app

# Copy application source code
COPY . .

# # Expose API port
EXPOSE 8000

# # Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Run the application
# CMD ["python", "footfall_tracking.py"]
