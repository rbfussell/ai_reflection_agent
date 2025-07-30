"""File management utilities for the WebUI."""

import json
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import os


class FileManager:
    """Handles file operations for the WebUI."""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        dirs_to_create = [
            self.base_dir / "logs",
            self.base_dir / "exports", 
            self.base_dir / "backups",
            self.base_dir / "configs"
        ]
        
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_experiment_results(
        self, 
        results: List[Dict[str, Any]], 
        experiment_id: str,
        format_type: str = "json"
    ) -> str:
        """Save experiment results to file."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type.lower() == "json":
            filename = f"experiment_{experiment_id}_{timestamp}.json"
            filepath = self.base_dir / "exports" / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
                
        elif format_type.lower() == "csv":
            filename = f"experiment_{experiment_id}_{timestamp}.csv"
            filepath = self.base_dir / "exports" / filename
            
            # Flatten results for CSV
            flattened_data = []
            for result in results:
                flat_result = self._flatten_dict(result)
                flattened_data.append(flat_result)
            
            if flattened_data:
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=flattened_data[0].keys())
                    writer.writeheader()
                    writer.writerows(flattened_data)
        
        elif format_type.lower() == "markdown":
            filename = f"experiment_{experiment_id}_{timestamp}.md"
            filepath = self.base_dir / "exports" / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Experiment Results: {experiment_id}\n\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n\n")
                
                for i, result in enumerate(results):
                    f.write(f"## Level {i}: {result.get('step_name', 'Unknown')}\n\n")
                    f.write(f"**Thinking:** {result.get('thinking', 'N/A')}\n\n")
                    f.write(f"**Response:** {result.get('response', 'N/A')}\n\n")
                    f.write("---\n\n")
        
        return str(filepath)
    
    def load_log_entries(
        self,
        log_file: str = "consciousness_exploration.jsonl",
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Load and filter log entries."""
        
        log_path = self.base_dir / log_file
        if not log_path.exists():
            return []
        
        entries = []
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entry = json.loads(line)
                            if self._matches_filters(entry, filters):
                                entries.append(entry)
                        except json.JSONDecodeError:
                            continue  # Skip malformed lines
        
        except Exception as e:
            print(f"Error loading log entries: {e}")
            return []
        
        # Sort by timestamp (newest first)
        entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return entries
    
    def get_entry_by_id(self, entry_id: str, log_file: str = "consciousness_exploration.jsonl") -> Optional[Dict[str, Any]]:
        """Get a specific entry by ID."""
        
        entries = self.load_log_entries(log_file)
        for entry in entries:
            if entry.get('id') == entry_id:
                return entry
        
        return None
    
    def backup_logs(self, backup_name: Optional[str] = None) -> str:
        """Create a backup of current logs."""
        
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = self.base_dir / "backups" / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy log files
        log_files = [
            "consciousness_exploration.jsonl",
            "responses.jsonl", 
            "explorations.jsonl"
        ]
        
        copied_files = []
        for log_file in log_files:
            source_path = self.base_dir / log_file
            if source_path.exists():
                dest_path = backup_dir / log_file
                dest_path.write_bytes(source_path.read_bytes())
                copied_files.append(log_file)
        
        # Create backup info file
        backup_info = {
            "created": datetime.now().isoformat(),
            "files": copied_files,
            "total_size": sum((backup_dir / f).stat().st_size for f in copied_files)
        }
        
        info_path = backup_dir / "backup_info.json"
        with open(info_path, 'w') as f:
            json.dump(backup_info, f, indent=2)
        
        return str(backup_dir)
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """Flatten nested dictionary for CSV export."""
        
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert lists to string representation
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    def _matches_filters(self, entry: Dict[str, Any], filters: Optional[Dict[str, Any]]) -> bool:
        """Check if entry matches the given filters."""
        
        if not filters:
            return True
        
        for key, value in filters.items():
            if key == 'date_from':
                entry_date = entry.get('timestamp', '')
                if entry_date < value:
                    return False
            
            elif key == 'date_to':
                entry_date = entry.get('timestamp', '')
                if entry_date > value:
                    return False
            
            elif key == 'model':
                if value != "All Models" and entry.get('model_name') != value:
                    return False
            
            elif key == 'experiment_type':
                if value != "All Types":
                    entry_type = entry.get('metadata', {}).get('type', '')
                    if entry_type != value:
                        return False
            
            elif key == 'search_query' and value:
                # Search in prompt, response, and thinking
                search_text = value.lower()
                searchable_fields = [
                    entry.get('prompt', ''),
                    entry.get('response', ''),
                    entry.get('thinking_process', '')
                ]
                
                if not any(search_text in field.lower() for field in searchable_fields):
                    return False
        
        return True
    
    def get_log_statistics(self, log_file: str = "consciousness_exploration.jsonl") -> Dict[str, Any]:
        """Get statistics about log entries."""
        
        entries = self.load_log_entries(log_file)
        
        if not entries:
            return {"total_entries": 0}
        
        # Calculate statistics
        total_entries = len(entries)
        models = {}
        experiment_types = {}
        total_thinking_chars = 0
        total_response_chars = 0
        
        for entry in entries:
            # Model statistics
            model = entry.get('model_name', 'unknown')
            models[model] = models.get(model, 0) + 1
            
            # Experiment type statistics
            exp_type = entry.get('metadata', {}).get('type', 'unknown')
            experiment_types[exp_type] = experiment_types.get(exp_type, 0) + 1
            
            # Character counts
            thinking = entry.get('thinking_process', '')
            response = entry.get('response', '')
            total_thinking_chars += len(thinking) if thinking else 0
            total_response_chars += len(response) if response else 0
        
        return {
            "total_entries": total_entries,
            "models": models,
            "experiment_types": experiment_types,
            "avg_thinking_length": total_thinking_chars / total_entries if total_entries > 0 else 0,
            "avg_response_length": total_response_chars / total_entries if total_entries > 0 else 0,
            "total_thinking_chars": total_thinking_chars,
            "total_response_chars": total_response_chars
        }


# Global file manager instance
file_manager = FileManager()