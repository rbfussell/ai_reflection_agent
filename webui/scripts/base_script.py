"""Base classes for experiment scripts."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScriptConfig:
    """Configuration for an experiment script."""
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "Unknown"
    tags: List[str] = None
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.parameters is None:
            self.parameters = {}


@dataclass 
class ExperimentStep:
    """A single step in an experiment."""
    level: int
    name: str
    prompt_template: str
    description: str = ""
    requires_previous: bool = True
    timeout_seconds: int = 120


@dataclass
class ExperimentResult:
    """Result from running an experiment step."""
    step: ExperimentStep
    success: bool
    thinking: str = ""
    response: str = ""
    error: Optional[str] = None
    duration_seconds: float = 0.0
    timestamp: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


class BaseExperimentScript(ABC):
    """Base class for all experiment scripts."""
    
    def __init__(self):
        self.config = self.get_config()
        self.steps = self.define_steps()
        self.results: List[ExperimentResult] = []
        self.progress_callback: Optional[Callable] = None
        
    @abstractmethod
    def get_config(self) -> ScriptConfig:
        """Return the script configuration."""
        pass
        
    @abstractmethod
    def define_steps(self) -> List[ExperimentStep]:
        """Define the experiment steps."""
        pass
        
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """Set callback for progress updates: (current_step, total_steps, message)"""
        self.progress_callback = callback
        
    def _notify_progress(self, current_step: int, message: str):
        """Notify progress callback if available."""
        if self.progress_callback:
            self.progress_callback(current_step, len(self.steps), message)
            
    def format_prompt(self, template: str, context: Dict[str, Any]) -> str:
        """Format a prompt template with context variables."""
        try:
            return template.format(**context)
        except KeyError as e:
            raise ValueError(f"Missing context variable for prompt: {e}")
            
    def build_context(self, step_index: int) -> Dict[str, Any]:
        """Build context for prompt formatting from previous results."""
        context = {
            "step_index": step_index,
            "step_name": self.steps[step_index].name,
            **self.config.parameters
        }
        
        # Add results from previous steps
        for i, result in enumerate(self.results):
            context[f"step_{i}_thinking"] = result.thinking
            context[f"step_{i}_response"] = result.response
            context[f"step_{i}_name"] = result.step.name
            
        # Add specific context for common patterns
        if self.results:
            context["original_thinking"] = self.results[0].thinking if self.results else ""
            context["original_response"] = self.results[0].response if self.results else ""
            context["previous_thinking"] = self.results[-1].thinking if self.results else ""
            context["previous_response"] = self.results[-1].response if self.results else ""
            
        return context
        
    @abstractmethod
    async def run_step(self, step: ExperimentStep, context: Dict[str, Any], backend) -> ExperimentResult:
        """Run a single experiment step."""
        pass
        
    async def run_experiment(self, backend, start_from: int = 0) -> List[ExperimentResult]:
        """Run the complete experiment."""
        self.results = self.results[:start_from]  # Keep previous results if resuming
        
        for i in range(start_from, len(self.steps)):
            step = self.steps[i]
            
            self._notify_progress(i, f"Starting {step.name}...")
            
            try:
                context = self.build_context(i)
                result = await self.run_step(step, context, backend)
                self.results.append(result)
                
                if not result.success:
                    self._notify_progress(i, f"Step failed: {result.error}")
                    if step.requires_previous:
                        break
                else:
                    self._notify_progress(i, f"Completed {step.name}")
                    
            except Exception as e:
                error_result = ExperimentResult(
                    step=step,
                    success=False,
                    error=str(e)
                )
                self.results.append(error_result)
                self._notify_progress(i, f"Step error: {str(e)}")
                
                if step.requires_previous:
                    break
                    
        self._notify_progress(len(self.results), "Experiment completed")
        return self.results
        
    def get_summary(self) -> Dict[str, Any]:
        """Get experiment summary statistics."""
        if not self.results:
            return {"status": "not_started"}
            
        successful_steps = sum(1 for r in self.results if r.success)
        total_thinking_chars = sum(len(r.thinking) for r in self.results if r.success)
        total_response_chars = sum(len(r.response) for r in self.results if r.success)
        
        return {
            "status": "completed" if successful_steps == len(self.steps) else "partial",
            "total_steps": len(self.steps),
            "completed_steps": successful_steps,
            "success_rate": successful_steps / len(self.steps) if self.steps else 0,
            "total_thinking_characters": total_thinking_chars,
            "total_response_characters": total_response_chars,
            "thinking_evolution": [len(r.thinking) for r in self.results if r.success],
            "response_evolution": [len(r.response) for r in self.results if r.success],
            "duration_total": sum(r.duration_seconds for r in self.results),
            "config": self.config
        }