"""Claude backend adapter using Anthropic's API."""

import os
from typing import Optional, Dict, Any

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .base import BackendAdapter


class ClaudeAdapter(BackendAdapter):
    """Backend adapter for Claude via Anthropic API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229", **kwargs):
        """Initialize Claude adapter."""
        super().__init__(api_key, **kwargs)
        
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package is required for Claude backend")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be provided")
        
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Default parameters
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.temperature = kwargs.get("temperature", 0.7)
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using Claude."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", self.temperature),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Get the Claude model name."""
        return self.model
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens using a simple heuristic (Claude uses ~4 chars per token)."""
        return len(text) // 4
    
    def get_usage_info(self) -> Dict[str, Any]:
        """Get information about API usage."""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }