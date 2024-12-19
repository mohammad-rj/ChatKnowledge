import os
import csv
from datetime import datetime

# مسیر پوشه ورودی
input_folder = "output/"

# فایل خروجی CSV
output_csv = "file_info.csv"

# استخراج اطلاعات فایل‌ها
file_info = []
files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
for file in files:
    file_path = os.path.join(input_folder, file)
    creation_time = os.path.getctime(file_path)
    creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
    file_info.append((file_path, creation_date))

# ذخیره اطلاعات در فایل CSV
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["File Path", "Creation Date"])
    csvwriter.writerows(file_info)

print(f"File information has been saved to {output_csv}")
