import os
import subprocess
import requests
from bs4 import BeautifulSoup
from huggingface_hub import snapshot_download
import re

MODELS_DIR = "/app/models"
HF_API_URL = "https://huggingface.co/api/models"
OLLAMA_LOCAL_URL = "http://localhost:11434/api/tags"
OLLAMA_LIBRARY_URL = "https://ollama.com/library"

# ✅ Ensure local directory exists
def ensure_model_dir():
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR, exist_ok=True)

# ✅ List models present locally
def list_local_models():
    ensure_model_dir()
    return [f for f in os.listdir(MODELS_DIR) if os.path.isdir(os.path.join(MODELS_DIR, f))]

# ✅ Check if model exists locally
def model_exists_locally(model_name: str):
    model_path = os.path.join(MODELS_DIR, model_name)
    return os.path.exists(model_path)

# ✅ Search Hugging Face
def search_huggingface_models(query: str, limit: int = 5):
    try:
        response = requests.get(f"{HF_API_URL}?search={query}&limit={limit}")
        if response.status_code == 200:
            data = response.json()
            return [
                {"id": m["id"], "downloads": m.get("downloads", 0), "likes": m.get("likes", 0)}
                for m in data
            ]
        return {"error": f"Failed to fetch models: {response.status_code}"}
    except Exception as e:
        return {"error": f"Exception while searching Hugging Face: {str(e)}"}

# ✅ Search ollama model
def search_ollama_models(query: str | None = None):
    """Search both local and hosted Ollama models, optionally filter by name."""
    # ----------------------------
    # 🔍 Fetch Local Models
    # ----------------------------
    try:
        response = requests.get(OLLAMA_LOCAL_URL, timeout=5)
        local_models = (
            response.json().get("models", [])
            if response.status_code == 200
            else []
        )
    except Exception as e:
        print(f"⚠️ Local Ollama not reachable: {e}")
        local_models = []

    # ----------------------------
    # 🌐 Fetch Hosted Models
    # ----------------------------
    hosted_models = []
    try:
        lib_response = requests.get(OLLAMA_LIBRARY_URL, timeout=10)
        if lib_response.status_code == 200:
            soup = BeautifulSoup(lib_response.text, "html.parser")

            for card in soup.select("a[href^='/library/']"):
                model_name = card.text.strip().lower()
                if not model_name:
                    continue

                # Optional query filtering early for performance
                if query and query.lower() not in model_name:
                    continue

                parent = card.find_parent("div")
                description = ""
                if parent:
                    desc_tag = parent.find("p")
                    if desc_tag:
                        description = desc_tag.text.strip()

                meta = parent.get_text(separator="\n") if parent else ""
                tags = re.findall(r"#(\w+)", meta)
                params = re.findall(r"\b\d+(?:\.\d+)?[bBmM]\b", meta)
                pulls_match = re.search(r"([\d,.]+[K|M]*)\s+Pulls", meta)
                updated_match = re.search(r"Updated\s+([^\n]+)", meta)

                hosted_models.append({
                    "name": model_name,
                    "description": description,
                    "tags": tags,
                    "params": params,
                    "pulls": pulls_match.group(1) if pulls_match else None,
                    "updated": updated_match.group(1) if updated_match else None
                })
    except Exception as e:
        print(f"⚠️ Failed to fetch Ollama hosted models: {e}")
        hosted_models = []

    # ----------------------------
    # 🧩 Optional Filtering for Local Models
    # ----------------------------
    if query:
        local_models = [
            m for m in local_models
            if query.lower() in m.get("name", "").lower()
        ]

    # ----------------------------
    # ✅ Return Unified Result
    # ----------------------------
    return {
        "source": "ollama",
        "query": query or "all",
        "results": {
            "local_models": local_models,
            "hosted_models": hosted_models
        },
        "status": "ok" if local_models or hosted_models else "no_models_found"
    }

# ✅ Download model from Ollama
def download_from_ollama(model_name: str):
    """Try downloading a model using Ollama CLI."""
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
        return {"status": "downloaded", "source": "ollama", "model": model_name}
    except Exception as e:
        return {"status": "failed", "source": "ollama", "error": str(e)}

# ✅ Download model from Hugging Face
def download_from_huggingface(model_repo: str, model_name: str):
    """Download a model from Hugging Face Hub."""
    try:
        ensure_model_dir()
        model_path = os.path.join(MODELS_DIR, model_name)
        snapshot_download(repo_id=model_repo, local_dir=model_path, resume_download=True)
        return {"status": "downloaded", "source": "huggingface", "path": model_path}
    except Exception as e:
        return {"status": "failed", "source": "huggingface", "error": str(e)}

# ✅ Handle user download request
def handle_user_model_download(source: str, model_name: str, hf_repo: str = None):
    """
    Handles user-defined model download from Ollama or Hugging Face.
    """
    ensure_model_dir()

    # Check local first
    if model_exists_locally(model_name):
        return {"status": "already_exists", "model": model_name, "source": "local"}

    # Ollama download
    if source.lower() == "ollama":
        return download_from_ollama(model_name)

    # Hugging Face download
    elif source.lower() == "huggingface":
        if not hf_repo:
            return {"status": "error", "message": "Hugging Face repo ID is required for HF download"}
        return download_from_huggingface(hf_repo, model_name)

    # Invalid source
    else:
        return {"status": "error", "message": "Invalid source. Use 'ollama' or 'huggingface'."}
