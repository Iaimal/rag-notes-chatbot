# rag.py
from search import search
from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    model="Qwen/Qwen2.5-7B-Instruct",
    provider="featherless-ai",
    token=os.environ.get("HF_TOKEN"),
)

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
    result = client.chat_completion(messages=messages, max_tokens=250)
    answer = result.choices[0].message.content
    return answer.strip()

def rag_answer(question):
    matches = search(question)
    MIN_SCORE = 0.2

    good_matches = [m for m in matches if m[2] >= MIN_SCORE]

    if not good_matches:
        return "I couldn't find anything relevant in your notes.", None, 0

    context = "\n\n".join(m[1] for m in good_matches)
    sources = [m[0] for m in good_matches]

    answer = generate_answer(context, question)
    return answer, sources, good_matches[0][2]