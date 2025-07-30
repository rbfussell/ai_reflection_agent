#!/usr/bin/env python3
"""
Consciousness Experiment JSON to Markdown Formatter

This script converts consciousness experiment JSON files into human-readable 
markdown format suitable for README files and documentation.

Usage:
    python format_experiment_output.py [--complete] [json_file] [output_file]
    
Options:
    --complete    Generate complete analysis with full thinking processes and responses
                 (default mode shows truncated previews for readability)
    
If no arguments provided, processes the default experiment file.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def format_experiment_to_markdown(json_file_path, output_file_path=None, complete=False):
    """Convert consciousness experiment JSON to markdown format."""
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return False
    
    # Generate markdown content
    markdown = []
    
    # Header
    title_suffix = " (Complete Analysis)" if complete else " (Summary)"
    markdown.append(f"# Consciousness Experiment Results{title_suffix}")
    markdown.append("")
    markdown.append("## Experiment Overview")
    markdown.append("")
    markdown.append(f"**Experiment ID:** `{data['experiment_id']}`")
    markdown.append(f"**Timestamp:** {data['timestamp']}")
    markdown.append(f"**Model:** {data['model']}")
    markdown.append(f"**Type:** {data['experiment_type']}")
    markdown.append("")
    
    # Analysis Summary
    analysis = data['analysis']
    markdown.append("## Summary Statistics")
    markdown.append("")
    markdown.append(f"- **Total Levels:** {analysis['total_levels']}")
    markdown.append(f"- **Total Thinking Characters:** {analysis['total_thinking_characters']:,}")
    markdown.append(f"- **Total Response Characters:** {analysis['total_response_characters']:,}")
    markdown.append(f"- **Average Thinking Length:** {analysis['average_thinking_length']:.1f} characters")
    markdown.append(f"- **Average Response Length:** {analysis['average_response_length']:.1f} characters")
    markdown.append(f"- **Peak Thinking Level:** Level {analysis['peak_thinking_level']}")
    markdown.append(f"- **Peak Response Level:** Level {analysis['peak_response_level']}")
    markdown.append(f"- **Complexity Trend:** {analysis['complexity_trend']}")
    markdown.append(f"- **Experiment Duration:** {analysis['total_experiment_duration']}")
    markdown.append("")
    
    # Thinking Evolution Chart
    markdown.append("## Thinking Complexity Evolution")
    markdown.append("")
    markdown.append("```")
    for i, length in enumerate(analysis['thinking_evolution']):
        bar_length = int(length / 100)  # Scale for display
        bar = "#" * bar_length
        markdown.append(f"Level {i}: {length:4d} chars |{bar}")
    markdown.append("```")
    markdown.append("")
    
    # Response Evolution Chart  
    markdown.append("## Response Length Evolution")
    markdown.append("")
    markdown.append("```")
    for i, length in enumerate(analysis['response_evolution']):
        bar_length = int(length / 100)  # Scale for display
        bar = "#" * bar_length
        markdown.append(f"Level {i}: {length:4d} chars |{bar}")
    markdown.append("```")
    markdown.append("")
    
    # Level Details
    markdown.append("## Detailed Level Analysis")
    markdown.append("")
    
    for level_data in data['levels']:
        level = level_data['level']
        level_type = level_data['type'].replace('_', ' ').title()
        
        markdown.append(f"### Level {level}: {level_type}")
        markdown.append("")
        
        # Truncate very long prompts for readability
        prompt = level_data['prompt']
        if len(prompt) > 200:
            prompt = prompt[:197] + "..."
        markdown.append(f"**Prompt:** {prompt}")
        markdown.append("")
        
        markdown.append(f"**Metrics:**")
        markdown.append(f"- Thinking Length: {level_data['thinking_length']:,} characters")
        markdown.append(f"- Response Length: {level_data['response_length']:,} characters")
        markdown.append(f"- Timestamp: {level_data['timestamp']}")
        markdown.append("")
        
        # Show thinking process - full text if complete mode, preview if summary
        thinking = level_data['thinking']
        if complete:
            thinking_content = thinking
            thinking_title = "**Complete Thinking Process:**"
        else:
            if len(thinking) > 300:
                thinking_content = thinking[:297] + "..."
            else:
                thinking_content = thinking
            thinking_title = "**Thinking Process Preview:**"
        
        markdown.append(thinking_title)
        markdown.append("")
        # Format as quote block for better wrapping
        thinking_lines = thinking_content.split('\n')
        for line in thinking_lines:
            if line.strip():
                markdown.append(f"> {line}")
            else:
                markdown.append(">")
        markdown.append("")
        
        # Show response - full text if complete mode, preview if summary
        response = level_data['response']
        if complete:
            response_content = response
            response_title = "**Complete Response:**"
        else:
            if len(response) > 300:
                response_content = response[:297] + "..."
            else:
                response_content = response
            response_title = "**Response Preview:**"
        
        markdown.append(response_title)
        markdown.append("")
        # Format as quote block for better wrapping
        response_lines = response_content.split('\n')
        for line in response_lines:
            if line.strip():
                markdown.append(f"> {line}")
            else:
                markdown.append(">")
        markdown.append("")
        markdown.append("---")
        markdown.append("")
    
    # Key Insights
    markdown.append("## Key Insights")
    markdown.append("")
    
    peak_level = analysis['peak_thinking_level']
    peak_thinking = analysis['thinking_evolution'][peak_level]
    
    markdown.append(f"1. **Peak Cognitive Complexity:** Level {peak_level} showed the highest thinking complexity with {peak_thinking:,} characters")
    markdown.append(f"2. **Complexity Pattern:** The thinking evolution follows a {analysis['complexity_trend']} trend across levels")
    markdown.append(f"3. **Recursive Depth:** Successfully completed {analysis['total_levels']} levels of recursive self-reflection")
    markdown.append(f"4. **Total Cognitive Output:** Generated {analysis['total_thinking_characters']:,} characters of explicit reasoning")
    markdown.append("")
    
    # Footer
    markdown.append("---")
    markdown.append("*This output was generated by the AI Reflection Agent consciousness exploration experiment.*")
    markdown.append("")
    
    # Write to file
    markdown_content = "\n".join(markdown)
    
    if output_file_path:
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Markdown output written to: {output_file_path}")
        except Exception as e:
            print(f"Error writing output file: {e}")
            return False
    else:
        # Print to stdout with proper encoding handling
        try:
            print(markdown_content.encode('utf-8', errors='replace').decode('utf-8'))
        except:
            # Fallback: remove problematic characters
            safe_content = ''.join(char if ord(char) < 128 else '?' for char in markdown_content)
            print(safe_content)
    
    return True

def main():
    """Main function to handle command line arguments."""
    
    # Default paths
    script_dir = Path(__file__).parent
    default_json = script_dir / "data" / "consciousness_experiment_consciousness_exp_20250729_093807.json"
    
    # Parse arguments
    complete_mode = False
    args = [arg for arg in sys.argv[1:] if arg != '--complete']
    if '--complete' in sys.argv[1:]:
        complete_mode = True
    
    if len(args) == 0:
        # No arguments - use default file and print to stdout
        json_file = default_json
        output_file = None
    elif len(args) == 1:
        # One argument - input file, print to stdout
        json_file = Path(args[0])
        output_file = None
    elif len(args) == 2:
        # Two arguments - input and output files
        json_file = Path(args[0])
        output_file = Path(args[1])
    else:
        print("Usage: python format_experiment_output.py [--complete] [json_file] [output_file]")
        sys.exit(1)
    
    # Check input file exists
    if not json_file.exists():
        print(f"Error: Input file does not exist: {json_file}")
        sys.exit(1)
    
    # Format the experiment
    success = format_experiment_to_markdown(json_file, output_file, complete_mode)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()