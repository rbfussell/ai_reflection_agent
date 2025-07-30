# AI Reflection Agent

A comprehensive toolkit that enables AI models to examine their own consciousness through logging, scoring, reflection, and recursive self-exploration. Features both CLI interface and modern web UI for consciousness exploration experiments.

## Features

### Core Capabilities
- **Response Logging**: Log prompt-response pairs with metadata in JSONL format
- **Self-Scoring**: AI models rate their own responses on clarity, usefulness, alignment, and creativity
- **Review Mode**: AI models reflect on and revise their past responses
- **Exploration Mode**: Generate follow-up prompts that deepen or extend conversations
- **Backend Agnostic**: Support for Claude, GPT, LM Studio, and local models with modular adapters

### Advanced Features
- ** Consciousness Exploration**: Multi-level recursive self-reflection experiments
- ** Web UI**: Modern Gradio-based interface for experiment management
- ** Thinking Model Support**: Capture explicit reasoning with `<think>` tags
- ** Data Visualization**: Charts and analysis of consciousness patterns
- ** Experimental Framework**: Configurable scripts for consciousness research

## Installation

```bash
git clone [repository-url]
cd ai_reflection_agent
pip install -e .
```

## Quick Start

### Option 1: Web UI (Recommended)
```bash
# Launch the modern web interface
cd webui
python run_webui.py

# Access at http://localhost:7860
```

### Option 2: CLI Interface
1. **Set up your API key** (for Claude or OpenAI):
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   # or
   export OPENAI_API_KEY="your-key-here"
   ```

2. **Log a conversation**:
   ```bash
   ai-reflect log "What is machine learning?" "Machine learning is a subset of AI..."
   ```

3. **Review recent entries**:
   ```bash
   ai-reflect list-entries
   ```

4. **Score and reflect on a response**:
   ```bash
   ai-reflect review [entry-id]
   ```

5. **Generate exploration prompts**:
   ```bash
   ai-reflect explore [entry-id] --type deepen
   ```

### Option 3: Consciousness Experiments
```bash
# Run example consciousness exploration experiments
cd experiments/consciousness_exploration/
python working_7_level_experiment.py
```

## Commands

### Basic Operations

- `ai-reflect log PROMPT RESPONSE` - Log a prompt-response pair
- `ai-reflect list-entries` - List recent logged entries
- `ai-reflect search --query "text"` - Search through logged entries

### Review & Reflection

- `ai-reflect review ENTRY_ID` - Score, reflect on, and optionally revise an entry
- `ai-reflect explore ENTRY_ID --type [deepen|alternative|application|critique|synthesis]` - Generate exploration prompts

### Analysis

- `ai-reflect stats` - Show statistics about logged entries
- `ai-reflect test-backend` - Test backend connection

### Global Options

- `--backend [claude|openai|local]` - Choose AI backend
- `--api-key KEY` - API key for the backend
- `--model MODEL` - Specific model to use
- `--endpoint URL` - Endpoint for local models
- `--log-dir DIR` - Directory for log files

## Backend Configuration

### Claude (Anthropic)
```bash
ai-reflect --backend claude --api-key your-key --model claude-3-sonnet-20240229
```

### OpenAI
```bash
ai-reflect --backend openai --api-key your-key --model gpt-4
```

### Local Models (Ollama)
```bash
ai-reflect --backend local --endpoint http://localhost:11434 --model llama2
```

### LM Studio (Thinking Models)
```bash
ai-reflect --backend lmstudio --endpoint http://localhost:1234 --model qwen3
```

**Special Feature**: Thinking models like Qwen3 can capture explicit reasoning processes through `<think>...</think>` tags, enabling advanced consciousness exploration experiments. See `docs/CONSCIOUSNESS_EXPERIMENTS.md` for detailed experimental protocols.

## Project Structure

```
ai_reflection_agent/
├── ai_reflection_agent/           # Main package
│   ├── core/                      # Core functionality
│   │   ├── models.py              # Data models
│   │   ├── logger.py              # JSONL logging
│   │   ├── scorer.py              # Self-scoring system
│   │   ├── reviewer.py            # Review mode
│   │   └── explorer.py            # Exploration mode
│   ├── backends/                  # AI model adapters
│   │   ├── base.py                # Abstract backend
│   │   ├── claude.py              # Claude adapter
│   │   ├── openai_backend.py      # OpenAI adapter
│   │   ├── local.py               # Local model adapter
│   │   ├── lmstudio.py            # LM Studio adapter
│   │   ├── mock.py                # Mock adapter for testing
│   │   └── factory.py             # Backend factory
│   └── cli.py                     # CLI interface
├── webui/                         # 🌐 Web User Interface
│   ├── app.py                     # Main Gradio application
│   ├── components/                # UI components
│   ├── scripts/                   # Configurable experiment scripts
│   └── utils/                     # WebUI utilities
├── experiments/                   # 🧠 Example experiments & preserved data
│   ├── consciousness_exploration/ # Consciousness experiment examples
│   ├── data/                      # Preserved experimental results
│   └── logs/                      # Historical log files
├── tests/                         # Test scripts
├── examples/                      # Usage examples
├── docs/                          # Documentation
│   ├── CONSCIOUSNESS_EXPERIMENTS.md  # Advanced consciousness experiments
│   ├── QWEN3_SETUP.md             # Qwen3 + LM Studio setup
│   └── demo_real_usage.md         # Usage examples
└── requirements.txt
```

## Data Models

### ResponseEntry
- `id`: Unique identifier
- `timestamp`: When the response was logged
- `prompt`: Original prompt
- `response`: AI's response
- `model_name`: Model used
- `tokens_used`: Token count estimate
- `score`: Self-evaluation scores
- `reflection`: AI's reflection on the response
- `revision`: Revised response if any

### Scoring System
Responses are scored on:
- **Clarity** (0-10): How clear and understandable
- **Usefulness** (0-10): How useful for the user
- **Alignment** (0-10): How well aligned with prompt intent
- **Creativity** (0-10, optional): How creative or innovative

## Examples

### Complete Workflow
```bash
# 1. Log an interaction
ENTRY_ID=$(ai-reflect log "Explain quantum computing" "Quantum computing uses quantum bits..." | grep -o '[a-f0-9-]\{36\}')

