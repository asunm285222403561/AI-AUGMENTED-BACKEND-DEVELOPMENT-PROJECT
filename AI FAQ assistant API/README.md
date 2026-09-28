# 🤖 AI FAQ Assistant API

A smart, fast, and scalable FAQ Assistant API built with **FastAPI** and **Google Gemini AI**.

It offers **zero-latency responses** for commonly asked questions from a pre-defined knowledge base and seamlessly falls back to **Google Gemini AI** for any unanswered or dynamic questions!

---

## ✨ Features

- ⚡ **Lightning Fast**: Built on FastAPI and Uvicorn.
- 📚 **Knowledge Base**: Pre-loaded with 24+ common programming and tech questions.
- 🧠 **AI Fallback**: Automatically queries **Gemini 2.5 Flash** when a question isn't in the FAQ database.
- 📖 **Interactive API Docs**: Built-in Swagger UI at `/docs` and ReDoc at `/redoc`.
- 🛡️ **Environment Secured**: Uses `.env` to protect your API keys.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Server:** Uvicorn
- **AI Model:** Google Gemini API (`google-genai`)
- **Data Validation:** Pydantic
- **Environment Management:** Python Dotenv

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-FAQ-Assistant-API.git
cd "AI FAQ assistant API"
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your free Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
   > 💡 *Don't have a key? Get one completely free from [Google AI Studio](https://aistudio.google.com/).*

### 4. Run the API
```bash
uvicorn main:app --reload
```

Server will start at: `http://127.0.0.1:8000`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Welcome message & API metadata |
| `GET` | `/faqs` | List all available FAQs in database |
| `POST` | `/ask` | Ask any question (FAQ check + AI fallback) |

---

## 🧪 Example Usage

### 1. Ask a question found in FAQ
**Request:**
```http
POST /ask
Content-Type: application/json

{
  "question": "what is fastapi"
}
```

**Response:**
```json
{
  "question": "what is fastapi",
  "answer": "FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints.",
  "source": "FAQ Database"
}
```

---

### 2. Ask a question NOT in FAQ (AI Response)
**Request:**
```http
POST /ask
Content-Type: application/json

{
  "question": "What is the difference between synchronous and asynchronous code?"
}
```

**Response:**
```json
{
  "question": "What is the difference between synchronous and asynchronous code?",
  "answer": "Synchronous code executes sequentially, blocking subsequent tasks until the current one finishes. Asynchronous code allows tasks to execute concurrently without blocking the main execution thread.",
  "source": "Gemini AI"
}
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
