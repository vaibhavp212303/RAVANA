import os
import importlib.util
from sentence_transformers import SentenceTransformer
import chromadb

# -------------------------------
# 1️⃣ Load real requirements dynamically
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQ_DIR = os.path.join(BASE_DIR, "..")
REQ_FILE = os.path.normpath(os.path.join(REQ_DIR, "sample_requirement.py"))

print("📂 Loading requirements from:", REQ_FILE)

spec = importlib.util.spec_from_file_location("sample_requirement", REQ_FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

requirement = module.requirement
print("✅ Loaded requirements successfully!")

# Flatten complex nested requirement dicts into text
def extract_text(obj):
    texts = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                texts.extend(extract_text(value))
            elif isinstance(value, str):
                if any(k in key.lower() for k in ["title", "subtitle", "label", "text", "description"]):
                    texts.append(value)
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_text(item))
    return texts

texts = extract_text(requirement)
print(f"🧾 Extracted {len(texts)} text chunks.")

# -------------------------------
# 2️⃣ Initialize vector database + model
# -------------------------------
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("requirements")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("🧠 Model loaded.")

# -------------------------------
# 3️⃣ Create embeddings and add to Chroma
# -------------------------------
embeddings = model.encode(texts)
collection.add(
    ids=[f"REQ-{i+1:03d}" for i in range(len(texts))],
    documents=texts,
    embeddings=embeddings.tolist(),
    metadatas=[{"source": "sample_requirement", "index": i} for i in range(len(texts))],
)

print(f"✅ Stored {len(texts)} requirement texts in Chroma DB.")

# -------------------------------
# 4️⃣ Semantic search demo
# -------------------------------
query = "sign in to the system using email"
query_emb = model.encode([query]).tolist()

results = collection.query(query_embeddings=query_emb, n_results=3)

print(f"\n🔍 Search results for: '{query}'\n")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"- ID: {meta['index']}, Source: {meta['source']}")
    print(f"  → {doc}\n")
