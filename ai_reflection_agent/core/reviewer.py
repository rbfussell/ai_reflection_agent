"""Review mode for reflection and revision of AI responses."""

from typing import List, Optional, Dict, Any
from .models import ResponseEntry, Score
from .logger import ResponseLogger
from .scorer import SelfScorer


class ResponseReviewer:
    """Handles review mode functionality for reflecting on past responses."""
    
    def __init__(self, logger: ResponseLogger, scorer: SelfScorer):
        """Initialize the reviewer with logger and scorer instances."""
        self.logger = logger
        self.scorer = scorer
    
    def get_reviewable_entries(self, limit: int = 10, 
                              unscored_only: bool = False,
                              unreflected_only: bool = False) -> List[ResponseEntry]:
        """Get entries that can be reviewed based on criteria."""
        entries = self.logger.get_recent_entries(limit * 2)  # Get more to filter
        
        reviewable = []
        for entry in entries:
            if unscored_only and entry.score is not None:
                continue
            if unreflected_only and entry.reflection is not None:
                continue
            reviewable.append(entry)
            
            if len(reviewable) >= limit:
                break
        
        return reviewable
    
    def review_entry(self, entry_id: str, backend_adapter) -> Dict[str, Any]:
        """Perform a complete review of an entry including scoring and reflection."""
        entry = self.logger.get_entry(entry_id)
        if not entry:
            return {"error": "Entry not found"}
        
        results = {"entry_id": entry_id, "steps": []}
        
        # Step 1: Score the response if not already scored
        if entry.score is None:
            score_result = self.score_response(entry, backend_adapter)
            results["steps"].append(score_result)
            
            if score_result.get("success"):
                entry.score = score_result["score"]
        
        # Step 2: Generate reflection if not already done
        if entry.reflection is None:
            reflection_result = self.reflect_on_response(entry, backend_adapter)
            results["steps"].append(reflection_result)
            
            if reflection_result.get("success"):
                entry.reflection = reflection_result["reflection"]
        
        # Step 3: Generate revision if reflection indicates issues
        if entry.revision is None and entry.reflection:
            revision_result = self.revise_response(entry, backend_adapter)
            results["steps"].append(revision_result)
            
            if revision_result.get("success"):
                entry.revision = revision_result["revision"]
        
        # Update the entry in the log
        self.logger.update_entry(
            entry_id,
            score=entry.score,
            reflection=entry.reflection,
            revision=entry.revision
        )
        
        results["entry"] = entry
        return results
    
    def score_response(self, entry: ResponseEntry, backend_adapter) -> Dict[str, Any]:
        """Score a response using the AI backend."""
        try:
            scoring_prompt = self.scorer.create_scoring_prompt(entry)
            scoring_response = backend_adapter.generate_response(scoring_prompt)
            
            score = self.scorer.parse_scores(scoring_response)
            if score:
                return {
                    "step": "scoring",
                    "success": True,
                    "score": score,
                    "raw_response": scoring_response
                }
            else:
                return {
                    "step": "scoring",
                    "success": False,
                    "error": "Failed to parse scores from response",
                    "raw_response": scoring_response
                }
        
        except Exception as e:
            return {
                "step": "scoring",
                "success": False,
                "error": str(e)
            }
    
    def reflect_on_response(self, entry: ResponseEntry, backend_adapter) -> Dict[str, Any]:
        """Generate reflection on a response using the AI backend."""
        try:
            reflection_prompt = self.scorer.create_reflection_prompt(entry)
            reflection = backend_adapter.generate_response(reflection_prompt)
            
            return {
                "step": "reflection",
                "success": True,
                "reflection": reflection
            }
        
        except Exception as e:
            return {
                "step": "reflection",
                "success": False,
                "error": str(e)
            }
    
    def revise_response(self, entry: ResponseEntry, backend_adapter) -> Dict[str, Any]:
        """Generate a revised response based on reflection."""
        try:
            revision_prompt = self.scorer.create_revision_prompt(entry, entry.reflection)
            revision = backend_adapter.generate_response(revision_prompt)
            
            return {
                "step": "revision",
                "success": True,
                "revision": revision
            }
        
        except Exception as e:
            return {
                "step": "revision",
                "success": False,
                "error": str(e)
            }
    
    def batch_review(self, entry_ids: List[str], backend_adapter) -> Dict[str, Any]:
        """Review multiple entries in batch."""
        results = {
            "total": len(entry_ids),
            "successful": 0,
            "failed": 0,
            "results": []
        }
        
        for entry_id in entry_ids:
            result = self.review_entry(entry_id, backend_adapter)
            results["results"].append(result)
            
            if any(step.get("success", False) for step in result.get("steps", [])):
                results["successful"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    def get_review_summary(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of the review for an entry."""
        entry = self.logger.get_entry(entry_id)
        if not entry:
            return None
        
        summary = {
            "entry_id": entry_id,
            "timestamp": entry.timestamp,
            "model_name": entry.model_name,
            "has_score": entry.score is not None,
            "has_reflection": entry.reflection is not None,
            "has_revision": entry.revision is not None
        }
        
        if entry.score:
            summary["score_summary"] = self.scorer.get_score_summary(entry.score)
        
        return summary