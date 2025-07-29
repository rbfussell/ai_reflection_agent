"""OpenAI backend adapter using OpenAI's API."""

import os
from typing import Optional, Dict, Any

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .base import BackendAdapter


class OpenAIAdapter(BackendAdapter):
    """Backend adapter for OpenAI GPT models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo", **kwargs):
        """Initialize OpenAI adapter."""
        super().__init__(api_key, **kwargs)
        
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package is required for OpenAI backend")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be provided")
        
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Default parameters
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.temperature = kwargs.get("temperature", 0.7)
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", self.temperature),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Get the OpenAI model name."""
        return self.model
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens using a simple heuristic (GPT uses ~4 chars per token)."""
        return len(text) // 4
    
    def get_usage_info(self) -> Dict[str, Any]:
        """Get information about API usage."""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }