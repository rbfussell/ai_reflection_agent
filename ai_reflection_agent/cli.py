"""Command-line interface for the AI Reflection Agent."""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List

import click

from .core.logger import ResponseLogger, ExplorationLogger
from .core.scorer import SelfScorer  
from .core.reviewer import ResponseReviewer
from .core.explorer import PromptExplorer
from .backends.factory import BackendFactory


class ReflectionAgent:
    """Main class coordinating all reflection functionality."""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize the reflection agent."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.response_logger = ResponseLogger(self.log_dir / "responses.jsonl")
        self.exploration_logger = ExplorationLogger(self.log_dir / "explorations.jsonl")
        self.scorer = SelfScorer()
        self.reviewer = ResponseReviewer(self.response_logger, self.scorer)
        self.explorer = PromptExplorer(self.response_logger, self.exploration_logger)
        
        self.backend = None
    
    def setup_backend(self, backend_type: str, **kwargs):
        """Setup the AI backend."""
        self.backend = BackendFactory.create_adapter(backend_type, **kwargs)
    
    def log_interaction(self, prompt: str, response: str, model_name: str = None) -> str:
        """Log a prompt-response interaction."""
        if not model_name and self.backend:
            model_name = self.backend.get_model_name()
        
        tokens_used = None
        if self.backend:
            tokens_used = self.backend.estimate_tokens(prompt + response)
        
        return self.response_logger.log_response(
            prompt=prompt,
            response=response,
            model_name=model_name or "unknown",
            tokens_used=tokens_used
        )


@click.group()
@click.option('--log-dir', default='logs', help='Directory for log files')
@click.option('--backend', default='claude', help='AI backend to use (claude, openai, local)')
@click.option('--api-key', help='API key for the backend')
@click.option('--model', help='Model name to use')
@click.option('--endpoint', help='Endpoint URL for local backends')
@click.pass_context
def cli(ctx, log_dir, backend, api_key, model, endpoint):
    """AI Reflection Agent - A tool for AI models to reflect on their responses."""
    ctx.ensure_object(dict)
    
    agent = ReflectionAgent(log_dir)
    
    # Setup backend
    backend_kwargs = {}
    if api_key:
        backend_kwargs['api_key'] = api_key
    if model:
        backend_kwargs['model'] = model
    if endpoint:
        backend_kwargs['endpoint'] = endpoint
    
    try:
        agent.setup_backend(backend, **backend_kwargs)
    except Exception as e:
        click.echo(f"Warning: Failed to setup backend: {e}", err=True)
    
    ctx.obj['agent'] = agent


@cli.command()
@click.argument('prompt', required=True)
@click.argument('response', required=True)
@click.option('--model-name', help='Override model name for logging')
@click.pass_context
def log(ctx, prompt, response, model_name):
    """Log a prompt-response pair."""
    agent = ctx.obj['agent']
    entry_id = agent.log_interaction(prompt, response, model_name)
    click.echo(f"Logged interaction with ID: {entry_id}")


@cli.command()
@click.option('--limit', default=10, help='Number of recent entries to show')
@click.option('--format', 'output_format', default='summary', 
              type=click.Choice(['summary', 'full', 'json']), 
              help='Output format')
@click.pass_context
def list_entries(ctx, limit, output_format):
    """List recent logged entries."""
    agent = ctx.obj['agent']
    entries = agent.response_logger.get_recent_entries(limit)
    
    if output_format == 'json':
        click.echo(json.dumps([entry.model_dump() for entry in entries], indent=2, default=str))
    elif output_format == 'full':
        for entry in entries:
            click.echo(f"\n{'='*50}")
            click.echo(f"ID: {entry.id}")
            click.echo(f"Timestamp: {entry.timestamp}")
            click.echo(f"Model: {entry.model_name}")
            click.echo(f"\nPrompt: {entry.prompt}")
            click.echo(f"\nResponse: {entry.response}")
            if entry.score:
                click.echo(f"\nScores: {agent.scorer.get_score_summary(entry.score)}")
    else:  # summary
        click.echo(f"{'ID':<36} {'Timestamp':<20} {'Model':<20} {'Prompt Preview'}")
        click.echo("-" * 100)
        for entry in entries:
            prompt_preview = entry.prompt[:40] + "..." if len(entry.prompt) > 40 else entry.prompt
            click.echo(f"{entry.id:<36} {str(entry.timestamp)[:19]:<20} {entry.model_name:<20} {prompt_preview}")


@cli.command()
@click.argument('entry_id', required=True)
@click.pass_context
def review(ctx, entry_id):
    """Review an entry (score, reflect, and optionally revise)."""
    agent = ctx.obj['agent']
    
    if not agent.backend:
        click.echo("Error: No backend configured. Use --backend and --api-key options.", err=True)
        return
    
    click.echo(f"Reviewing entry {entry_id}...")
    
    try:
        result = agent.reviewer.review_entry(entry_id, agent.backend)
        
        if "error" in result:
            click.echo(f"Error: {result['error']}", err=True)
            return
        
        click.echo("Review completed:")
        for step in result["steps"]:
            step_name = step.get("step", "unknown")
            if step.get("success"):
                click.echo(f"✓ {step_name.title()} completed")
                if step_name == "scoring" and "score" in step:
                    scores = agent.scorer.get_score_summary(step["score"])
                    click.echo(f"  Scores: {scores}")
            else:
                click.echo(f"✗ {step_name.title()} failed: {step.get('error', 'Unknown error')}")
    
    except Exception as e:
        click.echo(f"Error during review: {e}", err=True)


