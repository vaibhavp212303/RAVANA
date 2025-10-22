from fastapi import FastAPI, Query
from pydantic import BaseModel
from system_info import get_system_info
from model_manager import (
    list_local_models,
    handle_user_model_download,
    search_huggingface_models,
    search_ollama_models
)

app = FastAPI(title="Dynamic AI Model Manager")

# ✅ Health check
@app.get("/")
def root():
    return {"message": "🐍 FastAPI Docker with Dynamic Model Control is running!"}

# ✅ System info
@app.get("/system-info")
def system_info():
    return get_system_info()

# ✅ List local models
@app.get("/models")
def list_models():
    return {"models": list_local_models()}

# ✅ Search models
@app.get("/search-models")
def search_models(
    source: str = Query(..., description="Source: 'huggingface' or 'ollama'"),
    query: str = Query("", description="Model name or keyword (for Hugging Face)")
):
    """
    Example:
    /search-models?source=huggingface&query=llava
    /search-models?source=ollama
    """
    if source.lower() == "huggingface":
        return {"source": "huggingface", "results": search_huggingface_models(query)}
    elif source.lower() == "ollama":
        return {"source": "ollama", "results": search_ollama_models(query)}
    else:
        return {"error": "Invalid source. Use 'huggingface' or 'ollama'."}

# 🧩 User-defined model download request
class ModelRequest(BaseModel):
    source: str  # "ollama" or "huggingface"
    model_name: str
    hf_repo: str | None = None

@app.post("/download-model")
def download_model(request: ModelRequest):
    """
    Example:
    {
      "source": "huggingface",
      "model_name": "llava-v1.5-7b",
      "hf_repo": "liuhaotian/llava-v1.5-7b"
    }
    or
    {
      "source": "ollama",
      "model_name": "llava"
    }
    """
    result = handle_user_model_download(
        source=request.source,
        model_name=request.model_name,
        hf_repo=request.hf_repo
    )
    return result
