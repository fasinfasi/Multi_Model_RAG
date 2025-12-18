import numpy as np
import embedding
import vector_store
import embedding
from openai import OpenAI
import os

def query_rag(query, top_k=3):
    query_emb = np.array([embedding.get_embeddings(query)]).astype("float32")

    distances, indices = vector_store.index.search(query_emb, top_k)
    retreived_texts = [embedding.chunk_to_text(embedding.index_to_chunk[i]) for i in indices[0]]

    context = "\n\n".join(retreived_texts)

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
        messages=[{"role":"user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    while True:
        q = input("Enter your query (or 'exit' to quit): ")
        if q.lower() == "exit":
            break
        answer = query_rag(q)
        print("\nAnswer:\n", answer)
        print("="*50)
