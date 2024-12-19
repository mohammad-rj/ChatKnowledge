import faiss
import numpy as np
import google.generativeai as genai
import json
import os
import csv

# پیکربندی Google Generative AI
genai.configure(api_key="aaa")  # جایگزین با کلید API واقعی

# فایل‌های ذخیره‌سازی
faiss_index_file = "faiss_index.bin"
texts_file = "texts.json"
index_file = "faisst_adder_index.txt"
csv_file = "file_info.csv"

# بارگذاری یا ایجاد FAISS Index
if os.path.exists(faiss_index_file):
    index = faiss.read_index(faiss_index_file)
    print(f"Loaded FAISS index with {index.ntotal} vectors.")
else:
    print("FAISS index not found. Creating a new one.")
    index = None

# بارگذاری یا ایجاد JSON
if os.path.exists(texts_file):
    with open(texts_file, "r", encoding="utf-8") as f:
        texts = json.load(f)
else:
    texts = []
    print("JSON file not found. A new one will be created.")

# بارگذاری یا ایجاد فایل ایندکس
if os.path.exists(index_file):
    with open(index_file, "r", encoding="utf-8") as f:
        processed_index = int(f.read().strip())
else:
    processed_index = -1  # اگر فایل موجود نبود از -1 شروع می‌کنیم

# پردازش فایل CSV
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")  # تغییر جداکننده به کاما
    for i, row in enumerate(reader):
        if len(row) < 1:  # بررسی خالی بودن خط
            print(f"Skipping empty line at index {i}.")
            continue

        # گرفتن فقط ستون اول
        file_path = row[0].strip()  # حذف فضای اضافی

        # تغییر مسیر فایل از output به output_summ
        updated_path = file_path.replace("output", "output_summ")

        if not os.path.exists(updated_path):
            print(f"File {updated_path} not found. Skipping.")
            continue

        if i <= processed_index:
            print(f"File {updated_path} already processed. Skipping.")
            continue

        try:
            # خواندن محتوای فایل
            with open(updated_path, "r", encoding="utf-8") as file:
                content = file.read()

            # تولید Embedding
            result = genai.embed_content(model="models/text-embedding-004", content=content)
            embedding = np.array([result['embedding']], dtype='float32')

            # ایجاد FAISS Index اگر وجود ندارد
            if index is None:
                dimension = embedding.shape[1]
                index = faiss.IndexFlatL2(dimension)
                print(f"Created a new FAISS index with dimension {dimension}.")

            # اضافه کردن متن و بردار به FAISS و JSON
            texts.append({"index": i, "path": updated_path, "content": content})
            index.add(embedding)

            # ذخیره اطلاعات
            faiss.write_index(index, faiss_index_file)
            with open(texts_file, "w", encoding="utf-8") as f:
                json.dump(texts, f, ensure_ascii=False, indent=2)

            # به‌روزرسانی فایل ایندکس
            with open(index_file, "w", encoding="utf-8") as idx_file:
                idx_file.write(str(i))

            # نمایش اطلاعات پردازش‌شده
            print(f"Processed and added {updated_path} to FAISS and JSON.")
            print(f"Text: {content}")
            print(f"Embedding: {embedding}")

        except Exception as e:
            print(f"Error processing file {updated_path}: {e}")

print("All files processed and saved successfully!")
