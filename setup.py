from setuptools import setup, find_packages

setup(
    name="ai-reflection-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pydantic>=2.0.0",
        "anthropic>=0.5.0",
        "openai>=1.0.0",
        "aiohttp>=3.8.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-reflect=ai_reflection_agent.cli:main",
        ],
    },
    author="AI Reflection Agent",
    description="A CLI tool for AI models to log, score, and reflect on their responses",
    python_requires=">=3.8",
)