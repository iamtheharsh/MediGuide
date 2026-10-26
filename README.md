# 🩺 MediGuide – AI Health Assistant

An **AI-powered medical assistant** that helps users get **accurate, compassionate, and multilingual health advice** (English, Hindi, Hinglish).  
Built as part of the **Software Engineer Assignment**.

---

## 👤 Author
**Harsh Patel**  
- 🎓 B.Tech, IIT (BHU), Varanasi (2027)  


---

## 🚀 Features
- 🔑 Secure **JWT Authentication** (Register/Login).  
- 💬 Chat UI built with **Streamlit**.  
- 📚 Retrieval-Augmented Generation (RAG) pipeline using **Gale Encyclopedia of Medicine**.  
- 🌐 Multilingual responses (English / Hindi / Hinglish).  
- 🗂️ **MongoDB**-based conversation history.  
- 🤝 Doctor-style answers: warm, clear, and fact-based.  

---

## 🛠️ Tech Stack
- **Frontend**: Streamlit  
- **Backend**: FastAPI  
- **Database**: MongoDB  
- **Vector Store**: FAISS  
- **LLM**: Groq (LLaMA-3.1-8B Instant)  
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)  
- **Auth**: JWT (`python-jose`, `passlib`)  

---
## 📂 Project Structure

```plaintext
.
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend
├── auth.py             # JWT auth & password hashing
├── database.py         # MongoDB operations
├── memory_llm.py       # Vector embedding pipeline
├── vectorstore/        # FAISS index
├── data/               # Knowledge base PDFs
└── README.md           # Project documentation


⚡ Getting Started
1. Clone Repo
git clone https://github.com/iamtheharsh/MediGuide.git
cd MediGuide

2. Install Dependencies
pip install -r requirements.txt

3. Set Environment Variables

Create a .env file in the project root:

MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
PRIMARY_GROQ_API_KEY=your-groq-key
FALLBACK_GROQ_API_KEY=your-backup-key

4. Run Backend
uvicorn main:app --reload

5. Run Frontend
streamlit run app.py
