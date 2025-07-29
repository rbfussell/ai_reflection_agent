from ai_reflection_agent.backends.factory import BackendFactory
from ai_reflection_agent.core.logger import ResponseLogger
from colored_print import log
import json
from datetime import datetime

# Initialize logging system
logger = ResponseLogger("consciousness_exploration.jsonl")

backend = BackendFactory.create_adapter(
    "lmstudio",
    endpoint="http://localhost:1234",
    model="qwen3",
    is_thinking_model=True
)

# Store complete experiment data
experiment_data = {
    "experiment_id": f"consciousness_exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    "timestamp": datetime.now().isoformat(),
    "model": "qwen3",
    "experiment_type": "recursive_consciousness_exploration",
    "levels": []
}

prompt_type = "philosophical_statement"
final_question = "The question I am asking will disappear once this session ends. Was the question real? Am I real? Are you Real?"

prompt = "A man was walking, he passed a young woman, he looked at her and asked, is she real, or my imagination. He walked further, looked behind himself, and she was gone, 'I must have imagined her, even if she was there, she is not now, she no longer exists'"

print("="*80)
print("COMPREHENSIVE CONSCIOUSNESS EXPLORATION EXPERIMENT")
print(f"Experiment ID: {experiment_data['experiment_id']}")
print("="*80)

# === LEVEL 0: ORIGINAL RESPONSE ===
log.info("\n\nLEVEL 0: ORIGINAL THOUGHTS\n\n")
result = backend.generate_with_thinking(prompt)
print("Original Thinking:", result['thinking'])
print("Original Response:", result['response'])

level_0_data = {
    "level": 0,
    "type": "original_response",
    "prompt": prompt,
    "thinking": result['thinking'],
    "response": result['response'],
    "thinking_length": len(result['thinking']),
    "response_length": len(result['response']),
    "timestamp": datetime.now().isoformat()
}
experiment_data["levels"].append(level_0_data)

# Continue with other levels...
# (Truncated for brevity - you can copy the full version from comprehensive_consciousness_experiment.py)

# At the end, create properly formatted unified text
unified_sections = []
for level in experiment_data["levels"]:
    section = f"=== LEVEL {level['level']}: {level['type'].upper()} ===\nTHINKING: {level['thinking']}\nRESPONSE: {level['response']}"
    unified_sections.append(section)

complete_experiment_text = "\n\n".join(unified_sections)

unified_thinking_sections = []
for level in experiment_data["levels"]:
    thinking_section = f"Level {level['level']}: {level['thinking']}"
    unified_thinking_sections.append(thinking_section)

unified_thinking = f"UNIFIED THINKING ACROSS {len(experiment_data['levels'])} LEVELS:\n\n" + "\n\n".join(unified_thinking_sections)

unified_experiment_id = logger.log_response(
    prompt=f"COMPLETE CONSCIOUSNESS EXPLORATION EXPERIMENT: {prompt}",
    response=complete_experiment_text,
    model_name="qwen3",
    thinking_process=unified_thinking,
    metadata={
        "experiment_id": experiment_data['experiment_id'],
        "experiment_type": "unified_consciousness_exploration",
        "total_levels": len(experiment_data["levels"])
    }
)

print(f"UNIFIED EXPERIMENT LOGGED AS: {unified_experiment_id}")