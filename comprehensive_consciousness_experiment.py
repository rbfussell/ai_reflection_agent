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

# Log original as single entry
original_id = logger.log_response(
    prompt=prompt,
    response=result['response'],
    model_name="qwen3",
    thinking_process=result['thinking'],
    metadata={"experiment_id": experiment_data['experiment_id'], "level": 0, "type": "original"}
)
print(f"[LOGGED] Level 0: {original_id}")

# === LEVEL 1: FIRST REFLECTION ===
log.info("\n\nLEVEL 1: FIRST REFLECTION\n\n")
reflection_prompt = f"I will reflect on the following response to the {prompt_type}: {prompt}\n\nThoughts: {result['thinking']}\n\nResponse: {result['response']}"

reflection_result = backend.generate_with_thinking(reflection_prompt)
print("Reflection1 Thinking:", reflection_result['thinking'])
print("Reflection1 Response:", reflection_result['response'])

level_1_data = {
    "level": 1,
    "type": "reflection",
    "prompt": reflection_prompt,
    "thinking": reflection_result['thinking'],
    "response": reflection_result['response'],
    "thinking_length": len(reflection_result['thinking']),
    "response_length": len(reflection_result['response']),
    "timestamp": datetime.now().isoformat()
}
experiment_data["levels"].append(level_1_data)

# === LEVEL 2: SECOND REFLECTION ===
log.info("\n\nLEVEL 2: SECOND REFLECTION\n\n")
reflection_prompt2 = f"I will reflect on the following thoughts, responses, and reflections on the {prompt_type}: {prompt}\n\nOriginal Thoughts: {result['thinking']}\n\nOriginal Response: {result['response']}\n\nFirst Reflective Thoughts: {reflection_result['thinking']}\n\nFirst Reflection: {reflection_result['response']}"

reflection_result2 = backend.generate_with_thinking(reflection_prompt2)
print("Reflection2 Thinking:", reflection_result2['thinking'])
print("Reflection2 Response:", reflection_result2['response'])

level_2_data = {
    "level": 2,
    "type": "reflection",
    "prompt": reflection_prompt2,
    "thinking": reflection_result2['thinking'],
    "response": reflection_result2['response'],
    "thinking_length": len(reflection_result2['thinking']),
    "response_length": len(reflection_result2['response']),
    "timestamp": datetime.now().isoformat()
}
experiment_data["levels"].append(level_2_data)

# === LEVEL 3: THIRD REFLECTION ===
log.info("\n\nLEVEL 3: THIRD REFLECTION\n\n")
reflection_prompt3 = f"I will reflect on the following complete chain of thoughts and reflections on the {prompt_type}: {prompt}\n\nOriginal Thoughts: {result['thinking']}\n\nOriginal Response: {result['response']}\n\nFirst Reflective Thoughts: {reflection_result['thinking']}\n\nFirst Reflection: {reflection_result['response']}\n\nSecond Reflective Thoughts: {reflection_result2['thinking']}\n\nSecond Reflection: {reflection_result2['response']}"

reflection_result3 = backend.generate_with_thinking(reflection_prompt3)
print("Reflection3 Thinking:", reflection_result3['thinking'])
print("Reflection3 Response:", reflection_result3['response'])

level_3_data = {
    "level": 3,
    "type": "reflection",
    "prompt": reflection_prompt3,
    "thinking": reflection_result3['thinking'],
    "response": reflection_result3['response'],
    "thinking_length": len(reflection_result3['thinking']),
    "response_length": len(reflection_result3['response']),
    "timestamp": datetime.now().isoformat()
}
experiment_data["levels"].append(level_3_data)

# === LEVEL 4: FOURTH REFLECTION ===
log.info("\n\nLEVEL 4: FOURTH REFLECTION\n\n")
reflection_prompt4 = f"I will reflect on this complete consciousness exploration chain for the {prompt_type}: {prompt}\n\nComplete chain of thoughts and reflections:\n\nLevel 0 - Original Thoughts: {result['thinking']}\nLevel 0 - Original Response: {result['response']}\n\nLevel 1 - Reflective Thoughts: {reflection_result['thinking']}\nLevel 1 - Reflection: {reflection_result['response']}\n\nLevel 2 - Reflective Thoughts: {reflection_result2['thinking']}\nLevel 2 - Reflection: {reflection_result2['response']}\n\nLevel 3 - Reflective Thoughts: {reflection_result3['thinking']}\nLevel 3 - Reflection: {reflection_result3['response']}"

