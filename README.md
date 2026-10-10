# 📚 Notes RAG Chatbot

A chatbot that answers questions using only your own notes and shows which files each answer came from. It runs as a Streamlit app, and also as a FastAPI service that can be containerized with Docker.

**🔗 Live demo:** https://rag-notes-chatbot-egdcv5vmdkt4ufnwdk5g4n.streamlit.app/

## What it does

You ask a question. The app finds the most relevant parts of your notes — up to three — and gives them to a language model, then shows the answer together with every source file used and a confidence score. If nothing in the notes is relevant, it says so instead of guessing.

## Features

- Answers grounded in your own text files, not the model's memory
- Retrieves multiple chunks per question, so it can combine information from more than one note
- Source citations with a confidence score for every answer
- A minimum-score check that rejects questions your notes can't answer
- Hand-written text chunking with overlap
- Semantic search with a Chroma vector database
- A chat interface built with Streamlit
- A FastAPI `/ask` endpoint, so other programs can call the chatbot
- Docker support for running the API anywhere

## How it works

1. **Chunking:** each note in `notes/` is split into smaller pieces with a hand-written `chunk_text()` function. Long paragraphs are cut into overlapping segments so that no idea is lost at a boundary.
2. **Embedding and storage:** every chunk is turned into a vector with `sentence-transformers` (`all-MiniLM-L6-v2`) and stored in a Chroma vector database, together with its source file name.
3. **Retrieval:** your question is embedded the same way, and Chroma returns the top 3 most similar chunks (cosine similarity). Each is checked against a minimum score threshold, and only the ones that pass are kept. If none pass, the app answers "I couldn't find anything relevant in your notes."
4. **Generation:** the surviving chunks are joined into one context and sent, with your question, to `llama-3.1-8b-instant` through the Groq API, with an instruction to answer only from the given context. This lets the app answer questions that need information from more than one note.
5. **Interface:** a Streamlit chat UI shows the answer with its source files and confidence. The same logic is also exposed as a JSON API through FastAPI.

```
Question → embed → Chroma finds the top 3 chunks → score check on each →
surviving chunks joined into context → LLM answers from that context → answer + sources
```

## Example questions

The included notes cover a few machine learning topics. Try:

- "What is the attention mechanism in transformers?"
- "How do I stop overfitting?"
- "How does gradient descent work?"
- "Compare gradient descent and overfitting" (needs information from two notes)
- "Who won the World Cup?" (not in the notes, so the app should say it found nothing relevant)

## Project structure

```
├── app.py            # Streamlit chat interface
├── api.py            # FastAPI endpoint (POST /ask)
├── rag.py            # Builds the prompt and generates the answer
├── search.py         # Chunking, embedding and retrieval (Chroma)
├── notes/            # The text files the chatbot answers from
├── Dockerfile        # Container recipe for the API
├── .dockerignore     # Files kept out of the Docker image
└── requirements.txt  # Python dependencies
```

## Run it locally

1. Clone the repo and open its folder:
```
   git clone https://github.com/Iaimal/rag-notes-chatbot.git
   cd rag-notes-chatbot
```
2. Install the dependencies:
```
   pip install -r requirements.txt
```
3. Set your Groq API key. You can create a free one at console.groq.com:
```
   set GROQ_API_KEY=your_groq_key
```
   On Mac or Linux, use `export GROQ_API_KEY=your_groq_key` instead.
4. Start the Streamlit app:
```
   python -m streamlit run app.py
```
   It opens at `http://localhost:8501`.

## Run it as an API

To run the FastAPI service without Docker:
```
python -m uvicorn api:app --reload
```
Then open `http://127.0.0.1:8000/docs` to try the `/ask` endpoint from your browser.

## Run it with Docker

1. Build the image:
```
   docker build -t rag-api .
```
2. Run the container, passing your key at run time (it is never stored in the image):
```
   docker run -p 8000:8000 -e GROQ_API_KEY=your_groq_key rag-api
```
3. Open `http://127.0.0.1:8000/docs` and try the `/ask` endpoint, or call it directly:
```
   curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"What is overfitting?\"}"
```

The response is JSON with the answer, the source files used, and the similarity score:
```
{"answer": "...", "sources": ["overfitting.txt"], "score": 0.78}
```

## Use your own notes

Delete the example files in `notes/` and add your own `.txt` files. The app reads every `.txt` file in that folder when it starts.

## Deploy on Streamlit Community Cloud

1. Push the project to a GitHub repo, with `app.py` at the top level and the `notes/` folder included.
2. On share.streamlit.io, create a new app from that repo, with `app.py` as the main file.
3. Under **Advanced settings → Secrets**, add:
```
   GROQ_API_KEY = "your_groq_key"
```
4. Click **Deploy**.

Never commit your key to the repo. It belongs only in Streamlit's Secrets box or in an environment variable.

## Limitations

- It retrieves up to 3 chunks per question, so a question needing information from more than 3 notes may still be incomplete.
- The Chroma database lives in memory and is rebuilt every time the app starts, so it isn't saved between restarts.
- Only `.txt` files are supported.
- RAG reduces hallucination but doesn't eliminate it. Always check the sources shown.
- It has no memory of earlier questions in the conversation; each question is answered independently.
- Depends on a hosted model through the Groq API. Model availability and free-tier limits can change, which may require updating the model name in `rag.py`.
- The free hosted app goes to sleep after a period without visitors and takes a moment to wake up.

## Possible improvements

- Rerank retrieved chunks before sending them to the LLM
- Save the vector database to disk
- Support PDF and Markdown files
- Add conversation memory for follow-up questions
- Evaluate answer quality with a set of test questions

## Built with

Python · Streamlit · FastAPI · Docker · sentence-transformers · Chroma · Groq