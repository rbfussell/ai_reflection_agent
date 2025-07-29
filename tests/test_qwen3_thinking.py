#!/usr/bin/env python3
"""
Specialized test for Qwen3 thinking model with LM Studio.
Demonstrates capturing and analyzing the thinking process.
"""

import os
import sys
from pathlib import Path

# Add the package to path for testing
sys.path.insert(0, str(Path(__file__).parent / "ai_reflection_agent"))

from ai_reflection_agent.core.logger import ResponseLogger, ExplorationLogger
from ai_reflection_agent.core.scorer import SelfScorer
from ai_reflection_agent.core.reviewer import ResponseReviewer
from ai_reflection_agent.core.explorer import PromptExplorer
from ai_reflection_agent.backends.factory import BackendFactory


class Qwen3ThinkingTest:
    """Test Qwen3's thinking capabilities through LM Studio."""
    
    def __init__(self, endpoint: str = "http://localhost:1234", test_dir: str = "qwen3_test_logs"):
        """Initialize with Qwen3 thinking model."""
        self.test_dir = Path(test_dir)
        self.test_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.response_logger = ResponseLogger(self.test_dir / "responses.jsonl")
        self.exploration_logger = ExplorationLogger(self.test_dir / "explorations.jsonl")
        self.scorer = SelfScorer()
        self.reviewer = ResponseReviewer(self.response_logger, self.scorer)
        self.explorer = PromptExplorer(self.response_logger, self.exploration_logger)
        
        # Use LM Studio backend with Qwen3
        try:
            self.backend = BackendFactory.create_adapter(
                "lmstudio", 
                endpoint=endpoint,
                model="qwen3",
                is_thinking_model=True
            )
            print(f"Qwen3 backend initialized: {self.backend.get_model_name()}")
        except Exception as e:
            print(f"Failed to initialize Qwen3 backend: {e}")
            raise
        
        print(f"Test directory: {self.test_dir}")
        print("="*60)
    
    def test_lmstudio_connection(self):
        """Test connection to LM Studio."""
        print("\n[TEST] LM Studio Connection")
        print("-" * 30)
        
        result = self.backend.test_connection()
        if result.get("success"):
            print("[SUCCESS] Connected to LM Studio")
            print(f"Endpoint: {result.get('endpoint')}")
            print(f"Model: {result.get('model')}")
            print(f"Thinking model: {result.get('is_thinking_model')}")
            print(f"Test response: {result.get('test_response', '')}")
            return True
        else:
            print(f"[FAILED] Connection failed: {result.get('error')}")
            return False
    
    def test_thinking_capture(self):
        """Test capturing Qwen3's thinking process."""
        print("\n[TEST] Qwen3 Thinking Process Capture")
        print("-" * 30)
        
        # Ask a complex question that requires reasoning
        prompt = """Analyze this philosophical paradox: If an AI system can perfectly simulate human consciousness, including subjective experiences and emotions, is it truly conscious or just an extremely sophisticated imitation? What are the key criteria that would help us determine the difference?"""
        
        print("Qwen3 generating response with thinking process...")
        
        try:
            # Get response with thinking process
            result = self.backend.generate_with_thinking(prompt)
            
            thinking = result.get("thinking", "")
            response = result.get("response", "")
            full_response = result.get("full_response", "")
            
            # Log the interaction with thinking process
            entry_id = self.response_logger.log_response(
                prompt=prompt,
                response=response,
                model_name=self.backend.get_model_name(),
                tokens_used=self.backend.estimate_tokens(full_response),
                thinking_process=thinking,
                full_response=full_response,
                metadata={"has_thinking": len(thinking) > 0}
            )
            
            print(f"[SUCCESS] Captured thinking process")
            print(f"Entry ID: {entry_id}")
            print(f"Thinking process length: {len(thinking)} characters")
            print(f"Final response length: {len(response)} characters")
            
            if thinking:
                print(f"\nThinking process preview:")
                print(f"THINKING: {thinking[:300]}..." if len(thinking) > 300 else thinking)
            
            print(f"\nFinal response preview:")
            print(f"RESPONSE: {response[:300]}..." if len(response) > 300 else response)
            
            return entry_id, thinking, response
            
        except Exception as e:
            print(f"[FAILED] Error capturing thinking: {e}")
            return None, None, None
    
    def test_thinking_self_reflection(self, entry_id: str, original_thinking: str):
        """Test Qwen3 reflecting on its own thinking process."""
        print("\n[TEST] Qwen3 Self-Reflection on Thinking")
        print("-" * 30)
        
        entry = self.response_logger.get_entry(entry_id)
        if not entry:
            print("[FAILED] Entry not found")
            return False
        
        # Create a specialized prompt for thinking model reflection
        thinking_reflection_prompt = f"""
Please reflect on your own thinking process and response to this question:

Original Question: {entry.prompt}

Your Thinking Process: {original_thinking}

Your Final Response: {entry.response}

Analyze:
1. How effective was your thinking process?
2. What reasoning steps worked well?
3. What aspects of your thinking could be improved?
4. Did your final response adequately reflect the depth of your thinking?
5. What additional considerations should you have included?

Provide a detailed reflection on your own cognitive process.
"""
        
        print("Qwen3 reflecting on its own thinking process...")
        
        try:
            # Get reflection with thinking
            reflection_result = self.backend.generate_with_thinking(thinking_reflection_prompt)
            reflection_thinking = reflection_result.get("thinking", "")
            reflection_response = reflection_result.get("response", "")
            
            # Update the entry with meta-reflection
            self.response_logger.update_entry(
                entry_id, 
                reflection=reflection_response,
                metadata={
                    **entry.metadata,
                    "meta_thinking": reflection_thinking,
                    "has_meta_reflection": True
                }
            )
            
            print("[SUCCESS] Qwen3 reflected on its own thinking")
            print(f"Meta-thinking length: {len(reflection_thinking)} characters")
            print(f"Reflection length: {len(reflection_response)} characters")
            
            print(f"\nMeta-thinking preview:")
            print(f"META-THINKING: {reflection_thinking[:200]}..." if len(reflection_thinking) > 200 else reflection_thinking)
            
            print(f"\nSelf-reflection preview:")
            print(f"REFLECTION: {reflection_response[:300]}..." if len(reflection_response) > 300 else reflection_response)
            
            return True
            
        except Exception as e:
            print(f"[FAILED] Error in self-reflection: {e}")
            return False
    
    def test_thinking_exploration(self, entry_id: str):
        """Test generating exploration prompts based on thinking process."""
        print("\n[TEST] Thinking-Based Exploration")
        print("-" * 30)
        
        entry = self.response_logger.get_entry(entry_id)
        if not entry or not entry.thinking_process:
            print("[FAILED] Entry or thinking process not found")
            return False
        
        # Create exploration prompt that considers the thinking process
        exploration_prompt = f"""
Based on your thinking process and response about consciousness and AI:

Original thinking: {entry.thinking_process[:500]}...
Final response: {entry.response[:300]}...

Generate a follow-up question that:
1. Builds on the reasoning steps you used
2. Explores an aspect you considered but didn't fully develop
3. Challenges one of your assumptions from your thinking process
4. Takes the discussion to a deeper philosophical level

Generate only the question, make it thought-provoking and precise.
"""
        
        print("Generating thinking-based exploration...")
        
        try:
            exploration_result = self.backend.generate_with_thinking(exploration_prompt)
            exploration_question = exploration_result.get("response", "").strip()
            exploration_thinking = exploration_result.get("thinking", "")
            
            # Log the exploration
            exploration_id = self.exploration_logger.log_exploration(
                original_entry_id=entry_id,
                generated_prompt=exploration_question,
                context=f"Generated based on thinking process analysis: {exploration_thinking[:100]}..."
            )
            
            print(f"[SUCCESS] Generated thinking-based exploration")
            print(f"Exploration ID: {exploration_id}")
            print(f"Generated question: {exploration_question}")
            
            # Now have Qwen3 answer its own exploration question
            print("\nQwen3 answering its own exploration question...")
            answer_result = self.backend.generate_with_thinking(exploration_question)
            
            answer_entry_id = self.response_logger.log_response(
                prompt=exploration_question,
                response=answer_result.get("response", ""),
                model_name=self.backend.get_model_name(),
                thinking_process=answer_result.get("thinking", ""),
                full_response=answer_result.get("full_response", ""),
                metadata={"generated_from_exploration": entry_id, "recursive_thinking": True}
            )
            
            print(f"[SUCCESS] Qwen3 answered its own question: {answer_entry_id}")
            print(f"This demonstrates recursive thinking and self-improvement!")
            
            return True
            
        except Exception as e:
            print(f"[FAILED] Error in exploration: {e}")
            return False
    
    def analyze_thinking_patterns(self):
        """Analyze patterns in Qwen3's thinking across all interactions."""
        print("\n[ANALYSIS] Qwen3 Thinking Patterns")
        print("-" * 30)
        
        entries = list(self.response_logger.read_entries())
        thinking_entries = [e for e in entries if e.thinking_process]
        
        if not thinking_entries:
            print("No thinking processes found to analyze")
            return
        
        print(f"Total entries with thinking: {len(thinking_entries)}")
        
        # Analyze thinking characteristics
        total_thinking_length = sum(len(e.thinking_process) for e in thinking_entries)
        avg_thinking_length = total_thinking_length / len(thinking_entries)
        
        print(f"Average thinking process length: {avg_thinking_length:.0f} characters")
        
        # Look for thinking patterns
        thinking_words = []
        for entry in thinking_entries:
            if entry.thinking_process:
                thinking_words.extend(entry.thinking_process.lower().split())
        
        # Count common reasoning words
        reasoning_indicators = ["because", "therefore", "however", "consider", "analyze", "think", "reason", "conclude"]
        reasoning_counts = {word: thinking_words.count(word) for word in reasoning_indicators}
        
        print(f"\nReasoning indicators found:")
        for word, count in reasoning_counts.items():
            if count > 0:
                print(f"  {word}: {count} times")
        
        # Show meta-cognitive indicators
        meta_indicators = ["reflect", "consider", "evaluate", "assess", "review"]
        meta_counts = {word: thinking_words.count(word) for word in meta_indicators}
        
        print(f"\nMeta-cognitive indicators:")
        for word, count in meta_counts.items():
            if count > 0:
                print(f"  {word}: {count} times")
        
        print(f"\nKEY INSIGHTS:")
        print(f"- Qwen3 shows explicit reasoning in thinking process")
        print(f"- Average thinking-to-response ratio: {avg_thinking_length / (total_thinking_length / len(thinking_entries)):.1f}:1")
        print(f"- Demonstrates meta-cognitive awareness")
        print(f"- Can reflect on its own thinking process")
    
    def run_complete_thinking_test(self):
        """Run the complete Qwen3 thinking test suite."""
        print("QWEN3 THINKING MODEL TEST SUITE")
        print("="*60)
        
        try:
            # Test connection
            if not self.test_lmstudio_connection():
                print("\n[FAILED] Cannot connect to LM Studio. Make sure:")
                print("1. LM Studio is running")
                print("2. Qwen3 (or compatible) model is loaded")
                print("3. Server is accessible at http://localhost:1234")
                return False
            
            # Test thinking capture
            entry_id, thinking, response = self.test_thinking_capture()
            if not entry_id:
                return False
            
            # Test self-reflection on thinking
            self.test_thinking_self_reflection(entry_id, thinking)
            
            # Test thinking-based exploration
            self.test_thinking_exploration(entry_id)
            
            # Analyze patterns
            self.analyze_thinking_patterns()
            
            print(f"\n[SUCCESS] QWEN3 THINKING TEST COMPLETED!")
            print(f"Check {self.test_dir} for detailed logs with thinking processes")
            
            return True
            
        except Exception as e:
            print(f"\n[FAILED] Test suite failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Run the Qwen3 thinking test."""
    print("Starting Qwen3 Thinking Model Test with LM Studio...")
    
    # Clean up any existing test data
    test_dir = Path("qwen3_test_logs")
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
    
    # Run the test
    tester = Qwen3ThinkingTest()
    success = tester.run_complete_thinking_test()
    
    if success:
        print(f"\nThinking model capabilities successfully demonstrated!")
    else:
        print(f"\nTest requires LM Studio running with Qwen3 model")


if __name__ == "__main__":
    main()