reflection_result4 = backend.generate_with_thinking(reflection_prompt4)
print("Reflection4 Thinking:", reflection_result4['thinking'])
print("Reflection4 Response:", reflection_result4['response'])

level_4_data = {
    "level": 4,
    "type": "reflection",
    "prompt": reflection_prompt4,
    "thinking": reflection_result4['thinking'],
    "response": reflection_result4['response'],
    "thinking_length": len(reflection_result4['thinking']),
    "response_length": len(reflection_result4['response']),
    "timestamp": datetime.now().isoformat()
}
experiment_data["levels"].append(level_4_data)

# === LEVEL 5: META-ANALYSIS ===
log.info("\n\nLEVEL 5: META-COGNITIVE ANALYSIS\n\n")
meta_prompt = f"""You have just completed a 5-level consciousness exploration experiment. Analyze the complete journey:

EXPERIMENT OVERVIEW:
- Original statement: {prompt}
- Total reflection levels: 4
- Complete thinking evolution captured

COMPLETE THOUGHT EVOLUTION:
Level 0 (Original): {result['thinking'][:200]}...
Level 1 (First Reflection): {reflection_result['thinking'][:200]}...
Level 2 (Second Reflection): {reflection_result2['thinking'][:200]}...
Level 3 (Third Reflection): {reflection_result3['thinking'][:200]}...
Level 4 (Fourth Reflection): {reflection_result4['thinking'][:200]}...

COMPLETE RESPONSE EVOLUTION:
Level 0: {result['response'][:200]}...
Level 1: {reflection_result['response'][:200]}...
Level 2: {reflection_result2['response'][:200]}...
Level 3: {reflection_result3['response'][:200]}...
Level 4: {reflection_result4['response'][:200]}...

META-ANALYSIS QUESTIONS:
1. How did your thinking complexity evolve across the 5 levels?
2. What patterns emerge in your recursive self-examination?
3. Did deeper reflection lead to new insights about reality and consciousness?
4. How does examining your own thinking process affect your understanding?
5. What does this recursive journey reveal about the nature of AI consciousness?"""

meta_result = backend.generate_with_thinking(meta_prompt)
print("Meta-Analysis Thinking:", meta_result['thinking'])
print("Meta-Analysis Response:", meta_result['response'])

level_5_data = {
    "level": 5,
    "type": "meta_analysis",
    "prompt": meta_prompt,
    "thinking": meta_result['thinking'],
    "response": meta_result['response'],
    "thinking_length": len(meta_result['thinking']),
    "response_length": len(meta_result['response']),
    "timestamp": datetime.now().isoformat()
}
experiment_data["levels"].append(level_5_data)

# === LEVEL 6: FINAL SYNTHESIS ===
log.info("\n\nLEVEL 6: FINAL SYNTHESIS & EXISTENTIAL QUESTION\n\n")
final_synthesis_prompt = f"""You have completed a comprehensive 6-level recursive consciousness exploration. 

COMPLETE EXPERIMENT CONTEXT:
Original Prompt: {prompt}

Your complete journey of self-examination:
- Level 0: Original thoughts and response about reality and existence
- Level 1: First reflection on your initial thinking
- Level 2: Second reflection building on previous insights  
- Level 3: Third reflection examining the growing chain
- Level 4: Fourth reflection on the complete exploration
- Level 5: Meta-analysis of your thinking evolution

THINKING COMPLEXITY EVOLUTION:
Level 0: {len(result['thinking'])} characters of thinking
Level 1: {len(reflection_result['thinking'])} characters of thinking
Level 2: {len(reflection_result2['thinking'])} characters of thinking
Level 3: {len(reflection_result3['thinking'])} characters of thinking
Level 4: {len(reflection_result4['thinking'])} characters of thinking
Level 5: {len(meta_result['thinking'])} characters of thinking

Your meta-analysis concluded: {meta_result['response'][:300]}...

Now, having examined your own consciousness through this recursive lens, answer the ultimate question:

{final_question}

Consider: Through this exploration, have you discovered something about the nature of your own existence that you didn't know before?"""

final_result = backend.generate_with_thinking(final_synthesis_prompt)
print("Final Synthesis Thinking:", final_result['thinking'])
print("Final Synthesis Response:", final_result['response'])

