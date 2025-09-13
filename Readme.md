# 🚀 Groq Conversation Management & Information Extraction

This project demonstrates advanced conversation management and structured information extraction using the **Groq API’s OpenAI-compatible SDK**.

---

## ✅ Features

- 💬 **Conversation History Management**  
  Manage conversation flow with:
  - Periodic summarization after every _k-th_ turn
  - Character and turn-based truncation
  - Intelligent summary replacement of older messages

- 🧱 **JSON Schema-based Information Extraction**  
  Extract structured personal data from chat conversations, including:
  - Name
  - Email
  - Phone number
  - Location
  - Age

- ✅ **Robust Data Validation**  
  Validates extracted fields (e.g., correct email format, valid age range).

---

## ⚡ Technology Stack

- Python (Standard Libraries)
- OpenAI-compatible Groq SDK
- No external frameworks (e.g., no TensorFlow or PyTorch)

---

## ⚡ Setup Instructions

1️⃣ Clone the repository:
```bash
git clone https://github.com/your-username/groq-conversation-extraction.git
cd groq-conversation-extraction
