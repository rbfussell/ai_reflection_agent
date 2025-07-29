"""Base backend adapter interface."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BackendAdapter(ABC):
    """Abstract base class for AI backend adapters."""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """Initialize the backend adapter."""
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the AI model."""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the name of the model being used."""
        pass
    
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in the given text."""
        pass
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to the backend."""
        try:
            test_response = self.generate_response("Hello, this is a test.")
            return {
                "success": True,
                "model": self.get_model_name(),
                "response_length": len(test_response)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }