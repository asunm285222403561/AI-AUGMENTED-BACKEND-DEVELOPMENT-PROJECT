import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI App
app = FastAPI(
    title="AI FAQ Assistant API",
    description="An intelligent FAQ assistant API with instant FAQ answers and Gemini AI fallback.",
    version="1.0.0"
)

# Request schema
class QueryRequest(BaseModel):
    question: str

# 1. Expanded Knowledge Base / FAQ Database (24 common questions)
faqs = {
    # Programming Languages
    "what is python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
    "what is html": "HTML (HyperText Markup Language) is the standard markup language used to structure web pages.",
    "what is css": "CSS (Cascading Style Sheets) is used to style and layout web pages (colors, fonts, spacing).",
    "what is javascript": "JavaScript is a versatile programming language used to create dynamic and interactive web pages.",
    "what is java": "Java is a popular, class-based, object-oriented programming language designed for platform independence.",
    "what is c++": "C++ is a high-performance, compiled programming language widely used in system/software development and game design.",
    
    # Databases & Backend
    "what is dbms": "DBMS (Database Management System) is software used to store, manage, and retrieve data securely.",
    "what is sql": "SQL (Structured Query Language) is used to interact with relational databases (queries, updates, schema).",
    "what is nosql": "NoSQL refers to non-relational databases designed for flexible schemas and horizontal scaling (e.g. MongoDB).",
    "what is fastapi": "FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints.",
    "what is api": "API (Application Programming Interface) is a set of rules allowing different software applications to communicate.",
    "what is rest api": "REST API is an architectural style for web services that uses HTTP methods (GET, POST, PUT, DELETE).",
    "what is backend": "Backend refers to the server-side architecture handling business logic, database operations, and APIs.",
    "what is frontend": "Frontend refers to the client-facing part of a web or mobile application that users interact with.",
    
    # Version Control & Tools
    "what is git": "Git is a distributed version control system for tracking source code changes during software development.",
    "what is github": "GitHub is a cloud-based hosting service that lets developers store, manage, and collaborate on Git repositories.",
    "what is docker": "Docker is a containerization platform that packages applications and dependencies together for consistent execution.",
    "what is uvicorn": "Uvicorn is a lightning-fast ASGI web server implementation for Python, commonly used with FastAPI.",
    
    # Artificial Intelligence & Concepts
    "what is ai": "AI (Artificial Intelligence) refers to machines engineered to simulate human intelligence and problem solving.",
    "what is machine learning": "Machine Learning is a subset of AI where algorithms learn patterns from data to make predictions.",
    "what is deep learning": "Deep Learning is a specialized branch of Machine Learning based on multi-layered artificial neural networks.",
    "what is nlp": "NLP (Natural Language Processing) is an AI domain focused on enabling computers to understand human language.",
    "what is cloud computing": "Cloud computing provides on-demand computing services (servers, storage, networking) over the internet.",
    "what is devops": "DevOps combines development and IT operations to shorten the systems development lifecycle with high quality."
}

def ask_gemini_ai(prompt: str) -> tuple[str, str]:
    """Helper function to fetch an answer from Google Gemini when question is not in FAQ."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or "your_" in api_key.lower():
        return (
            "This question is not in the FAQ database. "
            "To get live AI answers, please add your free Gemini API key to the .env file! "
            "(Get a free key from https://aistudio.google.com/)",
            "FAQ Fallback (No Key)"
        )
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"You are a helpful and concise technical assistant. Answer this question clearly in 2-4 sentences: {prompt}"
        )
        if response.text:
            return response.text.strip(), "Gemini AI"
        return "Could not generate an AI response for this question.", "Gemini AI"
    except Exception as e:
        err_str = str(e)
        if "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
            return (
                "The GEMINI_API_KEY in your .env file is invalid. Please get a free valid key from https://aistudio.google.com/",
                "Gemini AI (Invalid Key)"
            )
        return f"AI Error: {err_str}", "Gemini AI (Error)"

# --- API Endpoints ---

@app.get("/")
def home():
    """Root endpoint welcoming users and displaying API metadata."""
    return {
        "project": "AI FAQ Assistant API",
        "status": "Online",
        "total_faqs": len(faqs),
        "docs_url": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "GET /faqs": "List all FAQ questions and answers",
            "POST /ask": "Ask a question (returns FAQ answer or AI response)"
        }
    }

@app.get("/faqs")
def get_all_faqs():
    """Retrieve all available FAQs in the database."""
    return {
        "count": len(faqs),
        "faqs": faqs
    }

@app.post("/ask")
def ask_question(payload: QueryRequest):
    """
    Main endpoint:
    1. Checks if question matches the FAQ database.
    2. If found -> Returns pre-defined FAQ answer (Fast & 0 cost).
    3. If not found -> Queries Gemini AI dynamically.
    """
    query_text = payload.question.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Clean the input (lowercase, remove trailing question marks and extra spaces)
    normalized = query_text.lower().rstrip("?").strip()

    # 1. Check local FAQ database (Exact match)
    if normalized in faqs:
        return {
            "question": payload.question,
            "answer": faqs[normalized],
            "source": "FAQ Database"
        }

    # Also check if any FAQ key is closely contained in the question
    for key, ans in faqs.items():
        if key in normalized:
            return {
                "question": payload.question,
                "answer": ans,
                "source": "FAQ Database (Matched)"
            }

    # 2. Not in FAQ -> Fallback to Gemini AI
    ai_answer, source = ask_gemini_ai(query_text)
    return {
        "question": payload.question,
        "answer": ai_answer,
        "source": source
    }

# --- Direct Run Support for VS Code ---
if __name__ == "__main__":
    import sys
    import uvicorn
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("\n" + "=" * 60)
    print("AI FAQ ASSISTANT API IS RUNNING!")
    print("Open your browser at: http://127.0.0.1:8000/docs")
    print("=" * 60 + "\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

