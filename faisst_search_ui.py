import faiss
import numpy as np
import google.generativeai as genai
import json
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, Frame, VERTICAL, HORIZONTAL, RIGHT, Y, BOTTOM, X, END, LEFT, BOTH, ttk
from prettytable import PrettyTable
import tiktoken
import pyperclip

# پیکربندی Google Generative AI
genai.configure(api_key="aaa")

# فایل‌های ذخیره‌سازی
faiss_index_file = "faiss_index.bin"
texts_file = "texts.json"

# بارگذاری FAISS Index
index = faiss.read_index(faiss_index_file)
# print(f"Number of vectors in the loaded index: {index.ntotal}")

# بارگذاری فایل متون
with open(texts_file, "r", encoding="utf-8") as f:
    texts = json.load(f)

# مدل لیمیت‌ها
model_limits = {
    "o & mini": 4096,
    "o1 & mini": 16385,
    "gemini-1.5-flash": 1000000
}

# ایجاد توکنایزر برای مدل‌ها
tokenizer = tiktoken.get_encoding("cl100k_base")

# تابع جستجو
def search_query(event=None):
    query_text = query_entry.get("1.0", END).strip()
    k = int(k_entry.get())

    # تولید Embedding
    result = genai.embed_content(model="models/text-embedding-004", content=query_text)
    query_embedding = np.array([result['embedding']], dtype='float32')

    # جستجوی نزدیک‌ترین بردارها
    distances, indices = index.search(query_embedding, k)

    # نمایش جدول نتایج
    for i in results_table.get_children():
        results_table.delete(i)
    for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
        if idx != -1:
            results_table.insert("", "end", values=(f"Result {i+1}", idx, f"{dist:.4f}"))

    # نمایش متن‌ها و محاسبه توکن‌ها
    content_text.delete(1.0, END)
    total_tokens = 0
    for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
        if idx != -1:
            text = texts[idx]["content"]
            tokens = len(tokenizer.encode(text))
            total_tokens += tokens
            content_text.insert(END, f"\nResult {i+1}:\n{text}\n\n")

    # محاسبه باقی‌مانده توکن‌ها و اضافه کردن به جدول مدل‌ها
    average_tokens_per_word = 1.4  # میانگین توکن‌ها برای هر کلمه
    for i in model_table.get_children():
        model_table.delete(i)
    for model, limit in model_limits.items():
        remaining_tokens = max(0, limit - total_tokens)
        remaining_words = int(remaining_tokens / average_tokens_per_word)  # محاسبه تعداد کلمات باقی‌مانده
        model_table.insert("", "end", values=(model, limit, remaining_tokens, remaining_words))

    # محاسبه اطلاعات تعداد کاراکترها، توکن‌ها و کلمات
    total_chars = sum(len(texts[idx]["content"]) for idx in indices[0] if idx != -1)
    total_words = sum(len(texts[idx]["content"].split()) for idx in indices[0] if idx != -1)

    # نمایش اطلاعات در لیبل
    result_info_label.config(text=f"Characters: {total_chars} | Tokens: {total_tokens} | Words: {total_words}")

# تابع کپی به کلیپ‌بورد
def copy_to_clipboard():
    content = content_text.get(1.0, END).strip()
    pyperclip.copy(content)
    # print("Related Texts copied to clipboard.")

# رابط کاربری
root = Tk()
root.title("Semantic Search")
root.geometry("900x700")
root.configure(bg="#f7f7f7")

# استایل‌ها
label_font = ("Arial", 12, "bold")
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# قسمت بالایی برای ورود اطلاعات
query_frame = Frame(root, bg="#f7f7f7")
query_frame.pack(pady=10, padx=10, fill=X)

# نمایش تعداد وکتورها
vector_count_label = Label(query_frame, text=f"Number of vectors in the loaded index: {index.ntotal}", font=entry_font, bg="#f7f7f7")
vector_count_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

# نمایش اطلاعات ریزالت‌ها
result_info_label = Label(query_frame, text="", font=entry_font, bg="#f7f7f7")
result_info_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)

Label(query_frame, text="Query Text:", font=label_font, bg="#f7f7f7").grid(row=0, column=0, sticky="w", padx=5, pady=5)
query_entry = Text(query_frame, wrap="word", height=4, font=entry_font)
query_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

Label(query_frame, text="Number of Results (k):", font=label_font, bg="#f7f7f7").grid(row=2, column=0, sticky="w", padx=5, pady=5)
k_entry = Entry(query_frame, font=entry_font, width=10)
k_entry.insert(0, "5")
k_entry.grid(row=3, column=0, padx=5, pady=5, sticky="w")

Button(query_frame, text="Search", font=button_font, bg="#4CAF50", fg="white", command=search_query).grid(row=4, column=0, pady=10, sticky="w")

# فریم برای جدول‌ها
tables_frame = Frame(root, bg="#f7f7f7")
tables_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

# جدول مدل‌ها
Label(tables_frame, text="Model Limits:", font=label_font, bg="#f7f7f7").grid(row=0, column=0, sticky="w", padx=5, pady=5)
model_table = ttk.Treeview(tables_frame, columns=("Model", "Limit", "Remaining Tokens", "Remaining Words"), show="headings", height=8)
model_table.heading("Model", text="Model")
model_table.heading("Limit", text="Limit")
model_table.heading("Remaining Tokens", text="Remaining Tokens")
model_table.heading("Remaining Words", text="Remaining Words")
model_table.column("Model", width=110, anchor="center")
model_table.column("Limit", width=110, anchor="center")
model_table.column("Remaining Tokens", width=110, anchor="center")
model_table.column("Remaining Words", width=110, anchor="center")
model_table.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# جدول نتایج
Label(tables_frame, text="Results Table:", font=label_font, bg="#f7f7f7").grid(row=0, column=1, sticky="w", padx=5, pady=5)
results_table = ttk.Treeview(tables_frame, columns=("Result", "Index", "Distance"), show="headings", height=8)
results_table.heading("Result", text="Result")
results_table.heading("Index", text="Index")
results_table.heading("Distance", text="Distance")
results_table.column("Result", width=110, anchor="center")
results_table.column("Index", width=110, anchor="center")
results_table.column("Distance", width=110, anchor="center")

results_table.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# فریم برای متن‌ها
content_frame = Frame(root, bg="#f7f7f7")
content_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)
Label(content_frame, text="Related Texts:", font=label_font, bg="#f7f7f7").pack(anchor="w")
content_text = Text(content_frame, wrap="word", height=15, font=entry_font, bg="#ffffff", relief="groove")
content_text.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

# دکمه کپی برای متن مرتبط
copy_icon_button = Button(content_frame, text="📋", font=button_font, bg="#4CAF50", fg="white", command=copy_to_clipboard)
copy_icon_button.pack(side=RIGHT, padx=5, pady=5)

# اسکرول متن‌ها
scroll_y_content = Scrollbar(content_frame, orient=VERTICAL, command=content_text.yview)
scroll_y_content.pack(side=RIGHT, fill=Y)
content_text.config(yscrollcommand=scroll_y_content.set)

# دکمه کپی به کلیپ‌بورد
Button(root, text="Copy Related Texts", font=button_font, bg="#4CAF50", fg="white", command=copy_to_clipboard).pack(pady=10)

# شبیه‌سازی دکمه Enter برای عملکرد دکمه Search
root.bind('<Return>', search_query)

root.mainloop()