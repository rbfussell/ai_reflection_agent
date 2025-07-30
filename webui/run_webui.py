#!/usr/bin/env python3
"""
Startup script for AI Reflection Agent WebUI.

Usage:
    python run_webui.py
    python run_webui.py --host 0.0.0.0 --port 8080 --share
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import and run the WebUI
from webui.app import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 WebUI stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting WebUI: {e}")
        sys.exit(1)