import os
import time
import csv
from datetime import datetime
import google.generativeai as genai

# تنظیمات API
genai.configure(api_key="aaa")
model = genai.GenerativeModel("gemini-1.5-flash")

# مسیر پوشه‌ها و فایل‌ها
input_folder = "output"
output_folder = "output_summ"
file_info_csv = "file_info.csv"
index_file = "index.txt"

# اطمینان از وجود پوشه خروجی
os.makedirs(output_folder, exist_ok=True)

# محدودیت‌ها
max_requests_per_minute = 15
min_interval_between_requests = 5  # ثانیه

# خواندن اندیس فعلی
if os.path.exists(index_file):
    with open(index_file, "r") as f:
        start_index = int(f.read().strip())
else:
    start_index = 0

# خواندن اطلاعات فایل‌ها از CSV
with open(file_info_csv, "r", encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # رد کردن عنوان ستون‌ها
    file_info = list(csvreader)

# پردازش فایل‌ها از اندیس ذخیره شده
requests_sent = 0
start_time = time.time()

for idx, (file_path, _) in enumerate(file_info[start_index:], start=start_index):
    # چاپ اندیس و نام فایل
    print(f"Processing Index: {idx}, File: {file_path}")

    # خواندن فایل
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        continue

    # تعیین تاریخ ساخت فایل
    try:
        creation_time = os.path.getctime(file_path)
    except Exception as e:
        print(f"Error getting creation date for {file_path}: {e}")
        continue

    # ساختن پرامپت
    prompt = f"""summarize the text(chat) in English within maximum:1024 minimum:700 word, without code, or style, as a report:\n\n{text}"""

    # ارسال به API
    try:
        response = model.generate_content(prompt)
        summarized_text = response.text
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        continue

    # ذخیره نتیجه در فایل جدید
    output_file = os.path.basename(file_path)
    output_path = os.path.join(output_folder, output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summarized_text)

    # تنظیم تاریخ ساخت فایل خروجی
    try:
        os.utime(output_path, (creation_time, creation_time))
    except Exception as e:
        print(f"Error setting creation date for {output_path}: {e}")

    # به‌روز کردن اندیس ذخیره شده
    with open(index_file, "w") as f:
        f.write(str(idx + 1))

    # بررسی محدودیت زمانی
    requests_sent += 1
    elapsed_time = time.time() - start_time
    if requests_sent >= max_requests_per_minute:
        if elapsed_time < 60:
            time.sleep(60 - elapsed_time)  # صبر تا انتهای دقیقه
        requests_sent = 0
        start_time = time.time()
    else:
        while time.time() - start_time < requests_sent * min_interval_between_requests:
            time.sleep(0.1)

print("Processing complete.")
