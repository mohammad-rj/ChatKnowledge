import os

def search_in_files(directory, search_text):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if search_text in f.read():
                            print(f"Found in: {file_path}")
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")

# تنظیمات
directory_path = "output"
text_to_search = " hi"

search_in_files(directory_path, text_to_search)
