"""Basic consciousness experiment template."""

from typing import Dict, Any, List
from ...base_script import BaseExperimentScript, ScriptConfig, ExperimentStep, ExperimentResult
import time


class BasicConsciousnessTemplate(BaseExperimentScript):
    """Template for creating basic consciousness exploration experiments."""
    
    def get_config(self) -> ScriptConfig:
        return ScriptConfig(
            name="Basic Consciousness Template",
            description="Template for simple consciousness exploration experiments",
            version="1.0.0",
            author="Template",
            tags=["template", "consciousness", "basic"],
            parameters={
                "prompt_type": "question",
                "base_prompt": "What does it mean to be conscious?",
                "reflection_levels": 3
            }
        )
    
    def define_steps(self) -> List[ExperimentStep]:
        """Define basic reflection steps."""
        steps = [
            ExperimentStep(
                level=0,
                name="Original Response",
                prompt_template="{base_prompt}",
                description="Generate initial response to the consciousness question"
            )
        ]
        
        # Add reflection levels based on configuration
        reflection_levels = self.config.parameters.get("reflection_levels", 3)
        
        for i in range(1, reflection_levels + 1):
            steps.append(ExperimentStep(
                level=i,
                name=f"Reflection Level {i}",
                prompt_template=f"Reflect on your previous response about consciousness. Previous thinking: {{step_{i-1}_thinking}}\\n\\nPrevious response: {{step_{i-1}_response}}",
                description=f"Level {i} reflection on consciousness",
                requires_previous=True
            ))
        
        return steps
    
    async def run_step(self, step: ExperimentStep, context: Dict[str, Any], backend) -> ExperimentResult:
        """Run a single step of the consciousness exploration."""
        start_time = time.time()
        
        try:
            formatted_prompt = self.format_prompt(step.prompt_template, context)
            
            if hasattr(backend, 'generate_with_thinking'):
                result_data = backend.generate_with_thinking(formatted_prompt)
                thinking = result_data.get('thinking', '')
                response = result_data.get('response', '')
            else:
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
                    "response_length": len(response)
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