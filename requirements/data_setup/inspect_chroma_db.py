import chromadb
from pprint import pprint

# 1️⃣ Connect to the same Chroma DB path
client = chromadb.PersistentClient(path="./chroma_db")

# 2️⃣ List all collections
collections = client.list_collections()
print("\n📚 Available Collections:")
for c in collections:
    print("-", c.name)

# 3️⃣ Access the collection you used
collection = client.get_collection("requirements")

# 4️⃣ Fetch all stored items (include docs + embeddings if present)
print("\n📦 Stored Data in 'requirements' Collection:")
data = collection.get(include=["documents", "embeddings", "metadatas"])

# ✅ Handle None gracefully
ids = data.get("ids", [])
docs = data.get("documents") or []
metas = data.get("metadatas") or []
embs = data.get("embeddings")

print(f"🔹 Total items: {len(ids)}\n")

# 5️⃣ Print available info for each record
for i, item_id in enumerate(ids):
    print(f"ID: {item_id}")
    print(f"Document: {docs[i] if i < len(docs) else '(no document)'}")
    print(f"Metadata: {metas[i] if i < len(metas) else '(no metadata)'}")
    print("-" * 80)

# 6️⃣ Optional: embedding details
if embs and len(embs) > 0:
    print(f"\n🧠 Example embedding vector length: {len(embs[0])}")
    print(f"First 10 numbers: {embs[0][:10]}")
else:
    print("\n⚠️ No embeddings found or they weren’t stored.")
