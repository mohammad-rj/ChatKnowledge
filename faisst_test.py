import faiss
import numpy as np
import google.generativeai as genai

# پیکربندی Google Generative AI
genai.configure(api_key="aaa")

# تولید یک Embedding
text = "Hello world"
result = genai.embed_content(model="models/text-embedding-004", content=text)
embedding = np.array(result['embedding'], dtype='float32')  # تبدیل به آرایه NumPy با نوع float32

# ساخت ایندکس FAISS
dimension = len(embedding)  # تعداد ابعاد embedding
index = faiss.IndexFlatL2(dimension)  # استفاده از L2 برای محاسبه فاصله

# اضافه کردن Embedding به ایندکس
index.add(np.array([embedding]))  # اضافه کردن بردار به ایندکس
print("Embedding اضافه شد!")

# ذخیره ایندکس در فایل
faiss.write_index(index, "faiss_index.bin")
print("FAISS Index ذخیره شد!")

# _____________________________________________________________
# # بارگذاری ایندکس ذخیره شده
# index = faiss.read_index("faiss_index.bin")
#
# # تولید Embedding جدید برای جستجو
# query_text = "Hi world"
# query_embedding = genai.embed_content(model="models/text-embedding-004", content=query_text)['embedding']
# query_embedding = np.array([query_embedding], dtype='float32')  # تبدیل به آرایه NumPy
#
# # جستجوی نزدیک‌ترین بردارها
# k = 5  # تعداد نزدیک‌ترین همسایه‌ها
# distances, indices = index.search(query_embedding, k)
#
# print("نزدیک‌ترین بردارها:", indices)
# print("فاصله‌ها:", distances)
