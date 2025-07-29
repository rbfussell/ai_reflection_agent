# Tests

This directory contains test scripts for validating AI Reflection Agent functionality.

## Test Files

- **`test_agency.py`** - Comprehensive agency test with mock backend
- **`test_qwen3_thinking.py`** - Specialized test for thinking models (requires LM Studio)
- **`test_real_claude.py`** - Real Claude API test (requires Anthropic API key)

## Running Tests

```bash
# Basic agency test (works without API keys)
python tests/test_agency.py

# Thinking model test (requires LM Studio running)
python tests/test_qwen3_thinking.py

# Real Claude test (requires ANTHROPIC_API_KEY)
python tests/test_real_claude.py
```

## Requirements

- Mock tests: No external dependencies
- LM Studio tests: Requires LM Studio running with thinking model
- Claude tests: Requires valid Anthropic API key with credits