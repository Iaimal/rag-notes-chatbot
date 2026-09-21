# 📚 Notes RAG Chatbot

A chatbot that answers questions using only your own notes and shows which file each answer came from.

**🔗 Live demo:** https://rag-notes-chatbot-egdcv5vmdkt4ufnwdk5g4n.streamlit.app/

## What it does

You ask a question. The app finds the most relevant part of your notes, gives it to a language model, and shows the answer together with the source file and a confidence score. If nothing in the notes is relevant, it says so instead of guessing.

## Features

- Answers grounded in your own text files, not the model's memory
- Source citation with a confidence score for every answer
- A minimum-score check that rejects questions your notes can't answer
- Hand-written text chunking with overlap
- Semantic search with a Chroma vector database
- A chat interface built with Streamlit

## How it works

1. **Chunking:** each note in `notes/` is split into smaller pieces with a hand-written `chunk_text()` function. Long paragraphs are cut into overlapping segments so that no idea is lost at a boundary.
2. **Embedding and storage:** every chunk is turned into a vector with `sentence-transformers` (`all-MiniLM-L6-v2`) and stored in a Chroma vector database, together with its source file name.
3. **Retrieval:** your question is embedded the same way, and Chroma returns the most similar chunk (cosine similarity). If its score is below a minimum threshold, the app answers "I couldn't find anything relevant in your notes."
4. **Generation:** the retrieved chunk and your question are sent to `Qwen2.5-7B-Instruct` through the Hugging Face Inference API, with an instruction to answer only from the given context.
5. **Interface:** a Streamlit chat UI shows the answer with its source file and confidence.

```
Question → embed → Chroma finds the best chunk → score check → LLM answers from that chunk → answer + source
```

## Example questions

The included notes cover a few machine learning topics. Try:

- "What is the attention mechanism in transformers?"
- "How do I stop overfitting?"
- "How does gradient descent work?"
- "Who won the World Cup?" (not in the notes, so the app should say it found nothing relevant)

## Project structure

```
├── app.py            # Streamlit chat interface
├── rag.py            # Builds the prompt and generates the answer
├── search.py         # Chunking, embedding and retrieval (Chroma)
├── notes/            # The text files the chatbot answers from
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
3. Set your Hugging Face token. You need a free access token that is allowed to use Inference Providers:
```
   set HF_TOKEN=your_huggingface_token
```
   On Mac or Linux, use `export HF_TOKEN=your_huggingface_token` instead.
4. Start the app:
```
   python -m streamlit run app.py
```
   It opens at `http://localhost:8501`.

## Use your own notes

Delete the example files in `notes/` and add your own `.txt` files. The app reads every `.txt` file in that folder when it starts.

## Deploy on Streamlit Community Cloud

1. Push the project to a GitHub repo, with `app.py` at the top level and the `notes/` folder included.
2. On share.streamlit.io, create a new app from that repo, with `app.py` as the main file.
3. Under **Advanced settings → Secrets**, add:
```
   HF_TOKEN = "your_huggingface_token"
```
4. Click **Deploy**.

Never commit your token to the repo. It belongs only in Streamlit's Secrets box or in an environment variable.

## Limitations

- It retrieves a single best-matching chunk per question, so answers that need information from several notes can be incomplete.
- The Chroma database lives in memory and is rebuilt every time the app starts, so it isn't saved between restarts.
- Only `.txt` files are supported.
- RAG reduces hallucination but doesn't eliminate it. Always check the source shown.
- The free hosted app goes to sleep after a period without visitors and takes a moment to wake up.

## Possible improvements

- Retrieve several chunks per question instead of one
- Save the vector database to disk
- Support PDF and Markdown files
- Add Docker for containerized deployment
- Evaluate answer quality with a set of test questions

## Built with

Python · Streamlit · sentence-transformers · Chroma · Hugging Face Inference API
