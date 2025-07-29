#!/usr/bin/env python3
"""
Quick test to verify Qwen3 + LM Studio setup.
Run this to check if everything is working.
"""

import sys
from pathlib import Path

# Add the package to path for testing
sys.path.insert(0, str(Path(__file__).parent / "ai_reflection_agent"))

from ai_reflection_agent.backends.factory import BackendFactory


def quick_test():
    """Quick test to verify LM Studio + Qwen3 setup."""
    print("QUICK QWEN3 + LM STUDIO TEST")
    print("="*40)
    
    try:
        # Test LM Studio connection
        print("1. Testing LM Studio connection...")
        backend = BackendFactory.create_adapter(
            "lmstudio",
            endpoint="http://localhost:1234",
            model="qwen3",
            is_thinking_model=True
        )
        
        result = backend.test_connection()
        if result.get("success"):
            print("   [SUCCESS] LM Studio is running and accessible")
            print(f"   Model: {result.get('model')}")
            print(f"   Thinking model: {result.get('is_thinking_model')}")
        else:
            print(f"   [FAILED] {result.get('error')}")
            print("\n   SETUP REQUIRED:")
            print("   1. Start LM Studio")
            print("   2. Load a Qwen3 (or compatible thinking) model")
            print("   3. Start the local server")
            return False
        
        # Test thinking capture
        print("\n2. Testing thinking process capture...")
        test_prompt = "Think step by step: What is 2+2 and why?"
        
        thinking_result = backend.generate_with_thinking(test_prompt)
        thinking = thinking_result.get("thinking", "")
        response = thinking_result.get("response", "")
        
        if thinking:
            print("   [SUCCESS] Thinking process captured!")
            print(f"   Thinking length: {len(thinking)} characters")
            print(f"   Response length: {len(response)} characters")
            print(f"   Thinking preview: {thinking[:100]}...")
        else:
            print("   [WARNING] No thinking process found")
            print("   This might mean:")
            print("   - Model doesn't use <think> tags")
            print("   - Model configuration needs adjustment")
            print("   - Still works, but without thinking capture")
        
        print("\n3. Testing CLI integration...")
        print("   You can now use:")
        print("   ai-reflect --backend lmstudio test-backend")
        print("   ai-reflect --backend lmstudio log \"question\" \"answer\"")
        print("   python test_qwen3_thinking.py")
        
        print("\n[SUCCESS] Setup appears to be working!")
        print("Run 'python test_qwen3_thinking.py' for full test suite")
        
        return True
        
    except Exception as e:
        print(f"\n[FAILED] Setup test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure LM Studio is running on localhost:1234")
        print("2. Load a compatible model (Qwen3 or similar)")
        print("3. Start the server in LM Studio")
        print("4. Check for firewall/connection issues")
        return False


if __name__ == "__main__":
    quick_test()