import sys
import os

# Ensure safe UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass

from main import faqs, ask_gemini_ai

def run():
    print("\n" + "=" * 55)
    print("AI FAQ Assistant - Terminal Interactive Mode")
    print("Ask any question to get an instant answer.")
    print("Type 'exit' to quit.")
    print("=" * 55 + "\n")
    
    while True:
        try:
            query = input("Enter your question: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "q"]:
                print("Bye!")
                break
                
            normalized = query.lower().rstrip("?").strip()
            
            # Check local FAQ
            if normalized in faqs:
                print(f"\n[Answer]: {faqs[normalized]}")
                print("[Source]: FAQ Database\n" + "-" * 50)
                continue
                
            matched = False
            for key, ans in faqs.items():
                if key in normalized:
                    print(f"\n[Answer]: {ans}")
                    print("[Source]: FAQ Database (Matched)\n" + "-" * 50)
                    matched = True
                    break
                    
            if not matched:
                ai_answer, source = ask_gemini_ai(query)
                print(f"\n[Answer]: {ai_answer}")
                print(f"[Source]: {source}\n" + "-" * 50)
                
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

if __name__ == "__main__":
    run()
