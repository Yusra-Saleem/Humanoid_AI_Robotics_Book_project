from typing import List, Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    current_page: Optional[str] = None  # Current page path (e.g., "/docs/Module-1-ROS2/01-Week-3-Nodes-Topics")
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
