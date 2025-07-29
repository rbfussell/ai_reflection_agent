"""JSONL logging system for AI responses."""

import json
import uuid
from pathlib import Path
from typing import List, Optional, Iterator
from datetime import datetime

from .models import ResponseEntry, ExplorationPrompt


class ResponseLogger:
    """Handles logging of AI responses to JSONL files."""
    
    def __init__(self, log_file: str = "ai_responses.jsonl"):
        """Initialize the logger with a log file path."""
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_response(self, 
                    prompt: str, 
                    response: str, 
                    model_name: str,
                    tokens_used: Optional[int] = None,
                    metadata: Optional[dict] = None) -> str:
        """Log a prompt-response pair and return the entry ID."""
        entry = ResponseEntry(
            id=str(uuid.uuid4()),
            prompt=prompt,
            response=response,
            model_name=model_name,
            tokens_used=tokens_used,
            metadata=metadata or {}
        )
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(entry.model_dump_json() + '\n')
        
        return entry.id
    
    def update_entry(self, entry_id: str, **updates) -> bool:
        """Update an existing entry with new data."""
        entries = list(self.read_entries())
        updated = False
        
        for i, entry in enumerate(entries):
            if entry.id == entry_id:
                for key, value in updates.items():
                    if hasattr(entry, key):
                        setattr(entry, key, value)
                entries[i] = entry
                updated = True
                break
        
        if updated:
            self._rewrite_log(entries)
        
        return updated
    
    def read_entries(self) -> Iterator[ResponseEntry]:
        """Read all entries from the log file."""
        if not self.log_file.exists():
            return
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        yield ResponseEntry(**data)
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"Error parsing line: {e}")
                        continue
    
    def get_entry(self, entry_id: str) -> Optional[ResponseEntry]:
        """Get a specific entry by ID."""
        for entry in self.read_entries():
            if entry.id == entry_id:
                return entry
        return None
    
    def get_recent_entries(self, limit: int = 10) -> List[ResponseEntry]:
        """Get the most recent entries."""
        entries = list(self.read_entries())
        return sorted(entries, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def search_entries(self, query: str, field: str = "prompt") -> List[ResponseEntry]:
        """Search entries by text in a specific field."""
        results = []
        for entry in self.read_entries():
            if hasattr(entry, field):
                field_value = getattr(entry, field)
                if field_value and query.lower() in field_value.lower():
                    results.append(entry)
        return results
    
    def _rewrite_log(self, entries: List[ResponseEntry]):
        """Rewrite the entire log file with updated entries."""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(entry.model_dump_json() + '\n')


class ExplorationLogger:
    """Handles logging of exploration prompts."""
    
    def __init__(self, log_file: str = "explorations.jsonl"):
        """Initialize the exploration logger."""
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_exploration(self, original_entry_id: str, generated_prompt: str, context: str) -> str:
        """Log an exploration prompt."""
        exploration = ExplorationPrompt(
            id=str(uuid.uuid4()),
            original_entry_id=original_entry_id,
            generated_prompt=generated_prompt,
            context=context
        )
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(exploration.model_dump_json() + '\n')
        
        return exploration.id
    
    def read_explorations(self) -> Iterator[ExplorationPrompt]:
        """Read all exploration prompts."""
        if not self.log_file.exists():
            return
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        yield ExplorationPrompt(**data)
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"Error parsing exploration line: {e}")
                        continue