import os

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROMPTS_FILE = os.path.join(BASE_DIR, "prompts", "prompts.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Model Config
MODEL_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llava:7b"
USE_STREAM = True

# Logging
CPU_LOG_FILE = os.path.join(BASE_DIR, "cpu_usage.log")
