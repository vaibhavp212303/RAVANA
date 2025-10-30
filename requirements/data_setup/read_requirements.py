import os
import importlib.util
import pprint  # for pretty-printing large dicts/lists

# Get the current folder (data_setup)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up to reach `requirements`
REQ_DIR = os.path.join(BASE_DIR, "..")
REQ_FILE = os.path.join(REQ_DIR, "sample_requirement.py")

# Normalize the path
REQ_FILE = os.path.normpath(REQ_FILE)

print("📂 Loading requirements from:", REQ_FILE)

# Load the module dynamically
spec = importlib.util.spec_from_file_location("sample_requirement", REQ_FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Access your data
if hasattr(module, "requirement"):
    requirements = getattr(module, "requirement")
    print(f"✅ Loaded {len(requirements)} requirements.\n")

    print("📋 Full requirement data:\n")
    pprint.pprint(requirements, width=120)
else:
    print("⚠️ No `REQUIREMENTS` variable found in sample_requirement.py")
