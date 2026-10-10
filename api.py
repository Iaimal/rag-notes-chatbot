# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from rag import rag_answer

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    answer, sources, score = rag_answer(q.question)
    return {"answer": answer, "sources": sources, "score": score}