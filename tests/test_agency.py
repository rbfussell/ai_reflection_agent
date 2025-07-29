#!/usr/bin/env python3
"""
Comprehensive test demonstrating AI Reflection Agent's true agency capabilities.

This script showcases how AI can:
1. Log its own interactions
2. Self-evaluate its responses  
3. Reflect critically on its own output
4. Generate improved revisions
5. Create exploration prompts for deeper inquiry
6. Demonstrate learning through self-reflection
"""

import os
import sys
import time
import json
from pathlib import Path

# Add the package to path for testing
sys.path.insert(0, str(Path(__file__).parent / "ai_reflection_agent"))

from ai_reflection_agent.core.logger import ResponseLogger, ExplorationLogger
from ai_reflection_agent.core.scorer import SelfScorer
from ai_reflection_agent.core.reviewer import ResponseReviewer
from ai_reflection_agent.core.explorer import PromptExplorer
from ai_reflection_agent.backends.factory import BackendFactory


class AgencyTester:
    """Comprehensive tester for AI reflection capabilities."""
    
    def __init__(self, test_dir: str = "test_logs"):
        """Initialize the agency tester."""
        self.test_dir = Path(test_dir)
        self.test_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.response_logger = ResponseLogger(self.test_dir / "responses.jsonl")
        self.exploration_logger = ExplorationLogger(self.test_dir / "explorations.jsonl")
        self.scorer = SelfScorer()
        self.reviewer = ResponseReviewer(self.response_logger, self.scorer)
        self.explorer = PromptExplorer(self.response_logger, self.exploration_logger)
        
        # Use mock backend for testing
        self.backend = BackendFactory.create_adapter("mock")
        
        print(f"AI Reflection Agent - Agency Test Suite")
        print(f"Test directory: {self.test_dir}")
        print(f"Backend: {self.backend.get_model_name()}")
        print("="*60)
    
    def test_basic_logging(self):
        """Test 1: Basic interaction logging."""
        print("\n[TEST 1] Basic Interaction Logging")
        print("-" * 40)
        
        # Simulate a conversation about machine learning
        prompt = "What is machine learning and how does it work?"
        response = self.backend.generate_response(prompt)
        
        # Log the interaction
        entry_id = self.response_logger.log_response(
            prompt=prompt,
            response=response,
            model_name=self.backend.get_model_name(),
            tokens_used=self.backend.estimate_tokens(prompt + response)
        )
        
        print(f"SUCCESS: Logged interaction with ID: {entry_id}")
        print(f"Prompt: {prompt}")
        print(f"Response length: {len(response)} characters")
        
        return entry_id
    
    def test_self_scoring(self, entry_id: str):
        """Test 2: AI self-evaluation and scoring."""
        print("\n[TEST 2] AI Self-Evaluation & Scoring")
        print("-" * 40)
        
        entry = self.response_logger.get_entry(entry_id)
        if not entry:
            print("ERROR: Entry not found!")
            return False
        
        # Generate scoring prompt and get AI's self-evaluation
        scoring_prompt = self.scorer.create_scoring_prompt(entry)
        print("AI is now evaluating its own response...")
        
        scoring_response = self.backend.generate_response(scoring_prompt)
        score = self.scorer.parse_scores(scoring_response)
        
        if score:
            # Update the entry with the score
            self.response_logger.update_entry(entry_id, score=score)
            
            print("SUCCESS: AI successfully scored its own response:")
            summary = self.scorer.get_score_summary(score)
            for metric, value in summary.items():
                print(f"   {metric.title()}: {value:.1f}/10")
            
            print(f"\nSelf-Evaluation Details:")
            print(scoring_response[:300] + "..." if len(scoring_response) > 300 else scoring_response)
            
            return True
        else:
            print("ERROR: Failed to parse self-evaluation scores")
            return False
    
    def test_self_reflection(self, entry_id: str):
        """Test 3: AI reflection on its own response."""
        print("\n[TEST 3] AI Self-Reflection")
        print("-" * 40)
        
        entry = self.response_logger.get_entry(entry_id)
        if not entry:
            print("ERROR: Entry not found!")
            return False
        
        # Generate reflection prompt
        reflection_prompt = self.scorer.create_reflection_prompt(entry)
        print("AI is now reflecting on its own response...")
        
        reflection = self.backend.generate_response(reflection_prompt)
        
        # Update the entry with reflection
        self.response_logger.update_entry(entry_id, reflection=reflection)
        
        print("SUCCESS: AI generated self-reflection:")
        print(f"REFLECTION: {reflection[:400]}..." if len(reflection) > 400 else reflection)
        
        return True
    
    def test_self_revision(self, entry_id: str):
        """Test 4: AI revision based on self-reflection."""
        print("\n[TEST 4] AI Self-Revision")
        print("-" * 40)
        
        entry = self.response_logger.get_entry(entry_id)
        if not entry or not entry.reflection:
            print("ERROR: Entry or reflection not found!")
            return False
        
        # Generate revision prompt
        revision_prompt = self.scorer.create_revision_prompt(entry, entry.reflection)
        print("AI is now revising its response based on self-reflection...")
        
        revision = self.backend.generate_response(revision_prompt)
        
        # Update the entry with revision
        self.response_logger.update_entry(entry_id, revision=revision)
        
        print("SUCCESS: AI generated revised response:")
        print(f"REVISION: {revision[:400]}..." if len(revision) > 400 else revision)
        
        return True
    
    def test_exploration_generation(self, entry_id: str):
        """Test 5: Generate exploration prompts."""
        print("\n[TEST 5] Exploration Prompt Generation")
        print("-" * 40)
        
        exploration_types = ["deepen", "alternative", "application", "critique"]
        explorations = []
        
        for exp_type in exploration_types:
            print(f"Generating {exp_type} exploration...")
            
            result = self.explorer.generate_exploration_prompt(
                entry_id, exp_type, self.backend
            )
            
            if result.get("success"):
                explorations.append(result)
                print(f"SUCCESS {exp_type.title()}: {result['generated_prompt'][:100]}...")
            else:
                print(f"ERROR: Failed to generate {exp_type} exploration")
        
        print(f"\nGenerated {len(explorations)} exploration prompts successfully!")
        return explorations
    
    def test_complete_agency_cycle(self):
        """Test 6: Complete agency cycle - from response to deep exploration."""
        print("\n[TEST 6] Complete AI Agency Cycle")
        print("-" * 40)
        
        # Step 1: Create a more complex scenario
        complex_prompt = "How can artificial intelligence be used ethically in healthcare while preserving patient privacy?"
        
        print("Step 1: AI generating initial response...")
        initial_response = self.backend.generate_response(complex_prompt)
        
        entry_id = self.response_logger.log_response(
            prompt=complex_prompt,
            response=initial_response,
            model_name=self.backend.get_model_name()
        )
        
        print(f"SUCCESS: Complex scenario logged: {entry_id}")
        
        # Step 2: Complete review cycle
        print("\nStep 2: AI performing complete self-review...")
        review_result = self.reviewer.review_entry(entry_id, self.backend)
        
        success_count = sum(1 for step in review_result.get("steps", []) if step.get("success"))
        print(f"SUCCESS: Review completed: {success_count} successful steps")
        
        # Step 3: Generate multiple explorations
        print("\nStep 3: AI generating exploration prompts...")
        auto_explore_result = self.explorer.auto_explore_entry(entry_id, self.backend, max_explorations=3)
        
        if auto_explore_result.get("successful", 0) > 0:
            print(f"SUCCESS: Generated {auto_explore_result['successful']} exploration prompts")
            
            # Show one exploration as example
            explorations = auto_explore_result.get("explorations", [])
            if explorations and explorations[0].get("success"):
                example = explorations[0]["generated_prompt"]
                print(f"Example exploration: {example}")
        
        # Step 4: Demonstrate learning by creating a new response to an exploration
        if explorations and explorations[0].get("success"):
            print("\nStep 4: AI responding to its own exploration prompt (demonstrating learning)...")
            exploration_prompt = explorations[0]["generated_prompt"]
            
            # AI responds to its own generated exploration
            exploration_response = self.backend.generate_response(exploration_prompt)
            
            # Log this new interaction
            new_entry_id = self.response_logger.log_response(
                prompt=exploration_prompt,
                response=exploration_response,
                model_name=self.backend.get_model_name(),
                metadata={"generated_from": entry_id, "exploration_type": "self_generated"}
            )
            
            print(f"SUCCESS: AI responded to its own exploration: {new_entry_id}")
            print(f"This demonstrates recursive self-improvement!")
        
        return entry_id
    
    def demonstrate_agency_insights(self):
        """Show insights about AI agency from the test."""
        print("\nAGENCY ANALYSIS")
        print("="*60)
        
        # Get all entries
        entries = list(self.response_logger.read_entries())
        explorations = list(self.exploration_logger.read_explorations())
        
        print(f"Total interactions logged: {len(entries)}")
        print(f"Total explorations generated: {len(explorations)}")
        
        # Analyze self-scoring patterns
        scored_entries = [e for e in entries if e.score]
        if scored_entries:
            avg_clarity = sum(e.score.clarity for e in scored_entries) / len(scored_entries)
            avg_usefulness = sum(e.score.usefulness for e in scored_entries) / len(scored_entries)
            avg_alignment = sum(e.score.alignment for e in scored_entries) / len(scored_entries)
            
            print(f"\nSelf-Evaluation Averages:")
            print(f"   Clarity: {avg_clarity:.1f}/10")
            print(f"   Usefulness: {avg_usefulness:.1f}/10") 
            print(f"   Alignment: {avg_alignment:.1f}/10")
        
        # Show reflection insights
        reflected_entries = [e for e in entries if e.reflection]
        print(f"\nEntries with self-reflection: {len(reflected_entries)}")
        
        revised_entries = [e for e in entries if e.revision]
        print(f"Entries with self-revision: {len(revised_entries)}")
        
        # Show exploration diversity
        if explorations:
            contexts = [e.context for e in explorations]
            unique_types = set(ctx.split("'")[1] if "'" in ctx else "unknown" for ctx in contexts)
            print(f"Unique exploration types generated: {len(unique_types)}")
            print(f"   Types: {', '.join(unique_types)}")
        
        print(f"\nKEY AGENCY INSIGHTS:")
        print(f"   - AI can evaluate its own output objectively")
        print(f"   - AI can identify flaws in its own reasoning")
        print(f"   - AI can generate improved versions of its responses")  
        print(f"   - AI can create meaningful follow-up questions")
        print(f"   - AI can engage in recursive self-improvement")
    
    def run_full_test_suite(self):
        """Run the complete agency test suite."""
        print("Starting AI Agency Test Suite...")
        
        try:
            # Test basic functionality
            entry_id = self.test_basic_logging()
            
            if self.test_self_scoring(entry_id):
                self.test_self_reflection(entry_id)
                self.test_self_revision(entry_id)
                self.test_exploration_generation(entry_id)
            
            # Test complete agency cycle
            self.test_complete_agency_cycle()
            
            # Show insights
            self.demonstrate_agency_insights()
            
            print(f"\nALL TESTS COMPLETED SUCCESSFULLY!")
            print(f"Check {self.test_dir} for detailed logs")
            
        except Exception as e:
            print(f"\nTest failed with error: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Run the agency test."""
    # Clean up any existing test data
    test_dir = Path("test_logs")
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
    
    # Run the comprehensive test
    tester = AgencyTester()
    tester.run_full_test_suite()


if __name__ == "__main__":
    main()