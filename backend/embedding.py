import file_loader as loader
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

pdf_path = loader.pdf_path

text_blocks = loader.extract_text(pdf_path)
table_blocks = loader.extract_tables(pdf_path)
image_blocks = loader.extract_images(pdf_path)

chunks = text_blocks + table_blocks + image_blocks

# print(chunks)

def chunk_to_text(chunk):
    if chunk['type'] == 'text':
        return chunk['content']
    elif chunk['type'] == 'table':
        return chunk['content']
    elif chunk['type'] == 'image':
        return f"[Figure at page {chunk['page']}]"
    else:
        return "Not a expected type"
    
texts_for_index = [chunk_to_text(chunk) for chunk in chunks]
# print(texts_for_index)

def get_embeddings(text):
    embeddings = model.encode(text)
    return embeddings

embeddings = [get_embeddings(text) for text in texts_for_index]

# print(embeddings)

index_to_chunk = {i: chunks[i] for i in range(len(chunks))}

