# ===========================
# Stage 1: Dependency Installer (Builder) with GPU Access
# ===========================
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04 AS builder

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
    git wget gcc g++ curl \
    libglib2.0-0 libopencv-core libpq-dev \
    libgl1-mesa-glx libxrender1 libxext6 libsm6 \
    && apt-mark manual python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is in PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Install PyTorch (CUDA 12.1 - Closest match to 12.2)
RUN poetry run pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install TensorRT
RUN poetry run pip install nvidia-pyindex && \
    poetry run pip install --no-cache-dir tensorrt

# ===========================
# Stage 2: Final Runtime Image
# ===========================
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04 AS runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

ENV CUDA_HOME=/usr/local/cuda-12.2
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# Install minimal system dependencies
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    python3 python3-pip \
    libglib2.0-0 libpq-dev libgl1-mesa-glx libxrender1 libxext6 libsm6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the installed dependencies from the builder stage
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/local /usr/local

# Ensure Poetry is still available in the runtime container
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application source code
COPY . .

# Create a non-root user for better security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser
USER appuser

# Expose API port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
