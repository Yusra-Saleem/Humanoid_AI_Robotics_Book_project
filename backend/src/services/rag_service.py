import os
from typing import List, Optional, Tuple
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from qdrant_client.models import Filter, FieldCondition, MatchValue
from agents import Agent, Runner
from src.core.config import settings

# Lazy globals
_qdrant_client = None
_embedding_model = None

QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "textbook_chunks")


def _get_qdrant_client():
    """Lazy initialization of Qdrant client."""
    global _qdrant_client
    if _qdrant_client is None:
        try:
            if settings.QDRANT_URL:
                _qdrant_client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                )
                print("✓ Connected to Qdrant Cloud")
            else:
                _qdrant_client = QdrantClient(
                    host=os.getenv("QDRANT_HOST", "localhost"),
                    port=int(os.getenv("QDRANT_PORT", "6333")),
                    api_key=settings.QDRANT_API_KEY or None,
                )
                print("✓ Connected to local Qdrant")
        except Exception as e:
            print(f"Warning: Could not initialize Qdrant client: {e}")
            raise
    return _qdrant_client


def _get_embedding_model():
    """Lazy initialization of embedding model."""
    global _embedding_model
    if _embedding_model is None:
        try:
            _embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        except Exception as e:
            print(f"Warning: Could not initialize embedding model: {e}")
            raise
    return _embedding_model


class RAGService:
    def __init__(self):
        self.agent = Agent(
            name="RAG Assistant",
            instructions=(
                "You are a helpful textbook assistant. Use textbook context to answer. "
                "Reference chapters and sections when possible."
            ),
            model="gpt-3.5-turbo",
        )

    def generate_embedding(self, text: str) -> List[float]:
        model = _get_embedding_model()
        emb = list(model.embed([text]))
        return list(emb[0])

    async def generate_response(
        self,
        query: str,
        selected_text: Optional[str] = None,
        current_page: Optional[str] = None
    ) -> Tuple[str, List[str]]:

        try:
            context_list = []
            sources = []

            # Add selected text if provided
            if selected_text:
                context_list.append(f"User-selected text: {selected_text}")
                sources.append("User selection")

            # -------- Qdrant search --------
            try:
                qdrant = _get_qdrant_client()
                search_query = selected_text if selected_text else query
                query_embedding = self.generate_embedding(search_query)

                # If current page exists → boost
                if current_page:
                    try:
                        page_results = qdrant.search(
                            collection_name=QDRANT_COLLECTION_NAME,
                            query_vector=query_embedding,
                            query_filter=Filter(
                                must=[
                                    FieldCondition(
                                        key="page_path",
                                        match=MatchValue(value=current_page)
                                    )
                                ]
                            ),
                            limit=2,
                        )

                        general_results = qdrant.search(
                            collection_name=QDRANT_COLLECTION_NAME,
                            query_vector=query_embedding,
                            limit=3,
                        )

                        combined = list(page_results) + list(general_results)

                        unique = []
                        seen = set()
                        for hit in combined:
                            if hit.id not in seen:
                                seen.add(hit.id)
                                unique.append(hit)
                                if len(unique) >= 3:
                                    break

                        search_results = unique

                    except Exception as e:
                        print("Warning: page-specific search failed:", e)
                        search_results = qdrant.search(
                            collection_name=QDRANT_COLLECTION_NAME,
                            query_vector=query_embedding,
                            limit=3,
                        )

                else:
                    # no current page
                    search_results = qdrant.search(
                        collection_name=QDRANT_COLLECTION_NAME,
                        query_vector=query_embedding,
                        limit=3,
                    )

                # Extract context from qdrant results
                for hit in search_results:
                    if hit.payload and "content" in hit.payload:
                        txt = hit.payload["content"]

                        # Add chapter or section
                        if "chapter" in hit.payload:
                            txt = f"[{hit.payload['chapter']}] {txt}"

                        context_list.append(txt)

                        # Track source info
                        sp = []
                        if "page_path" in hit.payload:
                            sp.append(hit.payload["page_path"])
                        if "chapter" in hit.payload:
                            sp.append(hit.payload["chapter"])
                        if "section" in hit.payload:
                            sp.append(hit.payload["section"])

                        sources.append(" → ".join(sp) if sp else "Textbook")

            except Exception as e:
                print("Warning: Qdrant search failed:", e)
                if not selected_text:
                    context_list = [query]
                    sources = ["General knowledge"]

            if not context_list:
                context_list = [query]
                sources = ["General knowledge"]

            # ---------- Build Prompt ----------
            page_context = ""
            if current_page:
                page_context = (
                    f"\n\nThe user is currently viewing page: {current_page}. "
                    f"Prefer content relevant to this page."
                )

            joined_context = "\n\n".join(context_list[:2])
            if len(joined_context) > 800:
                joined_context = joined_context[:800] + "..."

            prompt = f"""
You are a helpful AI textbook assistant.{page_context}

Textbook Context:
{joined_context}

Question: {query}

Answer clearly and reference chapters/sections when helpful.
"""

            result = await Runner.run(self.agent, input=prompt)

            return str(result.final_output), sources

        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "insufficient" in err.lower():
                return (
                    "Your OpenAI account quota has been exceeded. Please check billing.",
                    []
                )
            if "429" in err or "rate limit" in err.lower():
                return ("Too many requests. Please try again shortly.", [])

            return (f"An error occurred: {err}", [])
