import os
import groq
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "You are a document assistant. Answer the user's question using only the "
    "context provided from the document. Be concise and accurate. If the answer "
    'is not found in the context, say "I couldn\'t find this in the document."'
)


def generate_answer(retrieved_pages, query):
    """
    Streams an AI-generated answer using Groq Mixtral.

    Args:
        retrieved_pages: List of page dicts (from retrieve_pages).
        query: User's question string.

    Yields:
        Streamed text chunks from the LLM response.
    """
    # Load from local .env file
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        yield "Error: GROQ_API_KEY is not found in your local .env file."
        return

    client = groq.Groq(api_key=api_key)

    # Build context string with page labels
    context = "\n\n".join(
        f"[Page {p['page']}]\n{p['text']}" for p in retrieved_pages
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Context from the document:\n\n{context}\n\n"
                f"Question: {query}"
            ),
        },
    ]

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=512,
        temperature=0.2,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content