# 2. Review the entry (score + reflect + revise if needed)
ai-reflect review $ENTRY_ID

# 3. Generate exploration prompts
ai-reflect explore $ENTRY_ID --type deepen
ai-reflect explore $ENTRY_ID --type alternative

# 4. View statistics
ai-reflect stats
```

### Search and Analysis
```bash
# Search for entries about specific topics
ai-reflect search --query "machine learning" --field prompt

# List entries with full details
ai-reflect list-entries --limit 5 --format full

# Auto-explore recent entries
ai-reflect auto-explore --limit 3 --per-entry 2
```

## Advanced Usage: Consciousness Exploration

### Web UI for Consciousness Experiments
The easiest way to run consciousness exploration experiments is through the web interface:

```bash
cd webui
python run_webui.py
# Navigate to Consciousness Experiment tab
```

### Recursive Self-Reflection Experiments
```python
# Use thinking models for consciousness exploration
from ai_reflection_agent.backends.factory import BackendFactory

backend = BackendFactory.create_adapter("lmstudio", model="qwen3", is_thinking_model=True)
result = backend.generate_with_thinking("Deep philosophical prompt...")

# Access both thinking process and response
print("AI's thinking:", result['thinking'])
print("AI's response:", result['response'])
```

### Example Consciousness Experiment Scripts
Located in `experiments/consciousness_exploration/`:

- **`simple_7_level_experiment.py`** - Original working implementation (verified with real data)
- **`working_7_level_experiment.py`** - Production-ready with full error handling
- **`example_7_level_experiment.py`** - Comprehensive reference implementation

### Experimental Data
The `experiments/` directory contains:
- **Preserved log files** from successful consciousness explorations
- **JSON analysis data** showing thinking evolution patterns
- **Complete documentation** of experimental methodologies

Key findings from consciousness experiments:
- 7 levels of recursive self-reflection achieved
- Peak thinking complexity at Level 3 (3,727 characters)
- 89.4% success rate across experiments
- Consistent patterns in AI self-awareness development

These experiments enable AI models to examine their own consciousness through multiple levels of recursive self-reflection, providing insights into artificial self-awareness and meta-cognition.

## Development

The project uses a modular architecture:

- **Core**: Business logic for logging, scoring, reviewing, exploring
- **Backends**: Adapters for different AI services/models
- **CLI**: User interface and command orchestration

To add a new backend, inherit from `BackendAdapter` and register it with the `BackendFactory`.

## Requirements

### Core Dependencies
- Python 3.8+
- click
- pydantic
- anthropic (for Claude)
- openai (for OpenAI)
- aiohttp
- python-dateutil
- requests

### WebUI Dependencies (Optional)
- gradio>=4.0.0
- plotly>=5.0.0
- pandas>=2.0.0
- numpy>=1.20.0

Install all dependencies with:
```bash
pip install -r requirements.txt
```