import google.generativeai as genai

genai.configure(api_key="aaa")
model = genai.GenerativeModel("gemini-1.5-flash")
text = (r"""
من gitlab رو ردیف کردم روی zero trust کلودفلر
آماده طراحی و پیش برد پروژه هستم
کلنگ استارت کار رو از کجا بزنم ؟

""")
prompt = r"""summarize the text(chat) in English within maximum:1024 minimum:700 word, whit out code,or style, as a report: 
""" + text
response = model.generate_content(prompt)
print(response.text)
