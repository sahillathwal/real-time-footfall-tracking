# ===========================
# Stage 1: Dependency Installer (Builder) with GPU Access
# ===========================
FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04 AS builder

# Enable GPU during build
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV CUDA_HOME=/usr/local/cuda-12.2
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install essential system dependencies for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    git wget gcc g++ \
    libglib2.0-0 libopencv-dev libpq-dev \
    libgl1-mesa-glx libxrender1 libxext6 libsm6 \
    && rm -rf /var/lib/apt/lists/*

# Install cuDNN 8.9.6 via NVIDIA repository
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcudnn8=8.9.6.*-1+cuda12.2 \
    libcudnn8-dev=8.9.6.*-1+cuda12.2 \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment to store dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app


# Copy only requirements file to leverage Docker caching
COPY requirements.txt .

# Install PyTorch with CUDA 12.2 manually to avoid auto-upgrade to CUDA 12.8
# RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu122

# Install TensorRT for CUDA 12.2
RUN pip install --no-cache-dir nvidia-pyindex && pip install --no-cache-dir tensorrt==8.6.*

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt



# ===========================
# Stage 2: Final Runtime Image
# ===========================
FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04 AS runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

ENV CUDA_HOME=/usr/local/cuda-12.2
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Install minimal system dependencies (no dev tools)
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip \
    libglib2.0-0 libpq-dev libgl1-mesa-glx libxrender1 libxext6 libsm6 \
    libcudnn8=8.9.6.*-1+cuda12.2 \
    libcudnn8-dev=8.9.6.*-1+cuda12.2 \
    && rm -rf /var/lib/apt/lists/*

# Ensure CUDA 12.2 Libraries are correctly linked
RUN ln -sf /lib/x86_64-linux-gnu/libcudnn.so.8 /usr/local/cuda-12.2/lib64/libcudnn.so.8 && \
    ln -sf /lib/x86_64-linux-gnu/libcudnn.so /usr/local/cuda-12.2/lib64/libcudnn.so && \
    ldconfig

# Copy the pre-installed virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application source code (only necessary files)
COPY . .

# Expose API port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
