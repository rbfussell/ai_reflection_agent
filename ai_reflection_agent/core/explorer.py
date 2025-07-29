"""Exploration mode for generating extended and deepening prompts."""

from typing import List, Dict, Any, Optional
from .models import ResponseEntry, ExplorationPrompt
from .logger import ResponseLogger, ExplorationLogger


class PromptExplorer:
    """Handles exploration mode functionality for generating new prompts."""
    
    EXPLORATION_TEMPLATES = {
        "deepen": """
Based on this previous conversation, generate a follow-up prompt that deepens the discussion:

Original Prompt: {prompt}
Original Response: {response}

Create a new prompt that:
1. Explores a specific aspect mentioned in the response in greater detail
2. Asks for more nuanced or advanced information
3. Challenges or extends the original thinking

New Prompt:
""",
        
        "alternative": """
Based on this previous conversation, generate an alternative perspective prompt:

Original Prompt: {prompt}
Original Response: {response}

Create a new prompt that:
1. Approaches the same topic from a different angle
2. Considers alternative viewpoints or methodologies
3. Explores what wasn't covered in the original response

New Prompt:
""",
        
        "application": """
Based on this previous conversation, generate a practical application prompt:

Original Prompt: {prompt}
Original Response: {response}

Create a new prompt that:
1. Asks how to apply the concepts discussed in real-world scenarios
2. Explores specific use cases or examples
3. Focuses on implementation or practical considerations

New Prompt:
""",
        
        "critique": """
Based on this previous conversation, generate a critical analysis prompt:

Original Prompt: {prompt}
Original Response: {response}

Create a new prompt that:
1. Questions assumptions made in the original response
2. Explores potential limitations or drawbacks
3. Asks for evidence or counter-arguments

New Prompt:
""",
        
        "synthesis": """
Based on this previous conversation, generate a synthesis prompt:

Original Prompt: {prompt}
Original Response: {response}

Create a new prompt that:
1. Connects this topic to other related concepts or fields
2. Asks for broader implications or connections
3. Explores how this fits into a larger framework

New Prompt:
"""
    }
    
    def __init__(self, response_logger: ResponseLogger, exploration_logger: ExplorationLogger):
        """Initialize the explorer with logger instances."""
        self.response_logger = response_logger
        self.exploration_logger = exploration_logger
    
    def generate_exploration_prompt(self, entry_id: str, 
                                  exploration_type: str, 
                                  backend_adapter) -> Dict[str, Any]:
        """Generate an exploration prompt for a given entry."""
        entry = self.response_logger.get_entry(entry_id)
        if not entry:
            return {"error": "Entry not found"}
        
        if exploration_type not in self.EXPLORATION_TEMPLATES:
            return {"error": f"Unknown exploration type: {exploration_type}"}
        
        try:
            template = self.EXPLORATION_TEMPLATES[exploration_type]
            generation_prompt = template.format(
                prompt=entry.prompt,
                response=entry.response
            )
            
            generated_prompt = backend_adapter.generate_response(generation_prompt)
            
            # Clean up the generated prompt
            cleaned_prompt = self._clean_generated_prompt(generated_prompt)
            
            # Log the exploration
            exploration_id = self.exploration_logger.log_exploration(
                original_entry_id=entry_id,
                generated_prompt=cleaned_prompt,
                context=f"Generated using '{exploration_type}' template"
            )
            
            return {
                "success": True,
                "exploration_id": exploration_id,
                "exploration_type": exploration_type,
                "generated_prompt": cleaned_prompt,
                "original_entry": entry
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_multiple_explorations(self, entry_id: str, 
                                     exploration_types: List[str], 
                                     backend_adapter) -> Dict[str, Any]:
        """Generate multiple exploration prompts for a single entry."""
        results = {
            "entry_id": entry_id,
            "total": len(exploration_types),
            "successful": 0,
            "failed": 0,
            "explorations": []
        }
        
        for exploration_type in exploration_types:
            result = self.generate_exploration_prompt(entry_id, exploration_type, backend_adapter)
            results["explorations"].append(result)
            
            if result.get("success"):
                results["successful"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def auto_explore_entry(self, entry_id: str, backend_adapter, 
                          max_explorations: int = 3) -> Dict[str, Any]:
        """Automatically generate multiple types of exploration prompts."""
        entry = self.response_logger.get_entry(entry_id)
        if not entry:
            return {"error": "Entry not found"}
        
        # Select exploration types based on response characteristics
        selected_types = self._select_exploration_types(entry, max_explorations)
        
        return self.generate_multiple_explorations(entry_id, selected_types, backend_adapter)
    
    def explore_recent_entries(self, backend_adapter, 
                             limit: int = 5, 
                             explorations_per_entry: int = 2) -> Dict[str, Any]:
        """Explore recent entries automatically."""
        recent_entries = self.response_logger.get_recent_entries(limit)
        
        results = {
            "total_entries": len(recent_entries),
            "total_explorations": 0,
            "successful_explorations": 0,
            "entry_results": []
        }
        
        for entry in recent_entries:
            entry_result = self.auto_explore_entry(
                entry.id, 
                backend_adapter, 
                max_explorations=explorations_per_entry
            )
            results["entry_results"].append(entry_result)
            
            if "explorations" in entry_result:
                results["total_explorations"] += len(entry_result["explorations"])
                results["successful_explorations"] += entry_result.get("successful", 0)
        
        return results
    
    def get_explorations_for_entry(self, entry_id: str) -> List[ExplorationPrompt]:
        """Get all exploration prompts generated for a specific entry."""
        explorations = []
        for exploration in self.exploration_logger.read_explorations():
            if exploration.original_entry_id == entry_id:
                explorations.append(exploration)
        
        return sorted(explorations, key=lambda x: x.timestamp, reverse=True)
    
    def search_explorations(self, query: str) -> List[ExplorationPrompt]:
        """Search exploration prompts by text content."""
        results = []
        for exploration in self.exploration_logger.read_explorations():
            if (query.lower() in exploration.generated_prompt.lower() or 
                query.lower() in exploration.context.lower()):
                results.append(exploration)
        
        return results
    
    def _select_exploration_types(self, entry: ResponseEntry, max_types: int) -> List[str]:
        """Select appropriate exploration types based on entry characteristics."""
        all_types = list(self.EXPLORATION_TEMPLATES.keys())
        
        # Simple heuristics for type selection
        selected = []
        
        # Always include deepen for comprehensive responses
        if len(entry.response) > 200:
            selected.append("deepen")
        
        # Include alternative for opinion-based or subjective content
        opinion_words = ["should", "could", "might", "recommend", "suggest", "believe"]
        if any(word in entry.response.lower() for word in opinion_words):
            selected.append("alternative")
        
        # Include application for how-to or explanatory content
        if any(word in entry.prompt.lower() for word in ["how", "what", "explain"]):
            selected.append("application")
        
        # Fill remaining slots randomly
        import random
        remaining_types = [t for t in all_types if t not in selected]
        while len(selected) < max_types and remaining_types:
            selected.append(remaining_types.pop(random.randint(0, len(remaining_types) - 1)))
        
        return selected[:max_types]
    
    def _clean_generated_prompt(self, raw_prompt: str) -> str:
        """Clean up the generated prompt by removing template artifacts."""
        lines = raw_prompt.strip().split('\n')
        
        # Find lines that look like actual prompts (not template instructions)
        prompt_lines = []
        in_prompt_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that look like template instructions
            if line.startswith(("1.", "2.", "3.", "Create a", "Generate a", "New Prompt:")):
                if line == "New Prompt:":
                    in_prompt_section = True
                continue
            
            # Look for actual prompt content
            if in_prompt_section or (line.endswith("?") and len(line) > 20):
                prompt_lines.append(line)
        
        if prompt_lines:
            return ' '.join(prompt_lines)
        
        # Fallback: return the last substantial line
        substantial_lines = [line for line in lines if len(line.strip()) > 20]
        return substantial_lines[-1] if substantial_lines else raw_prompt.strip()