import faiss
import numpy as np
import google.generativeai as genai
import json
import os  # برای بررسی وجود فایل

# پیکربندی Google Generative AI
genai.configure(api_key="aaa")  # جایگزین با کلید API واقعی

# فایل‌های ذخیره‌سازی
faiss_index_file = "faiss_index.bin"
texts_file = "texts.json"

# بررسی وجود FAISS Index
if os.path.exists(faiss_index_file):
    index = faiss.read_index(faiss_index_file)
    print(f"Loaded FAISS index with {index.ntotal} vectors.")
else:
    print("FAISS index not found. Creating a new one.")
    index = None

# بارگذاری یا ایجاد فایل JSON
if os.path.exists(texts_file):
    with open(texts_file, "r", encoding="utf-8") as f:
        texts = json.load(f)
else:
    texts = []
    print("JSON file not found. A new one will be created.")

# متنی که باید اضافه شود
new_text = "This is a new text to add."

# تولید Embedding
result = genai.embed_content(model="models/text-embedding-004", content=new_text)
new_embedding = np.array([result['embedding']], dtype='float32')

# ایجاد FAISS Index اگر وجود ندارد
if index is None:
    dimension = new_embedding.shape[1]
    index = faiss.IndexFlatL2(dimension)
    print(f"Created a new FAISS index with dimension {dimension}.")

# اضافه کردن متن و بردار به FAISS و JSON
texts.append(new_text)
index.add(new_embedding)

# ذخیره FAISS Index و JSON
faiss.write_index(index, faiss_index_file)
with open(texts_file, "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False, indent=2)

print("New text and embedding added successfully!")
