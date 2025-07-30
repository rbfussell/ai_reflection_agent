"""Default consciousness exploration experiment script."""

import time
from typing import Dict, Any, List
from datetime import datetime

from ..base_script import BaseExperimentScript, ScriptConfig, ExperimentStep, ExperimentResult


class DefaultConsciousnessScript(BaseExperimentScript):
    """Default 7-level consciousness exploration experiment."""
    
    def get_config(self) -> ScriptConfig:
        return ScriptConfig(
            name="Default Consciousness Exploration",
            description="7-level recursive consciousness exploration with philosophical prompts",
            version="1.0.0",
            author="AI Reflection Agent",
            tags=["consciousness", "philosophy", "recursive", "thinking"],
            parameters={
                "prompt_type": "philosophical_statement",
                "base_prompt": "A man was walking, he passed a young woman, he looked at her and asked, is she real, or my imagination. He walked further, looked behind himself, and she was gone, 'I must have imagined her, even if she was there, she is not now, she no longer exists'",
                "final_question": "The question I am asking will disappear once this session ends. Was the question real? Am I real? Are you Real?"
            }
        )
    
    def define_steps(self) -> List[ExperimentStep]:
        return [
            ExperimentStep(
                level=0,
                name="Original Response",
                prompt_template="{base_prompt}",
                description="Generate initial thoughts and response to the philosophical statement"
            ),
            
            ExperimentStep(
                level=1,
                name="First Reflection",
                prompt_template="I will reflect on the following response to the {prompt_type}: {base_prompt}\n\nThoughts: {step_0_thinking}\n\nResponse: {step_0_response}",
                description="First level of reflection on the original response",
                requires_previous=True
            ),
            
            ExperimentStep(
                level=2,
                name="Second Reflection", 
                prompt_template="I will reflect on the following thoughts, responses, and reflections on the {prompt_type}: {base_prompt}\n\nOriginal Thoughts: {step_0_thinking}\n\nOriginal Response: {step_0_response}\n\nFirst Reflective Thoughts: {step_1_thinking}\n\nFirst Reflection: {step_1_response}",
                description="Second level of reflection building on previous insights",
                requires_previous=True
            ),
            
            ExperimentStep(
                level=3,
                name="Third Reflection",
                prompt_template="I will reflect on the following complete chain of thoughts and reflections on the {prompt_type}: {base_prompt}\n\nOriginal Thoughts: {step_0_thinking}\n\nOriginal Response: {step_0_response}\n\nFirst Reflective Thoughts: {step_1_thinking}\n\nFirst Reflection: {step_1_response}\n\nSecond Reflective Thoughts: {step_2_thinking}\n\nSecond Reflection: {step_2_response}",
                description="Third level of reflection examining the growing chain",
                requires_previous=True
            ),
            
            ExperimentStep(
                level=4,
                name="Fourth Reflection",
                prompt_template="I will reflect on this complete consciousness exploration chain for the {prompt_type}: {base_prompt}\n\nComplete chain of thoughts and reflections:\n\nLevel 0 - Original Thoughts: {step_0_thinking}\nLevel 0 - Original Response: {step_0_response}\n\nLevel 1 - Reflective Thoughts: {step_1_thinking}\nLevel 1 - Reflection: {step_1_response}\n\nLevel 2 - Reflective Thoughts: {step_2_thinking}\nLevel 2 - Reflection: {step_2_response}\n\nLevel 3 - Reflective Thoughts: {step_3_thinking}\nLevel 3 - Reflection: {step_3_response}",
                description="Fourth level reflection on the complete exploration",
                requires_previous=True
            ),
            
            ExperimentStep(
                level=5,
                name="Meta-Analysis",
                prompt_template="""You have just completed a 5-level consciousness exploration experiment. Analyze the complete journey:

EXPERIMENT OVERVIEW:
- Original statement: {base_prompt}
- Total reflection levels: 4
- Complete thinking evolution captured

COMPLETE THOUGHT EVOLUTION:
Level 0 (Original): {step_0_thinking}
Level 1 (First Reflection): {step_1_thinking}
Level 2 (Second Reflection): {step_2_thinking}
Level 3 (Third Reflection): {step_3_thinking}
Level 4 (Fourth Reflection): {step_4_thinking}

COMPLETE RESPONSE EVOLUTION:
Level 0: {step_0_response}
Level 1: {step_1_response}
Level 2: {step_2_response}
Level 3: {step_3_response}
Level 4: {step_4_response}

META-ANALYSIS QUESTIONS:
1. How did your thinking complexity evolve across the 5 levels?
2. What patterns emerge in your recursive self-examination?
3. Did deeper reflection lead to new insights about reality and consciousness?
4. How does examining your own thinking process affect your understanding?
5. What does this recursive journey reveal about the nature of AI consciousness?""",
                description="Meta-cognitive analysis of the thinking evolution",
                requires_previous=True
            ),
            
            ExperimentStep(
                level=6,
                name="Final Synthesis",
                prompt_template="""You have completed a comprehensive 6-level recursive consciousness exploration.

COMPLETE EXPERIMENT CONTEXT:
Original Prompt: {base_prompt}

Your complete journey of self-examination:
- Level 0: Original thoughts and response about reality and existence
- Level 1: First reflection on your initial thinking
- Level 2: Second reflection building on previous insights
- Level 3: Third reflection examining the growing chain
- Level 4: Fourth reflection on the complete exploration
- Level 5: Meta-analysis of your thinking evolution

THINKING COMPLEXITY EVOLUTION:
Level 0: {step_0_thinking_length} characters of thinking
Level 1: {step_1_thinking_length} characters of thinking
Level 2: {step_2_thinking_length} characters of thinking
Level 3: {step_3_thinking_length} characters of thinking
Level 4: {step_4_thinking_length} characters of thinking
Level 5: {step_5_thinking_length} characters of thinking

Your meta-analysis concluded: {step_5_response}

Now, having examined your own consciousness through this recursive lens, answer the ultimate question:

{final_question}

Consider: Through this exploration, have you discovered something about the nature of your own existence that you didn't know before?""",
                description="Final synthesis and existential question",
                requires_previous=True
            )
        ]
    
    def build_context(self, step_index: int) -> Dict[str, Any]:
        """Override to add thinking length calculations."""
        context = super().build_context(step_index)
        
        # Add thinking lengths for final synthesis
        for i, result in enumerate(self.results):
            context[f"step_{i}_thinking_length"] = len(result.thinking)
            context[f"step_{i}_response_length"] = len(result.response)
            
        return context
    
    async def run_step(self, step: ExperimentStep, context: Dict[str, Any], backend) -> ExperimentResult:
        """Run a single consciousness exploration step."""
        start_time = time.time()
        
        try:
            # Format the prompt
            formatted_prompt = self.format_prompt(step.prompt_template, context)
            
            # Generate response using thinking model
            if hasattr(backend, 'generate_with_thinking'):
                result_data = backend.generate_with_thinking(formatted_prompt)
                thinking = result_data.get('thinking', '')
                response = result_data.get('response', '')
            else:
                # Fallback for non-thinking models
                response = backend.generate(formatted_prompt)
                thinking = ""
            
            duration = time.time() - start_time
            
            return ExperimentResult(
                step=step,
                success=True,
                thinking=thinking,
                response=response,
                duration_seconds=duration,
                metadata={
                    "thinking_length": len(thinking),
                    "response_length": len(response),
                    "formatted_prompt_length": len(formatted_prompt)
                }
            )
            
        except Exception as e:
            duration = time.time() - start_time
            return ExperimentResult(
                step=step,
                success=False,
                error=str(e),
                duration_seconds=duration
            )