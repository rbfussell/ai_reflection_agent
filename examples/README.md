# Examples

This directory contains example scripts demonstrating AI Reflection Agent capabilities.

## Files

- **`quick_qwen3_test.py`** - Quick setup verification for Qwen3 + LM Studio
- Run this first to verify your thinking model setup is working

## Usage

```bash
# Verify Qwen3 setup
python examples/quick_qwen3_test.py

# Then use the CLI with thinking models
ai-reflect --backend lmstudio --endpoint http://localhost:1234 test-backend
```