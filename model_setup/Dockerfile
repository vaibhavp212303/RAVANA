# ======================================================
# 🧠 Base Image: Ollama Official
# ======================================================
FROM ollama/ollama:latest

# Optional: Pre-pull model(s) during image build
# Comment this line if you want to pull models manually later
RUN ollama pull llava:7b

# Expose the Ollama API port
EXPOSE 11434

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11434

# Default command: start the Ollama server
CMD ["serve"]
