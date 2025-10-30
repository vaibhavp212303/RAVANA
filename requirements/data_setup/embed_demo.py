import os
import importlib.util
import pprint
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# --- Step 1: Load sample_requirement.py dynamically ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQ_DIR = os.path.join(BASE_DIR, "..")
REQ_FILE = os.path.normpath(os.path.join(REQ_DIR, "sample_requirement.py"))

print("📂 Loading requirements from:", REQ_FILE)
spec = importlib.util.spec_from_file_location("sample_requirement", REQ_FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if not hasattr(module, "requirement"):
    raise ValueError("⚠️ No 'requirement' variable found in sample_requirement.py")

requirement = module.requirement
print("✅ Requirement loaded successfully.\n")

pprint.pprint(requirement)

# --- Step 2: Flatten the requirement data into text chunks ---
def extract_text(obj):
    """Recursively extract meaningful text fields from nested dicts/lists"""
    texts = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                texts.extend(extract_text(value))
            elif isinstance(value, str):
                if any(word in key.lower() for word in ["title", "subtitle", "description", "label", "text"]):
                    texts.append(value)
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_text(item))

    return texts

texts = extract_text(requirement)
print(f"\n🧾 Extracted {len(texts)} text snippets for embedding.")
for t in texts[:5]:
    print("-", t)

# --- Step 3: Generate embeddings ---
print("\n🧠 Loading model: all-MiniLM-L6-v2 ...")
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(texts)
print(f"✅ Created {len(embeddings)} embeddings.")
print(f"Vector dimension: {len(embeddings[0])}")

# --- Step 4: Save embeddings ---
output_path = os.path.join(BASE_DIR, "embeddings_output.json")
data_to_save = [
    {"text": t, "embedding": emb.tolist()}
    for t, emb in zip(texts, embeddings)
]

with open(output_path, "w") as f:
    json.dump(data_to_save, f, indent=2)

print(f"\n💾 Saved embeddings to: {output_path}")
