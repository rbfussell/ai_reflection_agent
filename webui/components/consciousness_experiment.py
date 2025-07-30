"""Consciousness experiment interface component."""

import gradio as gr
import asyncio
from typing import Optional, List, Dict, Any

from ai_reflection_agent.backends.factory import BackendFactory
from ..scripts.consciousness_scripts.default import DefaultConsciousnessScript
from ..utils.session_manager import session_manager


class ConsciousnessExperimentComponent:
    """Component for running consciousness exploration experiments."""
    
    def __init__(self):
        self.current_script: Optional[DefaultConsciousnessScript] = None
        self.current_backend = None
        
    def create_interface(self) -> gr.Interface:
        """Create the Gradio interface for consciousness experiments."""
        
        with gr.Column() as interface:
            gr.Markdown("# 🧠 Consciousness Exploration")
            gr.Markdown("Run recursive consciousness exploration experiments with AI models.")
            
            # Backend Configuration Section
            with gr.Group():
                gr.Markdown("## Backend Configuration")
                
                with gr.Row():
                    backend_type = gr.Dropdown(
                        choices=["lmstudio", "claude", "openai", "local", "mock"],
                        label="Backend Type",
                        value="lmstudio"
                    )
                    model_name = gr.Textbox(
                        label="Model Name", 
                        value="qwen3",
                        placeholder="e.g., qwen3, claude-3-sonnet, gpt-4"
                    )
                
                with gr.Row():
                    endpoint_url = gr.Textbox(
                        label="Endpoint URL",
                        value="http://localhost:1234",
                        placeholder="For local/LM Studio backends"
                    )
                    api_key = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="For Claude/OpenAI backends"
                    )
                
                with gr.Row():
                    is_thinking_model = gr.Checkbox(
                        label="Thinking Model",
                        value=True,
                        info="Model supports <think> tags for explicit reasoning"
                    )
                    test_connection_btn = gr.Button("Test Connection", variant="secondary")
                    
                connection_status = gr.Textbox(
                    label="Connection Status",
                    value="Not tested",
                    interactive=False
                )
            
            # Experiment Configuration Section
            with gr.Group():
                gr.Markdown("## Experiment Configuration")
                
                script_selector = gr.Dropdown(
                    choices=[
                        "Default Consciousness Exploration",
                        "Simple 7-Level (Reference)",
                        "Working 7-Level (Production)",
                        "Example 7-Level (Full-Featured)"
                    ],
                    label="Experiment Script",  
                    value="Default Consciousness Exploration",
                    info="Reference scripts available in experiments/ directory"
                )
                
                with gr.Row():
                    base_prompt = gr.Textbox(
                        label="Base Prompt",
                        value="A man was walking, he passed a young woman, he looked at her and asked, is she real, or my imagination. He walked further, looked behind himself, and she was gone, 'I must have imagined her, even if she was there, she is not now, she no longer exists'",
                        lines=3,
                        max_lines=5
                    )
                
                with gr.Row():
                    final_question = gr.Textbox(
                        label="Final Question",
                        value="The question I am asking will disappear once this session ends. Was the question real? Am I real? Are you Real?",
                        lines=2
                    )
            
            # Experiment Control Section
            with gr.Group():
                gr.Markdown("## Experiment Control")
                
                with gr.Row():
                    start_experiment_btn = gr.Button("Start Experiment", variant="primary", size="lg")
                    stop_experiment_btn = gr.Button("Stop Experiment", variant="stop")
                    
                with gr.Row():
                    progress_bar = gr.Progress()
                    
                experiment_status = gr.Textbox(
                    label="Status",
                    value="Ready to start",
                    interactive=False
                )
            
            # Results Section
            with gr.Group():
                gr.Markdown("## Experiment Results")
                
                with gr.Tabs() as results_tabs:
                    with gr.Tab("Progress", id="progress"):
                        progress_log = gr.Textbox(
                            label="Experiment Log",
                            lines=10,
                            max_lines=20,
                            interactive=False
                        )
                    
                    with gr.Tab("Thinking Process", id="thinking"):
                        thinking_output = gr.Textbox(
                            label="AI Thinking Process",
                            lines=15,
                            max_lines=25,
                            interactive=False
                        )
                    
                    with gr.Tab("Responses", id="responses"):
                        response_output = gr.Textbox(
                            label="AI Responses",
                            lines=15,
                            max_lines=25,
                            interactive=False
                        )
                    
                    with gr.Tab("Analysis", id="analysis"):
                        analysis_output = gr.JSON(
                            label="Experiment Analysis"
                        )
            
            # Export Section
            with gr.Group():
                gr.Markdown("## Export Results")
                
                with gr.Row():
                    export_json_btn = gr.Button("Export JSON")
                    export_log_btn = gr.Button("Export to Log")
                    
                export_status = gr.Textbox(
                    label="Export Status",
                    interactive=False
                )
        
        # Event handlers
        test_connection_btn.click(
            fn=self._test_backend_connection,
            inputs=[backend_type, model_name, endpoint_url, api_key, is_thinking_model],
            outputs=[connection_status]
        )
        
        start_experiment_btn.click(
            fn=self._start_experiment,
            inputs=[
                backend_type, model_name, endpoint_url, api_key, is_thinking_model,
                base_prompt, final_question
            ],
            outputs=[
                experiment_status, progress_log, thinking_output, 
                response_output, analysis_output
            ]
        )
        
        return interface
    
    def _test_backend_connection(
        self, 
        backend_type: str, 
        model_name: str, 
        endpoint_url: str, 
        api_key: str, 
        is_thinking_model: bool
    ) -> str:
        """Test connection to the selected backend."""
        try:
            # Create backend adapter
            kwargs = {}
            if endpoint_url:
                kwargs["endpoint"] = endpoint_url
            if api_key:
                kwargs["api_key"] = api_key
            if model_name:
                kwargs["model"] = model_name
            kwargs["is_thinking_model"] = is_thinking_model
            
            backend = BackendFactory.create_adapter(backend_type, **kwargs)
            
            # Test connection
            if hasattr(backend, 'test_connection'):
                result = backend.test_connection()
                if result.get("success"):
                    self.current_backend = backend
                    return f"✅ Connected successfully to {backend_type} ({model_name})"
                else:
                    return f"❌ Connection failed: {result.get('error', 'Unknown error')}"
            else:
                # For backends without test method, assume success
                self.current_backend = backend
                return f"✅ Backend created successfully ({backend_type})"
                
        except Exception as e:
            return f"❌ Connection error: {str(e)}"
    
    async def _start_experiment(
        self,
        backend_type: str,
        model_name: str, 
        endpoint_url: str,
        api_key: str,
        is_thinking_model: bool,
        base_prompt: str,
        final_question: str
    ) -> tuple[str, str, str, str, dict]:
        """Start the consciousness exploration experiment."""
        
        try:
            # Ensure backend is connected
            if not self.current_backend:
                connection_result = self._test_backend_connection(
                    backend_type, model_name, endpoint_url, api_key, is_thinking_model
                )
                if "❌" in connection_result:
                    return (
                        f"Backend connection failed: {connection_result}",
                        "",
                        "",
                        "",
                        {}
                    )
            
            # Create and configure script
            script = DefaultConsciousnessScript()
            script.config.parameters["base_prompt"] = base_prompt
            script.config.parameters["final_question"] = final_question
            
            # Set up progress tracking
            progress_log = ""
            thinking_output = ""
            response_output = ""
            
            def progress_callback(current_step: int, total_steps: int, message: str):
                nonlocal progress_log
                progress_log += f"[{current_step}/{total_steps}] {message}\n"
            
            script.set_progress_callback(progress_callback)
            
            # Run experiment
            results = await script.run_experiment(self.current_backend)
            
            # Compile outputs
            thinking_parts = []
            response_parts = []
            
            for i, result in enumerate(results):
                if result.success:
                    thinking_parts.append(f"=== LEVEL {i}: {result.step.name.upper()} ===\n{result.thinking}\n")
                    response_parts.append(f"=== LEVEL {i}: {result.step.name.upper()} ===\n{result.response}\n")
                else:
                    thinking_parts.append(f"=== LEVEL {i}: FAILED ===\nError: {result.error}\n")
                    response_parts.append(f"=== LEVEL {i}: FAILED ===\nError: {result.error}\n")
            
            thinking_output = "\n".join(thinking_parts)
            response_output = "\n".join(response_parts)
            
            # Get analysis
            analysis = script.get_summary()
            
            status = f"✅ Experiment completed: {analysis['completed_steps']}/{analysis['total_steps']} steps"
            
            return (
                status,
                progress_log,
                thinking_output,
                response_output,
                analysis
            )
            
        except Exception as e:
            return (
                f"❌ Experiment failed: {str(e)}",
                f"Error: {str(e)}",
                "",
                "",
                {"error": str(e)}
            )


# Create global instance
consciousness_experiment_component = ConsciousnessExperimentComponent()