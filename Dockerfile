# ===========================
# Stage 1: Dependency Installer (Builder) with GPU Access
# ===========================
FROM pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime AS builder

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
    python3-dev git wget gcc g++ curl libglib2.0-0 libpq-dev \
    libgl1-mesa-glx libxrender1 libxext6 libsm6 \
    && rm -rf /var/lib/apt/lists/*

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

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libpq-dev libgl1-mesa-glx libxrender1 libxext6 libsm6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy installed dependencies from builder
COPY --from=builder /usr/local /usr/local

# Set working directory
WORKDIR /app

# Copy application source code
COPY . .

# Set correct ownership before switching user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose API port
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application directly
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
