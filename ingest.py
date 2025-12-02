import os
import asyncio
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastembed import TextEmbedding
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "textbook_chunks")
TEXTBOOK_PATH = os.getenv("TEXTBOOK_PATH", "my-ai-book/docs")

# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# Initialize FastEmbed model
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

async def initialize_qdrant_collection():
    try:
        # Check if collection exists
        collections_response = await qdrant_client.get_collections()
        existing_collections = [collection.name for collection in collections_response.collections]
        
        if QDRANT_COLLECTION_NAME not in existing_collections:
            await qdrant_client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )
            print(f"Collection '{QDRANT_COLLECTION_NAME}' created.")
        else:
            print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")
            # Optional: Check if vector params are correct and recreate if not
            collection_info = await qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
            if collection_info.vectors_config.params.size != 384:
                print("Vector size mismatch, recreating collection.")
                await qdrant_client.delete_collection(collection_name=QDRANT_COLLECTION_NAME)
                await qdrant_client.create_collection(
                    collection_name=QDRANT_COLLECTION_NAME,
                    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
                )
                print(f"Collection '{QDRANT_COLLECTION_NAME}' recreated with correct vector size.")
                
    except UnexpectedResponse as e:
        print(f"Error initializing Qdrant collection: {e}")
        raise

async def load_and_chunk_documents():
    print(f"Loading documents from {TEXTBOOK_PATH}...")
    loader = DirectoryLoader(TEXTBOOK_PATH, glob="**/*.mdx", loader_cls=TextLoader, silent_errors=True)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

async def generate_embeddings_and_index(chunks):
    print("Generating embeddings and indexing into Qdrant...")
    points = []
    
    # Generate embeddings in batches for efficiency
    contents = [chunk.page_content for chunk in chunks]
    embeddings = list(embedding_model.embed(contents))
    
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            models.PointStruct(
                id=i,  # Simple sequential ID
                vector=embedding.tolist(),  # Convert numpy array to list
                payload={"content": chunk.page_content, "source": chunk.metadata.get("source")},
            )
        )

    if points:
        try:
            # Upsert points in batches
            await qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                wait=True,
                points=points,
            )
            print(f"Successfully indexed {len(points)} points into Qdrant.")
        except UnexpectedResponse as e:
            print(f"Error during Qdrant upsert: {e}")
            raise
    else:
        print("No points to index.")

async def main():
    await initialize_qdrant_collection()
    chunks = await load_and_chunk_documents()
    await generate_embeddings_and_index(chunks)
    await qdrant_client.close()

if __name__ == "__main__":
    asyncio.run(main())
