import faiss
import numpy as np
import google.generativeai as genai
import json

# پیکربندی Google Generative AI
genai.configure(api_key="aaa")  # جایگزین با کلید API واقعی

# فایل‌های ذخیره‌سازی
faiss_index_file = "faiss_index.bin"
texts_file = "texts.json"

# بارگذاری FAISS Index
index = faiss.read_index(faiss_index_file)
print(f"Number of vectors in the loaded index: {index.ntotal}")

# بارگذاری فایل متون
with open(texts_file, "r", encoding="utf-8") as f:
    texts = json.load(f)

# متنی که باید پرس‌وجو شود
query_text = "telegram mini app"
result = genai.embed_content(model="models/text-embedding-004", content=query_text)
query_embedding = np.array([result['embedding']], dtype='float32')  # تبدیل متن به embedding

# جستجوی نزدیک‌ترین بردارها
k = 5  # تعداد نزدیک‌ترین همسایه‌ها
distances, indices = index.search(query_embedding, k)

print("نزدیک‌ترین بردارها (ایندکس‌ها):", indices)
print("فاصله‌ها:", distances)

# نمایش نتایج
for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
    if idx != -1:  # اگر برداری پیدا شد
        text = texts[idx]  # متن مربوط به ایندکس پیدا شده
        print(f"Result {i+1}: Index={idx}, Distance={dist}, Text='{text}'")
    else:
        print(f"Result {i+1}: No result found")
