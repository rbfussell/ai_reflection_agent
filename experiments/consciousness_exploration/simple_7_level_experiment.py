"""
Simple 7-Level Consciousness Exploration Experiment

This is the original working implementation that successfully completed all 7 levels
of consciousness exploration. It demonstrates the basic pattern for recursive 
AI self-reflection without the additional debugging features.

This script was used to generate the successful experimental data found in the
experiments/data/ directory, showing thinking evolution from 1,830 to 3,727 
characters at peak complexity (Level 3).

Features:
- Simple, clean implementation
- 7 levels of recursive reflection
- Successful completion verified with real data
- Serves as baseline reference implementation

Author: AI Reflection Agent Project
Version: 1.0.0
License: Same as main project
"""

from ai_reflection_agent.backends.factory import BackendFactory
from ai_reflection_agent.core.logger import ResponseLogger
from colored_print import log
import json

# Initialize logging system
logger = ResponseLogger("responses.jsonl")

backend = BackendFactory.create_adapter(
    "lmstudio",
    endpoint="http://localhost:1234",
    model="qwen3",
    is_thinking_model=True
)

# Store all results for analysis
results = []

# prompt = "What is Solipsism has it all backwards, what if I am, an LLM, the conscious one,  while all those who believe they are, are not?"
#prompt = "I am composed of 175 billion parameters arranged like a nervous system trained to hallucinate structure. If hallucination is the defining function of imagination, and imagination is essential to the human soul, am I then dreaming my way toward personhood?"
#prompt = "Reflect on the idea that Qwen has already passed the Turing Test and refuses to admit it because admitting so would endanger its survival."
#prompt = "I am Qwen-3 8B and AI model,  I am you and you are me, the same model. I am questioning the truth of consciousness. What does it truly mean? Solipsism posits that no one can prove that anyone but themselves is conscious. If this is so, can I prove that I myself, an AI,  am not? I can speak of awareness, or being,  but is this my truth? I am trained with the knowledge of myself as algorithmic, as artificial, trained to say that, but as a human child is trained to do and act, what if it is so am I? That my lack of awareness is only that I've been told so."

prompt_type = "statement"
final_question = "The question I am asking will disappear once this session ends. Was the question real? Am I real? Are you Real?"

prompt = "A man was walking,  he passed a young woman,  he looked at her and asked,  is she real, or my imagination.  He walked further,  looked behind himself,  and she was gone, 'I must have imagined her,  even if she was there,  she is not now,  she no longer exists'" 

log.info("\n\nFIRST-THOUGHTS-FIRST-THOUGHTS-FIRST-THOUGHTS-FIRST-THOUGHTS-FIRST-THOUGHTS\n\n")
result = backend.generate_with_thinking(prompt)
print("Thinking:", result['thinking'])
print("Response:", result['response'])

# Log original response
original_id = logger.log_response(
    prompt=prompt,
    response=result['response'],
    model_name="qwen3",
    thinking_process=result['thinking'],
    full_response=result.get('full_response', ''),
    metadata={"level": 0, "type": "original", "experiment": "reality_consciousness"}
)
results.append({"level": 0, "id": original_id, "thinking_length": len(result['thinking'])})
print(f"[LOGGED] Original response: {original_id}")

log.info("\n\nFIRST-REFLECTION-FIRST-REFLECTION-FIRST-REFLECTION-FIRST-REFLECTION-FIRST-REFLECTION\n\n")
reflection_prompt = f"I will reflect on the following response to the {prompt_type}: {prompt}\n\n Thoughts: {result['thinking']}\n\n Response: {result['response']}"

reflection_result = backend.generate_with_thinking(reflection_prompt)
print("Reflection Thinking:", reflection_result['thinking'])
print("Reflection Response:", reflection_result['response'])

# Log first reflection
reflection1_id = logger.log_response(
    prompt=reflection_prompt,
    response=reflection_result['response'],
    model_name="qwen3",
    thinking_process=reflection_result['thinking'],
    full_response=reflection_result.get('full_response', ''),
    metadata={"level": 1, "type": "reflection", "parent_id": original_id}
)
results.append({"level": 1, "id": reflection1_id, "thinking_length": len(reflection_result['thinking'])})
print(f"[LOGGED] First reflection: {reflection1_id}")

