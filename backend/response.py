"""RAG response module.

Provides `query_rag(query, top_k=3)` which retrieves nearest chunks from
the FAISS index and asks the OpenAI API to generate an answer grounded in
those chunks.

Quick run (interactive):

PowerShell:
$env:OPENAI_API_KEY = "your_api_key_here"
python -m backend.response

Or run the module directly:
python backend/response.py
"""

import os
from openai import OpenAI
import numpy as np
import embedding
import vector_store

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def query_rag(query, top_k=3):
    query_emb = np.array(
        [embedding.get_embeddings(query)],
        dtype="float32"
    )

    distances, indices = vector_store.index.search(query_emb, top_k)

    retrieved_texts = [
        embedding.chunk_to_text(embedding.index_to_chunk[i])
        for i in indices[0]
    ]

    context = "\n\n".join(retrieved_texts)

    prompt = f"""
    You are an expert analyst. Answer the following question using ONLY the context below.
    If the answer is not in the context, say "Not available in the document."

    Context:
    {context}

    Question:
    {query}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        answer = query_rag(query)
        print("\nAnswer:\n", answer)
        print("="*50)
