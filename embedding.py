import json

import google.generativeai as genai
genai.configure(api_key="aaa")

text = """	This report details the analysis and enhancement of a webpage's design, ... test text
"""
result = genai.embed_content(model="models/text-embedding-004", content=text)
print(result['embedding'])

# texts = [
#     """This report details the analysis and enhancement of a webpage's design, focusing on improving the user interface (UI) for touch devices. The initial webpage design is a visually appealing, dark-themed single page featuring a central quote, a particle background effect, and a right-side sidebar accessed via a button. The sidebar contains personal information, social media links, and a recent activity section.  The webpage utilizes advanced CSS and JavaScript, including Three.js for the background animation and custom shaders to create a dynamic visual experience.  The primary concern was enhancing the sidebar accessibility on touch devices.""",
#     """The original HTML structure is well-organized, using semantic HTML5 tags, including specific meta tags for various screen sizes and favicons.  The styling uses CSS to create a visually engaging design, employing a dark color scheme (#010811 background), a linear gradient background image, and custom fonts ('Spectral SC' and 'Montserrat Variable'). The sidebar is implemented using CSS positioning (`position: fixed`) and JavaScript to control its visibility and width (250px when open, 0px when closed).  The toggle mechanism originally utilized a button click event to show and hide the sidebar, relying on JavaScript for dynamic modification of CSS properties.""",
# ]
#
# # تابع برای تبدیل متون به Embedding
# def embed_texts(text_list):
#     embeddings = genai.embed_content(model="models/text-embedding-004", content=text_list)
#     return embeddings['embedding']
#
# # تبدیل تمام متون
# all_embeddings = embed_texts(texts)
#
# # ذخیره Embeddingها در یک فایل JSON
# with open("embeddings.json", "w", encoding='utf-8') as f:
#     json.dump({"texts": texts, "embeddings": all_embeddings}, f, ensure_ascii=False, indent=4)
#
# print("تبدیل و ذخیره Embeddingها با موفقیت انجام شد.")