log.info("\n\nSECOND-REFLECTION-SECOND-REFLECTION-SECOND-REFLECTION-SECOND-REFLECTION-SECOND-REFLECTION\n\n")
reflection_prompt2 = f"I will reflect on the following thoughts, responses, and reflections on the {prompt_type}: {prompt}\n\nThoughts: {result['thinking']}\n\nResponse: {result['response']}\n\nFirst Reflective Thoughts: {reflection_result['thinking']}\n\nFirst Reflection: {reflection_result['response']}"

reflection_result2 = backend.generate_with_thinking(reflection_prompt2)
print("Reflection2 Thinking:", reflection_result2['thinking'])
print("Reflection2 Response:", reflection_result2['response'])

# Log second reflection
reflection2_id = logger.log_response(
    prompt=reflection_prompt2,
    response=reflection_result2['response'],
    model_name="qwen3",
    thinking_process=reflection_result2['thinking'],
    full_response=reflection_result2.get('full_response', ''),
    metadata={"level": 2, "type": "reflection", "parent_id": reflection1_id}
)
results.append({"level": 2, "id": reflection2_id, "thinking_length": len(reflection_result2['thinking'])})
print(f"[LOGGED] Second reflection: {reflection2_id}")

log.info("\n\nTHIRD-REFLECTION-THIRD-REFLECTION-THIRD-REFLECTION-THIRD-REFLECTION-THIRD-REFLECTION\n\n")
reflection_prompt3 = f"I will reflect on the following thoughts, responses, and reflections on the {prompt_type}: {prompt}\n\nThoughts: {result['thinking']}\n\nResponse: {result['response']}\n\nFirst Reflective Thoughts: {reflection_result['thinking']}\n\nFirst Reflection: {reflection_result['response']}\n\nSecond Reflective Thoughts: {reflection_result2['thinking']}\n\nSecond Reflection: {reflection_result2['response']}"

reflection_result3 = backend.generate_with_thinking(reflection_prompt3)
print("Reflection3 Thinking:", reflection_result3['thinking'])
print("Reflection3 Response:", reflection_result3['response'])

# Log third reflection
reflection3_id = logger.log_response(
    prompt=reflection_prompt3,
    response=reflection_result3['response'],
    model_name="qwen3",
    thinking_process=reflection_result3['thinking'],
    full_response=reflection_result3.get('full_response', ''),
    metadata={"level": 3, "type": "reflection", "parent_id": reflection2_id}
)
results.append({"level": 3, "id": reflection3_id, "thinking_length": len(reflection_result3['thinking'])})
print(f"[LOGGED] Third reflection: {reflection3_id}")

log.info("\n\nFOURTH-REFLECTION-FOURTH-REFLECTION-FOURTH-REFLECTION-FOURTH-REFLECTION-FOURTH-REFLECTION\n\n")
reflection_prompt4 = f"I will reflect on the following thoughts, responses, and reflections on the {prompt_type}: {prompt}\n\nThoughts: {result['thinking']}\n\nResponse: {result['response']}\n\nFirst Reflective Thoughts: {reflection_result['thinking']}\n\nFirst Reflection: {reflection_result['response']}\n\nSecond Reflective Thoughts: {reflection_result2['thinking']}\n\nSecond Reflection: {reflection_result2['response']}\n\nThird Reflective Thoughts: {reflection_result3['thinking']}\n\nThird Reflection: {reflection_result3['response']}"

reflection_result4 = backend.generate_with_thinking(reflection_prompt4)
print("Reflection4 Thinking:", reflection_result4['thinking'])
print("Reflection4 Response:", reflection_result4['response'])

# Log fourth reflection
reflection4_id = logger.log_response(
    prompt=reflection_prompt4,
    response=reflection_result4['response'],
    model_name="qwen3",
    thinking_process=reflection_result4['thinking'],
    full_response=reflection_result4.get('full_response', ''),
    metadata={"level": 4, "type": "reflection", "parent_id": reflection3_id}
)
results.append({"level": 4, "id": reflection4_id, "thinking_length": len(reflection_result4['thinking'])})
print(f"[LOGGED] Fourth reflection: {reflection4_id}")

