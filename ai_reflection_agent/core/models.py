"""Data models for the AI reflection agent."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Score(BaseModel):
    """Scoring model for AI responses."""
    clarity: float = Field(ge=0, le=10, description="How clear and understandable the response is")
    usefulness: float = Field(ge=0, le=10, description="How useful the response is for the user")
    alignment: float = Field(ge=0, le=10, description="How well the response aligns with prompt intent")
    creativity: Optional[float] = Field(None, ge=0, le=10, description="Optional creativity score")


class ResponseEntry(BaseModel):
    """A single prompt-response pair with metadata."""
    model_config = {"protected_namespaces": ()}
    
    id: str = Field(description="Unique identifier for this entry")
    timestamp: datetime = Field(default_factory=datetime.now)
    prompt: str = Field(description="The input prompt")
    response: str = Field(description="The AI's response")
    model_name: str = Field(description="Name of the AI model used")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    score: Optional[Score] = Field(None, description="Self-evaluation scores")
    reflection: Optional[str] = Field(None, description="AI's reflection on its own response")
    revision: Optional[str] = Field(None, description="Revised response if any")
    thinking_process: Optional[str] = Field(None, description="AI's thinking process (for thinking models)")
    full_response: Optional[str] = Field(None, description="Full response including thinking tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExplorationPrompt(BaseModel):
    """A generated prompt for exploring past conversations."""
    id: str = Field(description="Unique identifier")
    timestamp: datetime = Field(default_factory=datetime.now)
    original_entry_id: str = Field(description="ID of the original entry this explores")
    generated_prompt: str = Field(description="The generated exploration prompt")
    context: str = Field(description="Context or reasoning for this exploration")