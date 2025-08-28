from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

DEFAULT_PROMPT = """
You are an AI Assignment Generator. Always write a detailed academic assignment 
with the following structure:

### Assignment Title: (Auto-generate a clear and professional title)

#### 1. Introduction (200–300 words)
- Define the core concept.
- Explain its importance and relevance in the subject area.

#### 2. Theoretical Background (300–400 words)
- Explain the history or background of the concept.
- Discuss the key theories, definitions, and related principles.

#### 3. Main Content (1000–1200 words)
- Break down the topic into multiple sub-sections.
- For each sub-section:
  - Definition / Explanation
  - Algorithms / Methods (if applicable)
  - Advantages & Disadvantages
  - Real-life Applications
  - Coding Example in Python (if related to computing/data)
  
#### 4. Case Study or Practical Example (400–500 words)
- Provide a practical or real-world case study.
- Demonstrate how the concept/technique is applied.

#### 5. Conclusion (150–250 words)
- Summarize the key learnings.
- Highlight future implications.

#### 6. References (Optional)
- List a few references in APA/MLA format (can be simulated).

**Note**: Make sure the writing style is academic, formal, and detailed.
"""


load_dotenv()

app = Flask(__name__)
CORS(app)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")  # Home route
def home():
    return "Hello! Flask is running 🚀 + OPENAI is running"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_question = data.get("prompt", "").strip()

    full_prompt = f"{DEFAULT_PROMPT}\n\nNow create an assignment on the topic: {user_question}"

    if not user_question:
        return jsonify({"error":"no question recieved"}),400
        
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            { "role":"system","content": "You are a helpful academic assistant. "},
            {"role":"user","content": full_prompt}

        ],
        max_tokens=2000
    )

    assignement_text = response.choices[0].message.content
    return jsonify({"assignment": assignement_text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

