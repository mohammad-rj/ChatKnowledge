import tkinter as tk
import tiktoken
import google.generativeai as genai
import faiss
import json
import os
import numpy as np

# تنظیم API کلید
genai.configure(api_key="aaa")  # جایگزین با کلید API واقعی
model = genai.GenerativeModel("gemini-1.5-flash")

faiss_index_file = "faiss_index.bin"
texts_file = "texts.json"

# تابع شمارش توکن‌ها
def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    return len(tokens)

# بارگذاری یا ایجاد FAISS Index
if os.path.exists(faiss_index_file):
    index = faiss.read_index(faiss_index_file)
    print(f"Loaded FAISS index with {index.ntotal} vectors.")
else:
    index = None
    print("FAISS index not found. A new one will be created when needed.")

# بارگذاری یا ایجاد JSON
if os.path.exists(texts_file):
    with open(texts_file, "r", encoding="utf-8") as f:
        texts = json.load(f)
else:
    texts = []
    print("JSON file not found. A new one will be created when needed.")

def summarize_text():
    global index  # اعلام اینکه از متغیر سراسری index استفاده می‌کنیم
    text = input_text.get("1.0", "end-1c").strip()

    if not text:
        print("Error: No text entered.")
        return

    # محاسبه تعداد توکن‌ها
    num_tokens = count_tokens(text)
    token_count_label.config(text=f"Token count: {num_tokens}")

    # ساخت پرامپت
    prompt = f"""summarize the text(chat) in English within maximum:1024 minimum:700 word, without code, or style, as a report:\n\n{text}"""

    # ارسال درخواست به API و دریافت خلاصه
    try:
        response = model.generate_content(prompt)
        summarized_text = response.text

        # نمایش خلاصه در کنسول
        print("Summarized Text:\n", summarized_text)

        # تولید امبدینگ از متن خلاصه‌شده
        embedding_response = genai.embed_content(model="models/text-embedding-004", content=summarized_text)
        embedding = np.array([embedding_response['embedding']], dtype='float32')

        # ایجاد یا آپدیت FAISS Index
        if index is None:
            dimension = embedding.shape[1]
            index = faiss.IndexFlatL2(dimension)
            print(f"Created a new FAISS index with dimension {dimension}.")

        # اضافه کردن بردار جدید
        index.add(embedding)
        faiss.write_index(index, faiss_index_file)
        index_id = index.ntotal - 1  # ایندکس جدید

        # اضافه کردن به JSON
        new_entry = {
            "index": index_id,
            "content": summarized_text
        }
        texts.append(new_entry)
        with open(texts_file, "w", encoding="utf-8") as f:
            json.dump(texts, f, ensure_ascii=False, indent=2)

        print("Embedding Vector:\n", embedding)
        print(f"Successfully added summarized text and embedding to FAISS and JSON with index {index_id}.")

    except Exception as e:
        print(f"Error processing the text: {e}")

# تابع برای بروزرسانی تعداد توکن‌ها و تغییر رنگ متن
def update_token_count(event=None):
    text = input_text.get("1.0", "end-1c").strip()
    num_tokens = count_tokens(text)
    token_count_label.config(text=f"Token count: {num_tokens}")

    if num_tokens > 950000:
        token_count_label.config(fg="red")
    else:
        token_count_label.config(fg="black")

def on_text_change(event=None):
    if input_text.edit_modified():
        update_token_count()
        input_text.edit_modified(False)

# رابط کاربری با tkinter
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("600x400")

input_label = tk.Label(root, text="Enter text to summarize:")
input_label.pack(pady=10)

input_text = tk.Text(root, height=10, width=60)
input_text.pack(pady=10)
input_text.bind("<KeyRelease>", on_text_change)
input_text.bind("<ButtonRelease-1>", on_text_change)

token_count_label = tk.Label(root, text="Token count: 0")
token_count_label.pack(pady=5)

summarize_button = tk.Button(root, text="Summarize", command=summarize_text)
summarize_button.pack(pady=20)

root.mainloop()
