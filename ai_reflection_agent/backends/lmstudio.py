"""LM Studio backend adapter with support for thinking models like Qwen3."""

import re
from typing import Optional, Dict, Any, Tuple
import requests
import json

from .base import BackendAdapter


class LMStudioAdapter(BackendAdapter):
    """Backend adapter for LM Studio with thinking model support."""
    
    def __init__(self, endpoint: str = "http://localhost:1234", model: str = "qwen3", **kwargs):
        """Initialize LM Studio adapter."""
        super().__init__(**kwargs)
        
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.is_thinking_model = kwargs.get("is_thinking_model", True)
        
        # Default parameters
        self.max_tokens = kwargs.get("max_tokens", 4000)
        self.temperature = kwargs.get("temperature", 0.7)
        
        print(f"LM Studio adapter initialized: {self.endpoint}")
        print(f"Model: {model} (thinking model: {self.is_thinking_model})")
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response using LM Studio's OpenAI-compatible API."""
        try:
            response = requests.post(
                f"{self.endpoint}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                    "temperature": kwargs.get("temperature", self.temperature),
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            full_response = data["choices"][0]["message"]["content"]
            
            # If this is a thinking model, extract both thinking and final response
            if self.is_thinking_model:
                thinking, final_response = self._parse_thinking_response(full_response)
                # Store thinking process in metadata for later analysis
                if hasattr(self, '_last_thinking'):
                    self._last_thinking = thinking
                return final_response
            else:
                return full_response
            
        except Exception as e:
            raise RuntimeError(f"LM Studio API error: {str(e)}")
    
    def _parse_thinking_response(self, response: str) -> Tuple[str, str]:
        """Parse thinking tokens from Qwen3 response."""
        # Extract thinking content between <think> tags
        think_pattern = r'<think>(.*?)</think>'
        think_matches = re.findall(think_pattern, response, re.DOTALL)
        
        # Remove thinking tags from final response
        final_response = re.sub(think_pattern, '', response, flags=re.DOTALL).strip()
        
        # Combine all thinking content
        thinking_content = '\n'.join(think_matches) if think_matches else ""
        
        return thinking_content, final_response
    
    def generate_with_thinking(self, prompt: str, **kwargs) -> Dict[str, str]:
        """Generate response and return both thinking process and final answer."""
        try:
            response = requests.post(
                f"{self.endpoint}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                    "temperature": kwargs.get("temperature", self.temperature),
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            full_response = data["choices"][0]["message"]["content"]
            
            if self.is_thinking_model:
                thinking, final_response = self._parse_thinking_response(full_response)
                return {
                    "thinking": thinking,
                    "response": final_response,
                    "full_response": full_response
                }
            else:
                return {
                    "thinking": "",
                    "response": full_response,
                    "full_response": full_response
                }
                
        except Exception as e:
            raise RuntimeError(f"LM Studio API error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Get the model name."""
        return f"{self.model} (LM Studio)"
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens using simple heuristic."""
        return len(text) // 4
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to LM Studio."""
        try:
            # Test with a simple prompt
            response = requests.post(
                f"{self.endpoint}/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": "Hello! This is a connection test."}
                    ],
                    "max_tokens": 100,
                    "temperature": 0.1
                },
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            test_response = data["choices"][0]["message"]["content"]
            
            return {
                "success": True,
                "endpoint": self.endpoint,
                "model": self.model,
                "is_thinking_model": self.is_thinking_model,
                "response_length": len(test_response),
                "test_response": test_response[:100] + "..." if len(test_response) > 100 else test_response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "endpoint": self.endpoint
            }
    
    def get_usage_info(self) -> Dict[str, Any]:
        """Get information about the LM Studio setup."""
        return {
            "model": self.model,
            "endpoint": self.endpoint,
            "is_thinking_model": self.is_thinking_model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }