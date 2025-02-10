# ===========================
# Stage 1: Dependency Installer (Builder) with GPU Access
# ===========================
FROM pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel AS builder

# Enable GPU
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV CUDA_HOME=/usr/local/cuda-12.1
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev git wget gcc g++ make build-essential curl libglib2.0-0 libpq-dev \
    libgl1-mesa-glx libxrender1 libxext6 libsm6 && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies efficiently
RUN pip install --no-cache-dir cython && \
    pip uninstall -y torchreid

# Clone and install TorchReID from source
RUN git clone https://github.com/KaiyangZhou/deep-person-reid.git /app/torchreid-source && \
    cd /app/torchreid-source && \
    pip install --no-cache-dir -r requirements.txt && \
    python setup.py develop

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is in PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock /app/

# Configure Poetry to install globally (no virtualenv)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Install all Python dependencies in one step to optimize caching
RUN pip install --no-cache-dir \
    ultralytics \
    insightface \
    onnxruntime \
    gdown \
    tensorboard && \
    pip install --no-cache-dir nvidia-pyindex && \
    pip install --no-cache-dir \
        tensorrt==10.3.0 \
        tensorrt-cu12==10.3.0 \
        tensorrt-cu12-bindings==10.3.0 \
        tensorrt-cu12-libs==10.3.0 && \
    pip install --no-cache-dir torch-tensorrt==2.5.0 -f https://github.com/NVIDIA/Torch-TensorRT/releases

RUN pip install --no-cache-dir \
    "nvidia-modelopt[all]" --extra-index-url https://pypi.nvidia.com && \
    pip install faiss-gpu-cu12

# ===========================
# Install TensorRT from NVIDIA
# ===========================
# Download TensorRT tarball
RUN wget -q --show-progress --progress=bar:force:noscroll -O /tmp/TensorRT.tar.gz \
    https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/10.3.0/tars/TensorRT-10.3.0.26.Linux.x86_64-gnu.cuda-12.5.tar.gz

# Extract TensorRT
RUN mkdir -p /opt/tensorrt && \
    tar -xzf /tmp/TensorRT.tar.gz -C /opt/tensorrt --strip-components=1 && \
    rm /tmp/TensorRT.tar.gz

# Move libraries to standard locations
RUN cp -P /opt/tensorrt/targets/x86_64-linux-gnu/lib/libnvinfer* /usr/lib/x86_64-linux-gnu/ && \
    ldconfig

# Move trtexec binary to /usr/bin
RUN cp /opt/tensorrt/targets/x86_64-linux-gnu/bin/trtexec /usr/bin/ && \
    chmod +x /usr/bin/trtexec

# Clean up to save space
RUN rm -rf /opt/tensorrt/samples /opt/tensorrt/data /opt/tensorrt/python /opt/tensorrt/docs

# ===========================
# Stage 2: Final Runtime Image
# ===========================
FROM pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime AS runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_HOME=/usr/local/cuda-12.1

ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Install minimal system dependencies & clean cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libpq-dev libgl1-mesa-glx libxrender1 libxext6 libsm6 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy installed dependencies from builder
COPY --from=builder /opt/conda/lib/python3.11/site-packages /opt/conda/lib/python3.11/site-packages
COPY --from=builder /usr/local /usr/local
COPY --from=builder /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/bin/trtexec /usr/bin/trtexec

# Set working directory
WORKDIR /app

# Copy application source code
COPY . .

# Expose API port
EXPOSE 8000

# Run the application directly
CMD ["tail", "-f", "/dev/null"]
