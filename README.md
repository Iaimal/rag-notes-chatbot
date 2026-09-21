# 📚 Notes RAG Chatbot

A chatbot that answers questions using only your own notes, and shows which file each answer came from.

**🔗 Live demo:** https://rag-notes-chatbot-egdcv5vmdkt4ufnwdk5g4n.streamlit.app/

## What it does

You ask a question. The app finds the most relevant part of your notes, gives it to a language model, and shows the answer along with the source file and a confidence score. If nothing in the notes is relevant, it says so instead of guessing.

## How it works

1. **Chunking:** each note in `notes/` is split into smaller pieces with a hand-written `chunk_text()` function.
2. **Embedding:** every chunk is turned into a vector with `sentence-transformers` (`all-MiniLM-L6-v2`).
3. **Retrieval:** your question is embedded the same way, and the most similar chunk is picked. If its score is below a minimum threshold, the app answers "I couldn't find anything relevant in your notes."
4. **Generation:** the retrieved chunk and your question are sent to `Qwen2.5-7B-Instruct` through the Hugging Face Inference API, with an instruction to answer only from the given context.
5. **Interface:** a Streamlit chat UI shows the answer with its source file and confidence.

## Project structure

```
├── app.py            # Streamlit chat interface
├── rag.py            # Builds the prompt and generates the answer
├── search.py         # Chunking, embedding and retrieval
├── notes/            # The text files the chatbot answers from
└── requirements.txt
```

## Run it locally

```
pip install -r requirements.txt
set HF_TOKEN=your_huggingface_token
streamlit run app.py
```

On Mac or Linux, use `export HF_TOKEN=your_huggingface_token` instead of `set`.

You need a free Hugging Face access token that is allowed to use Inference Providers.

## Limitations

- It retrieves a single best-matching chunk per question, so answers that need several notes can be incomplete.
- Retrieval is a plain in-memory search, not a vector database.
- RAG reduces hallucination but doesn't eliminate it. Always check the source shown.

## Built with

Python · Streamlit · sentence-transformers · Hugging Face Inference API