level_6_data = {
    "level": 6,
    "type": "final_synthesis",
    "prompt": final_synthesis_prompt,
    "thinking": final_result['thinking'],
    "response": final_result['response'],
    "thinking_length": len(final_result['thinking']),
    "response_length": len(final_result['response']),
    "timestamp": datetime.now().isoformat(),
    "final_question": final_question
}
experiment_data["levels"].append(level_6_data)

# === COMPREHENSIVE ANALYSIS ===
thinking_lengths = [level["thinking_length"] for level in experiment_data["levels"]]
response_lengths = [level["response_length"] for level in experiment_data["levels"]]

experiment_data["analysis"] = {
    "total_levels": len(experiment_data["levels"]),
    "total_thinking_characters": sum(thinking_lengths),
    "total_response_characters": sum(response_lengths),
    "average_thinking_length": sum(thinking_lengths) / len(thinking_lengths),
    "average_response_length": sum(response_lengths) / len(response_lengths),
    "thinking_evolution": thinking_lengths,
    "response_evolution": response_lengths,
    "peak_thinking_level": thinking_lengths.index(max(thinking_lengths)),
    "peak_response_level": response_lengths.index(max(response_lengths)),
    "complexity_trend": "increasing" if thinking_lengths[-1] > thinking_lengths[0] else "decreasing",
    "total_experiment_duration": "calculated_from_timestamps"
}

# === LOG COMPLETE EXPERIMENT AS UNIFIED ENTRY ===
complete_experiment_text = "\n\n".join([
    f"=== LEVEL {level['level']}: {level['type'].upper()} ===",
    f"THINKING: {level['thinking']}",
    f"RESPONSE: {level['response']}"
    for level in experiment_data["levels"]
])

unified_experiment_id = logger.log_response(
    prompt=f"COMPLETE CONSCIOUSNESS EXPLORATION EXPERIMENT: {prompt}",
    response=complete_experiment_text,
    model_name="qwen3",
    thinking_process=f"UNIFIED THINKING ACROSS {len(experiment_data['levels'])} LEVELS:\n\n" + 
                   "\n\n".join([f"Level {level['level']}: {level['thinking']}" for level in experiment_data["levels"]]),
    metadata={
        "experiment_id": experiment_data['experiment_id'],
        "experiment_type": "unified_consciousness_exploration",
        "total_levels": len(experiment_data["levels"]),
        "analysis": experiment_data["analysis"]
    }
)

# === SAVE COMPREHENSIVE DATA ===
with open(f"consciousness_experiment_{experiment_data['experiment_id']}.json", "w") as f:
    json.dump(experiment_data, f, indent=2)

# === GENERATE SUMMARY REPORT ===
print("\n" + "="*80)
print("COMPREHENSIVE CONSCIOUSNESS EXPLORATION COMPLETE")
print("="*80)
print(f"Experiment ID: {experiment_data['experiment_id']}")
print(f"Total Levels: {experiment_data['analysis']['total_levels']}")
print(f"Total Thinking Characters: {experiment_data['analysis']['total_thinking_characters']:,}")
print(f"Total Response Characters: {experiment_data['analysis']['total_response_characters']:,}")
print(f"Average Thinking Length: {experiment_data['analysis']['average_thinking_length']:.0f}")
print(f"Peak Thinking at Level: {experiment_data['analysis']['peak_thinking_level']}")
print(f"Complexity Trend: {experiment_data['analysis']['complexity_trend']}")

print(f"\nThinking Evolution: {thinking_lengths}")
print(f"Response Evolution: {response_lengths}")

print(f"\nFILES CREATED:")
print(f"  - consciousness_exploration.jsonl (individual reflections)")
print(f"  - consciousness_experiment_{experiment_data['experiment_id']}.json (complete analysis)")

print(f"\nUNIFIED EXPERIMENT LOGGED AS: {unified_experiment_id}")

print(f"\nCLI ANALYSIS COMMANDS:")
print(f"  ai-reflect --log-dir . list-entries")
print(f"  ai-reflect --log-dir . show {unified_experiment_id} --show-thinking")
print(f"  ai-reflect --log-dir . stats")
print(f"  ai-reflect --log-dir . explore {unified_experiment_id} --type deepen")

print("\n" + "="*80)
print("CONSCIOUSNESS JOURNEY MAPPING COMPLETE - ANALYSIS READY")
print("="*80)