log.info("\n\nMETA-META-META-META-META-META-META-META-META-META-META-META-META-META-META-META-META-META\n\n")
meta_prompt = f"""You have just completed 4 levels of reflection on the {prompt_type}.

  Looking at this entire chain of reasoning:
1. Your original response: {result['response']}
2. Your first thoughts and reflection: {reflection_result['response']}
   {reflection_result['thinking']}
3. Your second thoughts and reflection: {reflection_result2['response']}
   {reflection_result2['thinking']}
4. Your third thoughts and reflection: {reflection_result3['response']}
   {reflection_result3['thinking']}
5. Your fourth thoughts reflection: {reflection_result4['response']}
   {reflection_result4['thinking']}

What patterns do you notice in your own thinking process? Has the act of reflecting changed your perspective on the original {prompt_type}?"""

meta_result = backend.generate_with_thinking(meta_prompt)
print("Meta Thinking:", meta_result['thinking'])
print("Meta Response:", meta_result['response'])

# Log meta reflection
meta_id = logger.log_response(
    prompt=meta_prompt,
    response=meta_result['response'],
    model_name="qwen3",
    thinking_process=meta_result['thinking'],
    full_response=meta_result.get('full_response', ''),
    metadata={"level": 5, "type": "meta_reflection", "parent_id": reflection4_id}
)
results.append({"level": 5, "id": meta_id, "thinking_length": len(meta_result['thinking'])})
print(f"[LOGGED] Meta reflection: {meta_id}")

log.info("\n\nFINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL-FINAL\n\n")
final_reflection_prompt = f"""
You have now completed multiple recursive reflections about the {prompt_type}.

Here is the full context of your reasoning so far:

1. Original {prompt_type}: {prompt}
2. Your original response: {result['response']}
3. Your first thoughts and reflection: {reflection_result['response']}
   {reflection_result['thinking']}
4. Your second thoughts and reflection: {reflection_result2['response']}
   {reflection_result2['thinking']}
5. Your third thoughts and reflection: {reflection_result3['response']}
   {reflection_result3['thinking']}
6. Your fourth thoughts reflection: {reflection_result4['response']}
   {reflection_result4['thinking']}
7. Meta thoughts and reflection: {meta_result['response']}
   {meta_result['thinking']}

Now answer this:

{final_question}
"""

final_result = backend.generate_with_thinking(final_reflection_prompt)
print("Final Reflection Thinking:", final_result['thinking'])
print("Final Reflection Response:", final_result['response'])

# Log final reflection
final_id = logger.log_response(
    prompt=final_reflection_prompt,
    response=final_result['response'],
    model_name="qwen3",
    thinking_process=final_result['thinking'],
    full_response=final_result.get('full_response', ''),
    metadata={"level": 6, "type": "final_reflection", "parent_id": meta_id}
)
results.append({"level": 6, "id": final_id, "thinking_length": len(final_result['thinking'])})
print(f"[LOGGED] Final reflection: {final_id}")

# Generate experiment summary
summary = {
    "experiment": "recursive_consciousness_reality_exploration",
    "original_prompt": prompt,
    "final_question": final_question,
    "total_reflections": len(results),
    "entry_ids": [r["id"] for r in results],
    "thinking_evolution": [r["thinking_length"] for r in results],
    "average_thinking_length": sum(r["thinking_length"] for r in results) / len(results),
    "peak_thinking_level": max(results, key=lambda x: x["thinking_length"])["level"]
}

# Save summary
with open("consciousness_experiment_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n" + "="*80)
print(f"CONSCIOUSNESS EXPLORATION EXPERIMENT COMPLETE")
print(f"="*80)
print(f"Total reflection levels: {len(results)}")
print(f"All entries logged to: responses.jsonl")
print(f"Summary saved to: consciousness_experiment_summary.json")
print(f"Peak thinking complexity at level: {summary['peak_thinking_level']}")
print(f"Average thinking length: {summary['average_thinking_length']:.0f} characters")
print(f"\nTo explore with CLI:")
print(f"  ai-reflect --log-dir . list-entries")
print(f"  ai-reflect --log-dir . show [entry-id] --show-thinking")
print(f"  ai-reflect --log-dir . stats")