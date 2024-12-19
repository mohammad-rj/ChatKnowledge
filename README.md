### **ChatKnowledge**

**ChatKnowledge** is a robust and versatile system designed to manage, summarize, and retrieve knowledge from diverse data sources. Whether it's ChatGPT conversations, messenger chats, browser histories, or any other personal datasets, ChatKnowledge enables you to transform scattered information into an organized, searchable knowledge base.

---

### **How It Works**

#### **1. Initial Setup (One-Time)**
1. **Prepare Your Data:**
   - Export your conversations in JSON format and place them in the `chat` folder.
   
2. **Process the Conversations:**
   - Run `main_gpt.py` to convert raw JSON files into structured text files in the `out` folder.
   - Use `export.py` to generate a list of processed conversations for review.

3. **Summarize Conversations:**
   - Run `main.py` to create detailed summaries for each conversation and save them.

4. **Embed and Vectorize Summaries:**
   - Use `faiss_adder_from_files.py` to generate vector embeddings from the summaries and add them to the FAISS database.

#### **2. Adding New Conversations**
- For incremental updates, use `direct_adder.py` to process and add new conversations directly into the database without reprocessing previous data.

#### **3. Search and Retrieve Knowledge**
- Use `faiss_search_ui.py` to perform semantic searches and retrieve relevant knowledge tailored to your queries.

### **Use Cases**
- **Personal Knowledge Base:** Organize and retrieve insights from personal data across platforms.
- **Professional Research:** Aggregate and search through extensive conversation histories for academic or professional projects.
- **Customer Support:** Manage and retrieve historical support chats to improve response accuracy and consistency.
- **Content Creation:** Quickly access and reference past interactions to aid in brainstorming and content generation.

---

### **Why ChatKnowledge?**
ChatKnowledge is a completely free solution for transforming unstructured conversation data into actionable insights. All you need is a free API key from [Google AI Studio](https://aistudio.google.com/apikey) to get started.

With its ability to handle multiple data sources, generate advanced summaries, and provide lightning-fast retrieval, ChatKnowledge delivers exceptional value for both personal and professional use cases, all without spending a single dollar.

---

This version is designed for my personal needs, but I’ve decided to share it here. If you'd like to develop it further or have any questions, feel free to reach out [dev@epid.co](mailto:dev@epid.co). I'm happy to help!
### **License**
This project is licensed under the [MIT License](LICENSE).

