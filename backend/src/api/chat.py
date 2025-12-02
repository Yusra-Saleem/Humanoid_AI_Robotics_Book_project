from fastapi import APIRouter, Depends, HTTPException
from src.models.chat import ChatRequest, ChatResponse
from src.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    import time
    start_time = time.time()
    try:
        print(f"Chat request - Query: '{request.query[:50]}...', Page: {request.current_page or 'N/A'}")
        answer, sources = await rag_service.generate_response(
            query=request.query,
            selected_text=request.selected_text,
            current_page=request.current_page
        )
        elapsed = time.time() - start_time
        print(f"Chat response generated in {elapsed:.2f}s with {len(sources)} sources")
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"Error in chat endpoint after {elapsed:.2f}s: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
