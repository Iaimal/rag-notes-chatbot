# rag.py
from search import search
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "openai/gpt-oss-20b"

def generate_answer(context, question):
    messages = [
        {
            "role": "user",
            "content": (
                "Answer the question using only the context below. "
                "If the context doesn't contain the answer, say so.\n\n"
                f"Context: {context}\n\nQuestion: {question}"
            ),
        }
    ]
    result = client.chat.completions.create(model=MODEL_NAME, messages=messages, max_tokens=400)
    answer = result.choices[0].message.content
    return answer.strip()

def rag_answer(question):
    matches = search(question)
    MIN_SCORE = 0.2

    good_matches = [m for m in matches if m[2] >= MIN_SCORE]

    if not good_matches:
        return "I couldn't find anything relevant in your notes.", None, 0

    context = "\n\n".join(m[1] for m in good_matches)
    sources = list(dict.fromkeys(m[0] for m in good_matches))

    answer = generate_answer(context, question)
    return answer, sources, good_matches[0][2]