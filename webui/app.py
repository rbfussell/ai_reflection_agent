"""Main Gradio WebUI application for AI Reflection Agent."""

import gradio as gr
import os
import sys
from pathlib import Path

# Add parent directory to path to import ai_reflection_agent
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from components.consciousness_experiment import consciousness_experiment_component
from components.log_browser import log_browser_component
from components.comparison import comparison_component
from components.visualization import visualization_component
from utils.session_manager import session_manager


class AIReflectionWebUI:
    """Main WebUI application class."""
    
    def __init__(self):
        self.title = "🧠 AI Reflection Agent"
        self.description = """
        **AI Reflection Agent WebUI** - Explore consciousness, analyze responses, and visualize AI thinking patterns.
        
        Features:
        - 🧠 **Consciousness Experiments**: Run recursive self-reflection experiments
        - 📋 **Log Browser**: Browse and search through response logs  
        - ⚖️ **Response Comparison**: Compare responses across models and experiments
        - 📊 **Data Visualization**: Visualize patterns and trends in AI behavior
        """
        
    def create_dashboard_tab(self):
        """Create the main dashboard tab."""
        with gr.Column() as dashboard:
            gr.Markdown("# 🏠 Dashboard")
            gr.Markdown("Welcome to the AI Reflection Agent WebUI. Get started by selecting a tab above.")
            
            # Quick Stats Section
            with gr.Group():
                gr.Markdown("## Quick Stats")
                
                with gr.Row():
                    total_experiments = gr.Number(
                        label="Total Experiments",
                        value=47,
                        interactive=False
                    )
                    active_sessions = gr.Number(
                        label="Active Sessions", 
                        value=session_manager.get_session_count(),
                        interactive=False
                    )
                    success_rate = gr.Number(
                        label="Success Rate (%)",
                        value=89.4,
                        interactive=False
                    )
            
            # Recent Activity Section
            with gr.Group():
                gr.Markdown("## Recent Activity")
                
                recent_activity = gr.Dataframe(
                    headers=["Time", "Activity", "Model", "Status"],
                    value=[
                        ["10:30", "Consciousness Experiment", "qwen3", "✅ Completed"],
                        ["10:15", "Single Response", "claude-3", "✅ Completed"], 
                        ["09:45", "Comparison Analysis", "gpt-4 vs qwen3", "✅ Completed"],
                        ["09:30", "Log Export", "All Models", "✅ Completed"],
                        ["09:15", "Consciousness Experiment", "qwen3", "❌ Failed at Level 3"]
                    ],
                    label="Recent Activities",
                    interactive=False
                )
            
            # Quick Actions Section
            with gr.Group():
                gr.Markdown("## Quick Actions")
                
                with gr.Row():
                    quick_consciousness_btn = gr.Button(
                        "🧠 Start Consciousness Experiment",
                        variant="primary",
                        size="lg"
                    )
                    quick_browse_btn = gr.Button(
                        "📋 Browse Logs", 
                        variant="secondary",
                        size="lg"
                    )
                    quick_compare_btn = gr.Button(
                        "⚖️ Compare Responses",
                        variant="secondary", 
                        size="lg"
                    )
                
                gr.Markdown("💡 **Tip**: Example experiments and test data available in `experiments/` directory")
            
            # System Status Section
            with gr.Group():
                gr.Markdown("## System Status")
                
                with gr.Row():
                    backend_status = gr.Textbox(
                        label="Backend Status",
                        value="🟢 LM Studio Connected (qwen3)",
                        interactive=False
                    )
                    storage_status = gr.Textbox(
                        label="Storage Status",
                        value="🟢 JSONL Logging Active",
                        interactive=False
                    )
                
                system_info = gr.Textbox(
                    label="System Information",
                    value="AI Reflection Agent v1.0.0 • Python 3.11 • Gradio WebUI",
                    interactive=False
                )
        
        return dashboard
    
    def create_app(self):
        """Create the main Gradio application."""
        
        # Custom CSS for better styling
        custom_css = """
        .gradio-container {
            max-width: 1400px !important;
        }
        .tab-nav {
            border-bottom: 2px solid #e0e0e0;
        }
        .tab-nav button {
            font-weight: 500;
            padding: 12px 24px;
        }
        .tab-nav button.selected {
            border-bottom: 3px solid #2196F3;
            color: #2196F3;
        }
        """
        
        with gr.Blocks(
            title=self.title,
            theme=gr.themes.Soft(),
            css=custom_css
        ) as app:
            
            # Header
            gr.Markdown(f"# {self.title}")
            gr.Markdown(self.description)
            
            # Main Tabs
            with gr.Tabs() as tabs:
                
                # Dashboard Tab
                with gr.Tab("🏠 Dashboard", id="dashboard"):
                    self.create_dashboard_tab()
                
                # Consciousness Experiment Tab
                with gr.Tab("🧠 Consciousness Experiment", id="consciousness"):
                    consciousness_experiment_component.create_interface()
                
                # Log Browser Tab
                with gr.Tab("📋 Log Browser", id="logs"):
                    log_browser_component.create_interface()
                
                # Comparison Tab
                with gr.Tab("⚖️ Response Comparison", id="comparison"):
                    comparison_component.create_interface()
                
                # Visualization Tab  
                with gr.Tab("📊 Data Visualization", id="visualization"):
                    visualization_component.create_interface()
                
                # Settings Tab
                with gr.Tab("⚙️ Settings", id="settings"):
                    self.create_settings_tab()
            
            # Footer
            gr.Markdown("""
            ---
            **AI Reflection Agent WebUI** | Built with [Gradio](https://gradio.app) | 
            [Documentation](docs/) | [GitHub](https://github.com/your-repo/ai_reflection_agent)
            """)
        
        return app
    
    def create_settings_tab(self):
        """Create the settings tab."""
        with gr.Column() as settings:
            gr.Markdown("# ⚙️ Settings")
            gr.Markdown("Configure the AI Reflection Agent WebUI settings.")
            
            # Default Backend Settings
            with gr.Group():
                gr.Markdown("## Default Backend Configuration")
                
                with gr.Row():
                    default_backend = gr.Dropdown(
                        choices=["lmstudio", "claude", "openai", "local", "mock"],
                        label="Default Backend",
                        value="lmstudio"
                    )
                    default_model = gr.Textbox(
                        label="Default Model",
                        value="qwen3"
                    )
                
                with gr.Row():
                    default_endpoint = gr.Textbox(
                        label="Default Endpoint",
                        value="http://localhost:1234"
                    )
                    thinking_model_default = gr.Checkbox(
                        label="Default to Thinking Model",
                        value=True
                    )
            
            # WebUI Settings
            with gr.Group():
                gr.Markdown("## WebUI Settings")
                
                with gr.Row():
                    theme_setting = gr.Dropdown(
                        choices=["Soft", "Default", "Monochrome", "Glass"],
                        label="Theme",
                        value="Soft"
                    )
                    max_entries_display = gr.Number(
                        label="Max Entries to Display",
                        value=50,
                        minimum=10,
                        maximum=500
                    )
                
                auto_refresh = gr.Checkbox(
                    label="Auto-refresh Dashboard",
                    value=True
                )
            
            # Logging Settings
            with gr.Group():
                gr.Markdown("## Logging Settings")
                
                with gr.Row():
                    log_directory = gr.Textbox(
                        label="Log Directory",
                        value="./logs",
                        placeholder="Path to log files directory"
                    )
                    log_format = gr.Dropdown(
                        choices=["JSONL", "JSON", "CSV"],
                        label="Log Format",
                        value="JSONL"
                    )
                
                with gr.Row():
                    auto_backup = gr.Checkbox(
                        label="Auto Backup Logs",
                        value=True
                    )
                    backup_frequency = gr.Dropdown(
                        choices=["Daily", "Weekly", "Monthly"],
                        label="Backup Frequency",
                        value="Weekly"
                    )
            
            # Export Settings
            with gr.Group():
                gr.Markdown("## Export Settings")
                
                with gr.Row():
                    default_export_format = gr.Dropdown(
                        choices=["JSON", "CSV", "Markdown", "HTML"],
                        label="Default Export Format",
                        value="JSON"
                    )
                    include_thinking = gr.Checkbox(
                        label="Include Thinking Process in Exports",
                        value=True
                    )
                
                export_directory = gr.Textbox(
                    label="Export Directory",
                    value="./exports",
                    placeholder="Path for exported files"
                )
            
            # Actions
            with gr.Group():
                gr.Markdown("## Actions")
                
                with gr.Row():
                    save_settings_btn = gr.Button("Save Settings", variant="primary")
                    reset_settings_btn = gr.Button("Reset to Defaults")
                    export_config_btn = gr.Button("Export Configuration")
                
                settings_status = gr.Textbox(
                    label="Status",
                    value="Settings loaded",
                    interactive=False
                )
        
        return settings
    
    def launch(self, **kwargs):
        """Launch the WebUI application."""
        app = self.create_app()
        
        # Default launch parameters
        launch_params = {
            "server_name": "127.0.0.1",
            "server_port": 7860,
            "share": False,
            "debug": False,
            "show_error": True,
            "quiet": False,
            **kwargs
        }
        
        print(f"🚀 Launching AI Reflection Agent WebUI...")
        print(f"📍 URL: http://{launch_params['server_name']}:{launch_params['server_port']}")
        print(f"🔧 Debug mode: {launch_params['debug']}")
        
        app.launch(**launch_params)


def main():
    """Main entry point for the WebUI."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Reflection Agent WebUI")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=7860, help="Port to bind to")
    parser.add_argument("--share", action="store_true", help="Create public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Create and launch the WebUI
    webui = AIReflectionWebUI()
    webui.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        debug=args.debug
    )


if __name__ == "__main__":
    main()