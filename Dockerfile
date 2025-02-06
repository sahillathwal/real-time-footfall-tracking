# Use an official lightweight Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

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

# Expose API port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
