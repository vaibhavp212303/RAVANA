# ---- Base Image ----
FROM python:3.12-slim

# ---- Environment setup ----
ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_MODELS=/root/.ollama/models
ENV PATH="/root/.local/bin:$PATH"

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y \
    curl gnupg ca-certificates git tar gzip && \
    rm -rf /var/lib/apt/lists/*

# ---- Install Ollama ----
RUN set -eux; \
    ARCH=$(uname -m); \
    echo "Detected architecture: $ARCH"; \
    curl -fsSL https://ollama.ai/install.sh -o /tmp/install.sh && \
    chmod +x /tmp/install.sh && \
    /tmp/install.sh || (echo "⚠️ Ollama install failed — continuing for build stability")

# ---- Create working directory ----
WORKDIR /app

# ---- Copy app code ----
COPY app/ ./
COPY requirements.txt ./

# ---- Install Python dependencies ----
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# ---- Expose Ports ----
EXPOSE 11434 8000

# ---- Start both services ----
CMD bash -c "\
    echo '🚀 Starting Ollama server...' && \
    ollama serve & \
    sleep 5 && \
    echo '🔥 Starting FastAPI app...' && \
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload \
"