@cli.command()
@click.argument('entry_id', required=True)
@click.option('--type', 'exploration_type', default='deepen',
              type=click.Choice(['deepen', 'alternative', 'application', 'critique', 'synthesis']),
              help='Type of exploration to generate')
@click.pass_context
def explore(ctx, entry_id, exploration_type):
    """Generate exploration prompts for an entry."""
    agent = ctx.obj['agent']
    
    if not agent.backend:
        click.echo("Error: No backend configured. Use --backend and --api-key options.", err=True)
        return
    
    click.echo(f"Generating {exploration_type} exploration for entry {entry_id}...")
    
    try:
        result = agent.explorer.generate_exploration_prompt(entry_id, exploration_type, agent.backend)
        
        if result.get("success"):
            click.echo(f"✓ Exploration generated (ID: {result['exploration_id']})")
            click.echo(f"\nGenerated prompt:\n{result['generated_prompt']}")
        else:
            click.echo(f"✗ Failed to generate exploration: {result.get('error', 'Unknown error')}", err=True)
    
    except Exception as e:
        click.echo(f"Error during exploration: {e}", err=True)


@cli.command()
@click.option('--limit', default=5, help='Number of recent entries to auto-explore')
@click.option('--per-entry', default=2, help='Number of explorations per entry')
@click.pass_context
def auto_explore(ctx, limit, per_entry):
    """Automatically explore recent entries."""
    agent = ctx.obj['agent']
    
    if not agent.backend:
        click.echo("Error: No backend configured. Use --backend and --api-key options.", err=True)
        return
    
    click.echo(f"Auto-exploring {limit} recent entries...")
    
    try:
        result = agent.explorer.explore_recent_entries(agent.backend, limit, per_entry)
        
        click.echo(f"Processed {result['total_entries']} entries")
        click.echo(f"Generated {result['successful_explorations']}/{result['total_explorations']} explorations")
        
        for entry_result in result['entry_results']:
            if 'explorations' in entry_result:
                click.echo(f"\nEntry {entry_result['entry_id']}: {entry_result['successful']}/{entry_result['total']} successful")
    
    except Exception as e:
        click.echo(f"Error during auto-exploration: {e}", err=True)


@cli.command()
@click.option('--query', help='Search query')
@click.option('--field', default='prompt', help='Field to search in')
@click.pass_context
def search(ctx, query, field):
    """Search logged entries."""
    agent = ctx.obj['agent']
    
    if not query:
        query = click.prompt('Enter search query')
    
    entries = agent.response_logger.search_entries(query, field)
    
    if not entries:
        click.echo("No entries found.")
        return
    
    click.echo(f"Found {len(entries)} entries:")
    click.echo(f"{'ID':<36} {'Timestamp':<20} {'Model':<20} {'Match Preview'}")
    click.echo("-" * 100)
    
    for entry in entries:
        field_value = getattr(entry, field, "")
        match_preview = field_value[:40] + "..." if len(field_value) > 40 else field_value
        click.echo(f"{entry.id:<36} {str(entry.timestamp)[:19]:<20} {entry.model_name:<20} {match_preview}")


@cli.command()
@click.pass_context
def test_backend(ctx):
    """Test the backend connection."""
    agent = ctx.obj['agent']
    
    if not agent.backend:
        click.echo("Error: No backend configured.", err=True)
        return
    
    click.echo("Testing backend connection...")
    result = agent.backend.test_connection()
    
    if result.get("success"):
        click.echo("✓ Backend connection successful")
        for key, value in result.items():
            if key != "success":
                click.echo(f"  {key}: {value}")
    else:
        click.echo(f"✗ Backend connection failed: {result.get('error', 'Unknown error')}", err=True)


@cli.command()
@click.pass_context
def stats(ctx):
    """Show statistics about logged entries."""
    agent = ctx.obj['agent']
    
    entries = list(agent.response_logger.read_entries())
    explorations = list(agent.exploration_logger.read_explorations())
    
    if not entries:
        click.echo("No entries found.")
        return
    
    # Basic stats
    total_entries = len(entries)
    scored_entries = sum(1 for e in entries if e.score is not None)
    reflected_entries = sum(1 for e in entries if e.reflection is not None)
    revised_entries = sum(1 for e in entries if e.revision is not None)
    
    # Model stats
    models = {}
    for entry in entries:
        models[entry.model_name] = models.get(entry.model_name, 0) + 1
    
    click.echo(f"Total entries: {total_entries}")
    click.echo(f"Scored entries: {scored_entries}")
    click.echo(f"Reflected entries: {reflected_entries}")
    click.echo(f"Revised entries: {revised_entries}")
    click.echo(f"Total explorations: {len(explorations)}")
    
    click.echo("\nModels used:")
    for model, count in models.items():
        click.echo(f"  {model}: {count}")
    
    # Average scores
    if scored_entries > 0:
        total_clarity = sum(e.score.clarity for e in entries if e.score)
        total_usefulness = sum(e.score.usefulness for e in entries if e.score)
        total_alignment = sum(e.score.alignment for e in entries if e.score)
        
        click.echo(f"\nAverage scores:")
        click.echo(f"  Clarity: {total_clarity / scored_entries:.2f}")
        click.echo(f"  Usefulness: {total_usefulness / scored_entries:.2f}")
        click.echo(f"  Alignment: {total_alignment / scored_entries:.2f}")


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()