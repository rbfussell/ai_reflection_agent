"""Scoring system for AI self-evaluation."""

from typing import Optional, Dict, Any
from .models import Score, ResponseEntry


class SelfScorer:
    """Handles AI self-scoring of responses."""
    
    SCORING_PROMPT_TEMPLATE = """
Please evaluate your previous response on the following criteria, giving a score from 0-10 for each:

Original Prompt: {prompt}

Your Response: {response}

Evaluation Criteria:
1. Clarity (0-10): How clear and understandable is the response?
2. Usefulness (0-10): How useful is the response for addressing the prompt?
3. Alignment (0-10): How well does the response align with the intent of the prompt?
4. Creativity (0-10, optional): How creative or innovative is the response?

Please provide scores in this exact format:
Clarity: X.X
Usefulness: X.X
Alignment: X.X
Creativity: X.X (or "N/A" if not applicable)

Also provide a brief explanation for each score.
"""
    
    REFLECTION_PROMPT_TEMPLATE = """
Please reflect on your previous response to this prompt:

Original Prompt: {prompt}

Your Response: {response}

Consider the following:
1. Are there any inaccuracies, hallucinations, or errors in your response?
2. What aspects of the response could be improved?
3. Did you fully address all parts of the prompt?
4. What would you do differently if answering this prompt again?

Provide your reflection as a structured analysis addressing these points.
"""
    
    REVISION_PROMPT_TEMPLATE = """
Based on your reflection, please provide a revised version of your original response.

Original Prompt: {prompt}

Your Original Response: {response}

Your Reflection: {reflection}

Please provide an improved version of your response that addresses the issues identified in your reflection.
"""
    
    def create_scoring_prompt(self, entry: ResponseEntry) -> str:
        """Create a prompt for the AI to score its own response."""
        return self.SCORING_PROMPT_TEMPLATE.format(
            prompt=entry.prompt,
            response=entry.response
        )
    
    def create_reflection_prompt(self, entry: ResponseEntry) -> str:
        """Create a prompt for the AI to reflect on its response."""
        return self.REFLECTION_PROMPT_TEMPLATE.format(
            prompt=entry.prompt,
            response=entry.response
        )
    
    def create_revision_prompt(self, entry: ResponseEntry, reflection: str) -> str:
        """Create a prompt for the AI to revise its response."""
        return self.REVISION_PROMPT_TEMPLATE.format(
            prompt=entry.prompt,
            response=entry.response,
            reflection=reflection
        )
    
    def parse_scores(self, scoring_response: str) -> Optional[Score]:
        """Parse scores from the AI's scoring response."""
        lines = scoring_response.strip().split('\n')
        scores = {}
        
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key in ['clarity', 'usefulness', 'alignment']:
                    try:
                        scores[key] = float(value)
                    except ValueError:
                        continue
                elif key == 'creativity':
                    if value.lower() not in ['n/a', 'na', 'not applicable']:
                        try:
                            scores['creativity'] = float(value)
                        except ValueError:
                            continue
        
        if len(scores) >= 3:  # At least clarity, usefulness, alignment
            return Score(**scores)
        
        return None
    
    def calculate_overall_score(self, score: Score) -> float:
        """Calculate an overall score from individual metrics."""
        base_score = (score.clarity + score.usefulness + score.alignment) / 3
        
        if score.creativity is not None:
            return (base_score * 3 + score.creativity) / 4
        
        return base_score
    
    def get_score_summary(self, score: Score) -> Dict[str, Any]:
        """Get a summary of the scores."""
        summary = {
            'clarity': score.clarity,
            'usefulness': score.usefulness,
            'alignment': score.alignment,
            'overall': self.calculate_overall_score(score)
        }
        
        if score.creativity is not None:
            summary['creativity'] = score.creativity
        
        return summary