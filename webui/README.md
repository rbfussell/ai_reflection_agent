# AI Reflection Agent WebUI

A modern web interface for running consciousness exploration experiments and analyzing AI responses.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- AI Reflection Agent package installed
- LM Studio, Claude API, or other backend configured

### Installation
```bash
# Install additional WebUI dependencies
pip install gradio plotly pandas numpy

# Or install from requirements.txt
pip install -r ../requirements.txt
```

### Launch WebUI
```bash
# From the webui directory
python run_webui.py

# Or with custom settings
python run_webui.py --host 0.0.0.0 --port 8080 --share
```

The WebUI will be available at `http://localhost:7860` by default.

## 📋 Features

### 🧠 Consciousness Experiments
- **Script-based experiments**: Configurable experiment templates
- **Real-time progress**: Live updates during long-running experiments
- **Thinking model support**: Capture explicit reasoning with `<think>` tags
- **Multi-backend support**: LM Studio, Claude, OpenAI, local models

### 📊 Data Visualization  
- **Thinking evolution charts**: Visualize complexity progression
- **Model performance metrics**: Success rates and comparisons
- **Response analysis**: Length trends and patterns
- **Export capabilities**: PNG, PDF, SVG formats

### 📋 Log Browser
- **Search and filter**: Find entries by content, date, model
- **Detailed view**: Full responses with thinking processes
- **Export options**: JSON, CSV, Markdown formats

### ⚖️ Response Comparison
- **Side-by-side comparison**: Compare responses from different models
- **Similarity analysis**: Semantic similarity scoring
- **Diff visualization**: Highlight text differences
- **Statistical metrics**: Length, complexity, and performance comparisons

## 🏗️ Architecture

### Directory Structure
```
webui/
├── app.py                     # Main Gradio application
├── run_webui.py              # Startup script
├── components/               # UI Components
│   ├── consciousness_experiment.py
│   ├── log_browser.py
│   ├── comparison.py
│   └── visualization.py
├── scripts/                  # Experiment Scripts
│   ├── base_script.py       # Base classes
│   ├── consciousness_scripts/
│   │   ├── default.py       # Default 7-level experiment
│   │   └── templates/       # Script templates
│   └── analysis_scripts/    # Analysis tools
├── utils/                   # Utilities
│   └── session_manager.py   # Session management
└── static/                  # Static assets
```

### Script System
The WebUI uses a modular script system for experiments:

- **BaseExperimentScript**: Abstract base class for all experiments
- **ScriptConfig**: Configuration and metadata
- **ExperimentStep**: Individual experiment steps
- **ExperimentResult**: Results from each step

### Creating Custom Scripts
```python
from webui.scripts.base_script import BaseExperimentScript, ScriptConfig, ExperimentStep

class MyCustomScript(BaseExperimentScript):
    def get_config(self) -> ScriptConfig:
        return ScriptConfig(
            name="My Custom Experiment",
            description="Description of the experiment",
            parameters={"param1": "value1"}
        )
    
    def define_steps(self) -> List[ExperimentStep]:
        return [
            ExperimentStep(
                level=0,
                name="Step 1",
                prompt_template="Your prompt template here",
                description="What this step does"
            )
        ]
    
    async def run_step(self, step, context, backend):
        # Implementation here
        pass
```

## 🔧 Configuration

### Backend Configuration
The WebUI supports multiple AI backends:

- **LM Studio**: Local models with thinking support
- **Claude**: Anthropic's Claude models
- **OpenAI**: GPT models
- **Local**: Custom local model endpoints
- **Mock**: For testing without API calls

### Settings
Access settings through the WebUI Settings tab:

- Default backend and model selection
- Logging configuration
- Export settings
- Theme customization

## 📊 Data Flow

1. **User Input**: Configure experiment through WebUI
2. **Script Execution**: Selected script runs with configured backend
3. **Progress Tracking**: Real-time updates via callback system
4. **Result Processing**: Compile thinking processes and responses
5. **Visualization**: Generate charts and analysis
6. **Export**: Save results in chosen format

## 🔍 Troubleshooting

### Common Issues

**WebUI won't start**
- Check Python version (3.8+ required)
- Install missing dependencies: `pip install -r ../requirements.txt`
- Check port availability

**Backend connection failed** 
- Verify LM Studio/API service is running
- Check endpoint URL and API keys
- Test connection using the "Test Connection" button

**Experiments fail silently**
- Check browser console for JavaScript errors
- Verify backend model supports the required features
- Check log files for detailed error messages

**Unicode display issues**
- Update to latest Gradio version
- Check browser font support
- Use the safe print functions in the scripts

### Debug Mode
```bash
python run_webui.py --debug
```

### Log Files
- WebUI logs: `./webui.log`
- Experiment logs: `./consciousness_exploration.jsonl`
- Error logs: Check console output

## 🚧 Future Extensions

The WebUI is designed for extensibility:

- **Plugin System**: Custom analysis tools
- **Multi-user Support**: User accounts and isolated sessions
- **Experiment Scheduling**: Automated experiment runs
- **Advanced Visualizations**: 3D plots, interactive charts
- **Integration APIs**: REST endpoints for external tools
- **Real-time Collaboration**: Shared experiment sessions

## 📚 API Reference

### Script System APIs
- `BaseExperimentScript`: Base class for experiments
- `ScriptConfig`: Configuration structure
- `ExperimentStep`: Step definition
- `ExperimentResult`: Result structure

### Component APIs
- `ConsciousnessExperimentComponent`: Main experiment interface
- `LogBrowserComponent`: Log browsing functionality
- `ComparisonComponent`: Response comparison tools
- `VisualizationComponent`: Data visualization

### Utility APIs
- `SessionManager`: Session state management
- `FileManager`: File operations (future)

## 🤝 Contributing

To add new features:

1. Create new components in `components/`
2. Add experiment scripts to `scripts/`
3. Update the main app in `app.py`
4. Add tests and documentation

## 📄 License

Same as AI Reflection Agent main project.