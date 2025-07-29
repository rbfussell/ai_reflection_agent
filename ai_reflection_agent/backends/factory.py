"""Factory for creating backend adapters."""

from typing import Dict, Any, Type
from .base import BackendAdapter
from .claude import ClaudeAdapter
from .openai_backend import OpenAIAdapter
from .local import LocalAdapter
from .mock import MockAdapter
from .lmstudio import LMStudioAdapter


class BackendFactory:
    """Factory for creating backend adapters."""
    
    _adapters: Dict[str, Type[BackendAdapter]] = {
        "claude": ClaudeAdapter,
        "openai": OpenAIAdapter,
        "local": LocalAdapter,
        "mock": MockAdapter,
        "lmstudio": LMStudioAdapter,
    }
    
    @classmethod
    def create_adapter(cls, backend_type: str, **kwargs) -> BackendAdapter:
        """Create a backend adapter of the specified type."""
        if backend_type not in cls._adapters:
            available = ", ".join(cls._adapters.keys())
            raise ValueError(f"Unknown backend type: {backend_type}. Available: {available}")
        
        adapter_class = cls._adapters[backend_type]
        return adapter_class(**kwargs)
    
    @classmethod
    def get_available_backends(cls) -> list[str]:
        """Get list of available backend types."""
        return list(cls._adapters.keys())
    
    @classmethod
    def register_adapter(cls, name: str, adapter_class: Type[BackendAdapter]):
        """Register a new adapter type."""
        cls._adapters[name] = adapter_class