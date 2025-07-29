#!/usr/bin/env python3
"""
Real Claude API test for AI Reflection Agent.
Uses actual Anthropic API to demonstrate true AI self-reflection.
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


class RealClaudeTest:
    """Test with real Claude API."""
    
    def __init__(self, api_key: str, test_dir: str = "claude_test_logs"):
        """Initialize with real Claude backend."""
        self.test_dir = Path(test_dir)
        self.test_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.response_logger = ResponseLogger(self.test_dir / "responses.jsonl")
        self.exploration_logger = ExplorationLogger(self.test_dir / "explorations.jsonl")
        self.scorer = SelfScorer()
        self.reviewer = ResponseReviewer(self.response_logger, self.scorer)
        self.explorer = PromptExplorer(self.response_logger, self.exploration_logger)
        
        # Use real Claude backend
        try:
            self.backend = BackendFactory.create_adapter(
                "claude", 
                api_key=api_key,
                model="claude-3-haiku-20240307"  # Using Haiku for cost efficiency
            )
            print(f"Claude backend initialized: {self.backend.get_model_name()}")
        except Exception as e:
            print(f"Failed to initialize Claude backend: {e}")
            raise
        
        print(f"Test directory: {self.test_dir}")
        print("="*60)
    
    def test_claude_connection(self):
        """Test the Claude API connection."""
        print("\n[TEST] Claude API Connection")
        print("-" * 30)
        
        result = self.backend.test_connection()
        if result.get("success"):
            print("SUCCESS: Connected to Claude API")
            print(f"Model: {result.get('model')}")
            print(f"Response length: {result.get('response_length')} chars")
            return True
        else:
            print(f"ERROR: {result.get('error')}")
            return False
    
    def test_real_self_reflection(self):
        """Test Claude reflecting on its own response."""
        print("\n[TEST] Real Claude Self-Reflection")
        print("-" * 30)
        
        # Start with a philosophical question that requires nuanced thinking
        prompt = "What is the most important unsolved problem in artificial intelligence, and why?"
        
        print("Claude generating initial response...")
        response = self.backend.generate_response(prompt)
        
        # Log the interaction
        entry_id = self.response_logger.log_response(
            prompt=prompt,
            response=response,
            model_name=self.backend.get_model_name(),
            tokens_used=self.backend.estimate_tokens(prompt + response)
        )
        
        print(f"Initial response logged: {entry_id}")
        print(f"Response preview: {response[:200]}...")
        
        # Now have Claude reflect on its own response
        print("\nClaude reflecting on its own response...")
        reflection_result = self.reviewer.reflect_on_response(
            self.response_logger.get_entry(entry_id), 
            self.backend
        )
        
        if reflection_result.get("success"):
            reflection = reflection_result["reflection"]
            self.response_logger.update_entry(entry_id, reflection=reflection)
            
            print("SUCCESS: Claude generated self-reflection:")
            print(f"Reflection: {reflection[:300]}...")
            
            return entry_id, reflection
        else:
            print(f"ERROR: {reflection_result.get('error')}")
            return None, None
    
    def test_real_self_scoring(self, entry_id: str):
        """Test Claude scoring its own response."""
        print("\n[TEST] Real Claude Self-Scoring")
        print("-" * 30)
        
        entry = self.response_logger.get_entry(entry_id)
        if not entry:
            print("ERROR: Entry not found")
            return False
        
        print("Claude evaluating its own response...")
        scoring_result = self.reviewer.score_response(entry, self.backend)
        
        if scoring_result.get("success"):
            score = scoring_result["score"]
            self.response_logger.update_entry(entry_id, score=score)
            
            print("SUCCESS: Claude scored its own response:")
            summary = self.scorer.get_score_summary(score)
            for metric, value in summary.items():
                print(f"   {metric.title()}: {value:.1f}/10")
            
            return True
        else:
            print(f"ERROR: {scoring_result.get('error')}")
            return False
    
    def test_real_exploration(self, entry_id: str):
        """Test Claude generating exploration prompts."""
        print("\n[TEST] Real Claude Exploration Generation")
        print("-" * 30)
        
        print("Claude generating exploration prompts...")
        
        # Generate one exploration of each type
        exploration_types = ["deepen", "alternative"]  # Limit to 2 to save tokens
        
        for exp_type in exploration_types:
            result = self.explorer.generate_exploration_prompt(
                entry_id, exp_type, self.backend
            )
            
            if result.get("success"):
                print(f"SUCCESS {exp_type.upper()}: {result['generated_prompt']}")
            else:
                print(f"ERROR {exp_type}: {result.get('error')}")
        
        return True
    
    def test_complete_real_cycle(self):
        """Test a complete real Claude reflection cycle."""
        print("\n[TEST] Complete Real Claude Reflection Cycle")
        print("-" * 30)
        
        # Test connection first
        if not self.test_claude_connection():
            return False
        
        # Run self-reflection test
        entry_id, reflection = self.test_real_self_reflection()
        if not entry_id:
            return False
        
        # Run self-scoring test
        self.test_real_self_scoring(entry_id)
        
        # Run exploration test
        self.test_real_exploration(entry_id)
        
        # Show final results
        print(f"\nFINAL RESULTS:")
        print("-" * 20)
        
        entries = list(self.response_logger.read_entries())
        explorations = list(self.exploration_logger.read_explorations())
        
        print(f"Total Claude interactions: {len(entries)}")
        print(f"Total explorations generated: {len(explorations)}")
        
        # Show the complete cycle
        final_entry = self.response_logger.get_entry(entry_id)
        if final_entry:
            print(f"\nClaude's self-reflection journey:")
            print(f"1. Original prompt: {final_entry.prompt}")
            print(f"2. Initial response: {final_entry.response[:100]}...")
            if final_entry.score:
                scores = self.scorer.get_score_summary(final_entry.score)
                print(f"3. Self-evaluation: Overall {scores['overall']:.1f}/10")
            if final_entry.reflection:
                print(f"4. Self-reflection: {final_entry.reflection[:100]}...")
        
        return True


def main():
    """Run the real Claude test."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Please set ANTHROPIC_API_KEY environment variable")
        return
    
    print("REAL CLAUDE AI REFLECTION TEST")
    print("Using Anthropic Claude-3-Haiku")
    print("="*60)
    
    # Clean up any existing test data
    test_dir = Path("claude_test_logs")
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
    
    try:
        # Run the real Claude test
        tester = RealClaudeTest(api_key)
        success = tester.test_complete_real_cycle()
        
        if success:
            print(f"\nREAL CLAUDE TEST COMPLETED SUCCESSFULLY!")
            print(f"This demonstrates actual AI self-reflection using Claude's API")
        else:
            print(f"\nTest encountered issues - check API key and connection")
            
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()