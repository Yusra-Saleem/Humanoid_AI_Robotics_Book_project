import os
import uuid
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
from fastembed import TextEmbedding

# Load environment variables from .env file
load_dotenv()

# Configure Qdrant client
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333")) # Default port
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "textbook_chunks")


qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT, 
    api_key=QDRANT_API_KEY,
)

# Initialize FastEmbed model
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Function to generate embeddings
def generate_embedding(text: str) -> list[float]:
    # FastEmbed expects a list of strings and returns a generator of embeddings
    embeddings = list(embedding_model.embed([text]))
    return list(embeddings[0])

# Function to chunk text (simple example for now)
def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    # A more sophisticated chunking mechanism would be used here
    # For now, a simple split by sentences or paragraphs will do
    sentences = text.replace('\\n', ' ').split('.') # Simple split by sentences
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + "."
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Function to ingest data
def ingest_data(mdx_file_path: str):
    with open(mdx_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_text(content)

    # Ensure collection exists
    try:
        qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
    except Exception: # Qdrant raises an exception if collection not found
        # Determine embedding size dynamically from first chunk
        if not chunks:
            print(f"No chunks to embed from {mdx_file_path}. Skipping ingestion.")
            return

        first_embedding = generate_embedding(chunks[0])
        vector_size = len(first_embedding)

        qdrant_client.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
        )
        print(f"Collection '{QDRANT_COLLECTION_NAME}' created with vector size {vector_size}.")


    points = []
    for i, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)
        points.append(
            models.PointStruct(
                id=str(uuid.uuid4()),  # Generate a unique ID for each chunk
                vector=embedding,
                payload={"content": chunk, "source_file": mdx_file_path, "chunk_id": i},
            )
        )

    if points:
        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=points,
        )
        print(f"Ingested {len(chunks)} chunks from {mdx_file_path} into Qdrant.")
    else:
        print(f"No content to ingest from {mdx_file_path}.")


if __name__ == "__main__":
    # Example usage: Replace with actual MDX file paths
    # For hackathon, assume content is in a specific folder
    # For now, let's create a dummy file for demonstration.
    dummy_mdx_content = "# Chapter 1: Introduction to Robotics\\n\\nRobotics is an interdisciplinary field that integrates computer science and engineering.\\nIt involves the design, construction, operation, and use of robots. Artificial intelligence, mechanical engineering, and computer vision are key components. Robots can perform tasks autonomously or semi-autonomously."
    dummy_mdx_file = "dummy_chapter.mdx"
    with open(dummy_mdx_file, "w") as f:
        f.write(dummy_mdx_content)

    ingest_data(dummy_mdx_file)
    os.remove(dummy_mdx_file) # Clean up dummy file
