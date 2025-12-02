"""
Ingest all Docusaurus docs from my-ai-book/docs into Qdrant using fastembed.
This script reads all .md files, chunks them, generates embeddings, and stores in Qdrant.
"""
import os
import uuid
import re
from pathlib import Path
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
from fastembed import TextEmbedding

# Load environment variables
load_dotenv()

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "textbook_chunks")

# Path to docs directory (relative to backend folder)
DOCS_PATH = Path(__file__).parent.parent / "my-ai-book" / "docs"

# Initialize embedding model
print("Loading FastEmbed model...")
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
print("✓ FastEmbed model loaded")


def get_qdrant_client():
    """Initialize Qdrant client (cloud or local)."""
    if QDRANT_URL:
        print(f"Connecting to Qdrant Cloud: {QDRANT_URL}")
        return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    else:
        print(f"Connecting to local Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
        return QdrantClient(
            host=QDRANT_HOST,
            port=QDRANT_PORT,
            api_key=QDRANT_API_KEY if QDRANT_API_KEY else None,
        )


def generate_embedding(text: str) -> list[float]:
    """Generate embedding for text using FastEmbed."""
    embeddings = list(embedding_model.embed([text]))
    return list(embeddings[0])


def extract_metadata(file_path: Path) -> dict:
    """Extract metadata from file path and content."""
    # Get relative path from docs folder
    rel_path = file_path.relative_to(DOCS_PATH)
    parts = rel_path.parts
    
    # Extract module/chapter info from path
    module = parts[0] if len(parts) > 1 else "Introduction"
    filename = parts[-1]
    
    # Extract chapter/section from filename (e.g., "01-Week-3-Nodes-Topics.md")
    chapter_match = re.match(r"(\d+)-(.+)\.md", filename)
    if chapter_match:
        chapter_num = chapter_match.group(1)
        chapter_name = chapter_match.group(2).replace("-", " ")
    else:
        chapter_num = "1"
        chapter_name = filename.replace(".md", "").replace("-", " ")
    
    # Build page path (Docusaurus route)
    page_path = f"/docs/{'/'.join(parts[:-1])}/{filename.replace('.md', '')}" if len(parts) > 1 else f"/docs/{filename.replace('.md', '')}"
    
    return {
        "module": module,
        "chapter": chapter_name,
        "chapter_num": chapter_num,
        "filename": filename,
        "page_path": page_path,
        "source_file": str(rel_path),
    }


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Chunk text intelligently by paragraphs and sentences.
    Maintains context with overlap between chunks.
    """
    # Remove markdown frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    
    # Split by double newlines (paragraphs)
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If adding this paragraph would exceed chunk size
        if len(current_chunk) + len(para) + 2 > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap (last 50 chars)
            current_chunk = current_chunk[-overlap:] + "\n\n" + para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    # Add remaining chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def ingest_file(file_path: Path, qdrant_client: QdrantClient):
    """Ingest a single markdown file into Qdrant."""
    print(f"\nProcessing: {file_path.name}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
        return
    
    if not content.strip():
        print(f"  ⚠ File is empty, skipping")
        return
    
    # Extract metadata
    metadata = extract_metadata(file_path)
    
    # Chunk the content
    chunks = chunk_text(content)
    print(f"  → Generated {len(chunks)} chunks")
    
    if not chunks:
        print(f"  ⚠ No chunks generated, skipping")
        return
    
    # Generate embeddings and prepare points
    points = []
    for i, chunk in enumerate(chunks):
        try:
            embedding = generate_embedding(chunk)
            points.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "content": chunk,
                        "source_file": metadata["source_file"],
                        "page_path": metadata["page_path"],
                        "module": metadata["module"],
                        "chapter": metadata["chapter"],
                        "chapter_num": metadata["chapter_num"],
                        "filename": metadata["filename"],
                        "chunk_index": i,
                    },
                )
            )
        except Exception as e:
            print(f"  ✗ Error generating embedding for chunk {i}: {e}")
            continue
    
    if points:
        try:
            qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=points,
            )
            print(f"  ✓ Ingested {len(points)} chunks into Qdrant")
        except Exception as e:
            print(f"  ✗ Error upserting to Qdrant: {e}")
    else:
        print(f"  ⚠ No points to upsert")


def ensure_collection(qdrant_client: QdrantClient):
    """Ensure Qdrant collection exists with correct configuration."""
    try:
        collection_info = qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
        print(f"✓ Collection '{QDRANT_COLLECTION_NAME}' already exists")
        print(f"  Vector size: {collection_info.config.params.vectors.size}")
        return
    except Exception:
        pass
    
    # Create collection - need to determine vector size first
    print(f"Creating collection '{QDRANT_COLLECTION_NAME}'...")
    test_text = "This is a test chunk to determine embedding size."
    test_embedding = generate_embedding(test_text)
    vector_size = len(test_embedding)
    
    qdrant_client.create_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )
    print(f"✓ Collection '{QDRANT_COLLECTION_NAME}' created with vector size {vector_size}")


def main():
    """Main ingestion function."""
    print("=" * 60)
    print("Docusaurus Docs Ingestion to Qdrant")
    print("=" * 60)
    
    if not DOCS_PATH.exists():
        print(f"✗ Docs directory not found: {DOCS_PATH}")
        print("  Please ensure my-ai-book/docs directory exists")
        return
    
    print(f"📁 Docs directory: {DOCS_PATH}")
    
    # Initialize Qdrant client
    try:
        qdrant_client = get_qdrant_client()
        print("✓ Qdrant client initialized")
    except Exception as e:
        print(f"✗ Failed to connect to Qdrant: {e}")
        return
    
    # Ensure collection exists
    ensure_collection(qdrant_client)
    
    # Find all markdown files
    md_files = list(DOCS_PATH.rglob("*.md"))
    print(f"\n📄 Found {len(md_files)} markdown files")
    
    if not md_files:
        print("  No markdown files found in docs directory")
        return
    
    # Ingest each file
    total_chunks = 0
    for md_file in md_files:
        ingest_file(md_file, qdrant_client)
    
    print("\n" + "=" * 60)
    print("✓ Ingestion complete!")
    print("=" * 60)
    print(f"\nYou can now query the chatbot with questions about the textbook content.")
    print(f"Chatbot will retrieve relevant context from Qdrant based on your queries.")


if __name__ == "__main__":
    main()

