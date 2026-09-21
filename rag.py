# rag.py
from search import search
from huggingface_hub import InferenceClient
import os
client = InferenceClient(model="Qwen/Qwen2.5-7B-Instruct", provider="featherless-ai", token=os.environ.get("HF_TOKEN"))

def generate_answer(context, question):
    messages = [
        {
            "role": "user",
            "content": f"Answer the question using only the context below. If the context doesn't contain the answer, say so.\n\nContext: {context}\n\nQuestion: {question}"
        }
    ]
    result = client.chat_completion(messages=messages, max_tokens=60)
    answer = result.choices[0].message.content
    return answer.strip()
def rag_answer(question):
    filename, content, score = search(question)
    MIN_SCORE = 0.2

    if score < MIN_SCORE:
        return "I couldn't find anything relevant in your notes.", None, score

    answer = generate_answer(content, question)
    return answer, filename, score