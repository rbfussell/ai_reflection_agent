"""Local model backend adapter for running models locally."""

from typing import Optional, Dict, Any
import subprocess
import json
import requests

from .base import BackendAdapter


class LocalAdapter(BackendAdapter):
    """Backend adapter for local AI models via various interfaces."""
    
    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "llama2", **kwargs):
        """Initialize local adapter."""
        super().__init__(**kwargs)
        
        self.endpoint = endpoint
        self.model = model
        self.interface_type = kwargs.get("interface_type", "ollama")  # ollama, text-generation-webui, etc.
        
        # Default parameters
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.temperature = kwargs.get("temperature", 0.7)
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using the local model."""
        if self.interface_type == "ollama":
            return self._generate_ollama(prompt, **kwargs)
        elif self.interface_type == "text-generation-webui":
            return self._generate_textgen_webui(prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported interface type: {self.interface_type}")
    
    def _generate_ollama(self, prompt: str, **kwargs) -> str:
        """Generate response using Ollama API."""
        try:
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", self.temperature),
                        "num_predict": kwargs.get("max_tokens", self.max_tokens)
                    }
                },
                timeout=300
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {str(e)}")
    
    def _generate_textgen_webui(self, prompt: str, **kwargs) -> str:
        """Generate response using text-generation-webui API."""
        try:
            response = requests.post(
                f"{self.endpoint}/api/v1/generate",
                json={
                    "prompt": prompt,
                    "max_new_tokens": kwargs.get("max_tokens", self.max_tokens),
                    "temperature": kwargs.get("temperature", self.temperature),
                    "do_sample": True,
                    "stop": ["\\n\\n"]
                },
                timeout=300
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("results", [{}])[0].get("text", "")
            
        except Exception as e:
            raise RuntimeError(f"Text-generation-webui API error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Get the local model name."""
        return f"{self.model} (local/{self.interface_type})"
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens using a simple heuristic."""
        return len(text) // 4
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to the local model server."""
        try:
            if self.interface_type == "ollama":
                response = requests.get(f"{self.endpoint}/api/tags", timeout=10)
                response.raise_for_status()
                models = response.json().get("models", [])
                available_models = [m["name"] for m in models]
                
                return {
                    "success": True,
                    "interface": self.interface_type,
                    "endpoint": self.endpoint,
                    "available_models": available_models,
                    "current_model": self.model
                }
            else:
                # Generic test for other interfaces
                test_response = self.generate_response("Hello, this is a test.")
                return {
                    "success": True,
                    "interface": self.interface_type,
                    "endpoint": self.endpoint,
                    "model": self.model,
                    "response_length": len(test_response)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "interface": self.interface_type,
                "endpoint": self.endpoint
            }
    
    def get_usage_info(self) -> Dict[str, Any]:
        """Get information about the local model setup."""
        return {
            "model": self.model,
            "interface": self.interface_type,
            "endpoint": self.endpoint,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }