import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_selenium():
    # تنظیم Geckodriver برای فایرفاکس
    geckodriver_path = r"geckodriver.exe"  # مسیر Geckodriver را بررسی کنید
    driver = webdriver.Firefox(service=Service(geckodriver_path))
    return driver

# مسیر فایل HTML
html_file_path = "file:///C:/Users/Epid/Documents/dev/scripts/chatgpt%20manage/chat/chat.html"

# راه‌اندازی Selenium با Firefox
driver = setup_selenium()

# فایل CSV برای ذخیره گزارش
csv_file_name = "conversation_report.csv"

# نوشتن هدر فایل CSV
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Index", "Title", "Content", "Has_Keyword"])

    try:
        # باز کردن فایل HTML
        driver.get(html_file_path)
        time.sleep(2)  # صبر برای بارگذاری کامل محتوا

        # پیدا کردن همه تگ‌های conversation
        conversations = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.conversation"))
        )
        print(f"📊 تعداد conversation ها: {len(conversations)}")

        # کلمات کلیدی برای بررسی
        keywords = ["a1 ", " a2", "b1", "b2"]

        # پردازش و ذخیره‌سازی هر conversation
        for idx, conv in enumerate(conversations):
            try:
                # استخراج عنوان
                title_element = conv.find_element(By.TAG_NAME, "h4")
                title = title_element.text.strip() if title_element else f"conversation_{idx}"

                # استخراج محتوا
                content = conv.text.strip()

                # بررسی وجود کلمات کلیدی
                has_keyword = any(keyword in content for keyword in keywords)
                prefix = "^" if has_keyword else ""
                filename = f"{prefix}{title.replace(' ', '_')}.txt"

                # ذخیره محتوا در فایل متنی
                with open(filename, "w", encoding="utf-8") as text_file:
                    text_file.write(content)

                # نوشتن در فایل CSV
                writer.writerow([idx, title, content[:50] + "...", has_keyword])

                # چاپ لوگ
                print(f"[{idx}] ذخیره شد: {filename}")

            except Exception as e:
                print(f"❌ خطا در پردازش conversation {idx}: {e}")
                writer.writerow([idx, "Error", "Could not extract content", False])

    except Exception as e:
        print(f"❌ خطا در یافتن conversation ها: {e}")

    finally:
        driver.quit()

print(f"\n✅ اطلاعات در فایل {csv_file_name} ذخیره شد!")
