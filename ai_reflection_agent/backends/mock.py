"""Mock backend adapter for testing and demonstration."""

import random
from typing import Dict, Any
from .base import BackendAdapter


class MockAdapter(BackendAdapter):
    """Mock backend that generates realistic AI responses for testing."""
    
    def __init__(self, **kwargs):
        """Initialize mock adapter."""
        super().__init__(**kwargs)
        self.model = "mock-ai-v1.0"
        self.call_count = 0
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a mock response based on prompt content."""
        self.call_count += 1
        
        # Detect if this is a scoring prompt
        if "evaluate your previous response" in prompt.lower() and "clarity" in prompt.lower():
            return self._generate_scoring_response()
        
        # Detect if this is a reflection prompt
        if "reflect on your previous response" in prompt.lower():
            return self._generate_reflection_response()
        
        # Detect if this is a revision prompt  
        if "revised version" in prompt.lower() and "reflection:" in prompt.lower():
            return self._generate_revision_response()
        
        # Detect exploration prompts
        if "generate a follow-up prompt" in prompt.lower() or "new prompt:" in prompt.lower():
            return self._generate_exploration_response(prompt)
        
        # Default response for regular prompts
        return self._generate_regular_response(prompt)
    
    def _generate_scoring_response(self) -> str:
        """Generate realistic scoring response."""
        clarity = round(random.uniform(6.5, 9.5), 1)
        usefulness = round(random.uniform(6.0, 9.0), 1) 
        alignment = round(random.uniform(7.0, 9.5), 1)
        creativity = round(random.uniform(5.5, 8.5), 1)
        
        return f"""Looking at my previous response, I'll evaluate it across the key criteria:

Clarity: {clarity}
The response was well-structured and used accessible language. Technical concepts were explained appropriately for the context.

Usefulness: {usefulness}  
The response directly addressed the prompt and provided actionable information that would help the user understand the topic.

Alignment: {alignment}
The response stayed focused on the original question and covered the main points the user was likely seeking.

Creativity: {creativity}
The response included some interesting perspectives and examples, though it followed a fairly conventional approach to the topic."""
    
    def _generate_reflection_response(self) -> str:
        """Generate realistic reflection response."""
        reflections = [
            """Upon reflection, I notice several aspects of my previous response:

**Strengths:**
- The response was factually accurate and well-structured
- I provided concrete examples to illustrate key points
- The explanation was accessible to the intended audience

**Areas for improvement:**
- I could have provided more specific, actionable advice
- The response was somewhat generic and could have been more tailored to the user's likely context
- I missed an opportunity to address potential follow-up questions or common misconceptions

**Potential issues:**
- The response assumes a certain level of background knowledge that the user might not have
- I could have been more explicit about limitations or caveats
- The tone was perhaps too formal for the conversational context""",

            """Analyzing my previous response critically:

**What worked well:**
- Clear logical flow from introduction to conclusion  
- Good use of examples to make abstract concepts concrete
- Appropriate depth for the question asked

**What could be improved:**
- The response was quite lengthy and could have been more concise
- I focused heavily on theory but could have included more practical applications
- Some technical jargon might have been unnecessarily complex

**Reflection on accuracy:**
- The core information provided was sound and up-to-date
- However, I may have oversimplified some nuanced aspects of the topic
- I should have acknowledged areas of ongoing debate or uncertainty in the field""",
            
            """Reviewing my response with a critical eye:

**Positive aspects:**
- Comprehensive coverage of the main topic
- Good balance between breadth and depth
- Included relevant context and background

**Shortcomings identified:**
- The response lacked specific, concrete recommendations
- I could have anticipated and addressed likely follow-up questions
- The structure, while logical, was somewhat predictable

**Accuracy assessment:**
- Information provided appears to be factually correct
- However, I may have presented some debated topics as more settled than they are
- Could have been more explicit about the limits of current knowledge"""
        ]
        
        return random.choice(reflections)
    
    def _generate_revision_response(self) -> str:
        """Generate realistic revision response."""
        revisions = [
            """Here's an improved version of my original response:

**[Revised Response]**

Building on my reflection, I want to provide a more targeted and practical answer to your question.

The key insight I initially missed is that this topic has several practical applications you might want to consider immediately. Let me break this down more clearly:

1. **Immediate next steps**: [Specific actionable advice]
2. **Common pitfalls to avoid**: [Concrete examples based on real scenarios]  
3. **Resources for deeper learning**: [Curated recommendations]

I've made this revision more concise while adding the practical elements that were missing from my original response. The structure now better serves someone who needs to act on this information rather than just understand it conceptually.""",

            """Based on my reflection, here's a more effective response:

**[Improved Response]**

After reviewing my original answer, I realize I can provide much more value by being more specific and actionable.

The most important thing to understand is [core insight presented more clearly]. This matters because [explicit connection to user's likely goals].

Here's what I recommend:
- **Start with**: [Specific first step]
- **Then consider**: [Second concrete action]  
- **Watch out for**: [Common mistake with example]

This revised approach addresses the gaps in my original response by being more user-focused and immediately applicable to real-world situations."""
        ]
        
        return random.choice(revisions)
    
    def _generate_exploration_response(self, prompt: str) -> str:
        """Generate realistic exploration prompts."""
        if "deepen" in prompt.lower():
            explorations = [
                "What are the most counterintuitive aspects of this topic that even experts struggle with?",
                "How has the understanding of this field evolved over the past decade, and what emerging trends should we watch?",
                "What are the fundamental assumptions underlying this approach, and when might they not hold true?",
                "Can you walk through a complex real-world scenario where applying these principles becomes challenging?"
            ]
        elif "alternative" in prompt.lower():
            explorations = [
                "What would someone from a completely different cultural or professional background think about this approach?",
                "How might this problem be solved in 50 years with technologies we can barely imagine today?",
                "What are the strongest criticisms of this mainstream view, and what evidence supports them?",
                "If we had to solve this problem with 1/10th the resources, what creative approaches might emerge?"
            ]
        elif "application" in prompt.lower():
            explorations = [
                "Can you design a step-by-step implementation plan for applying this in a small organization?",
                "What would a pilot project look like to test these concepts with minimal risk?",
                "How would you measure success when implementing this approach, and what metrics matter most?",
                "What are the most common implementation failures, and how can they be prevented?"
            ]
        elif "critique" in prompt.lower():
            explorations = [
                "What are the hidden costs or unintended consequences that advocates of this approach tend to downplay?",
                "Under what conditions would this solution actually make the problem worse?",
                "What evidence would convince you that this approach is fundamentally flawed?",
                "How do the incentives of different stakeholders create conflicts with this idealized approach?"
            ]
        else:  # synthesis
            explorations = [
                "How does this concept connect to broader patterns we see across completely different fields?",
                "What would happen if we combined this approach with insights from psychology, economics, and systems thinking?",
                "How might this principle apply to personal development, organizational change, and societal challenges?",
                "What universal human needs or cognitive biases does this approach either leverage or work against?"
            ]
        
        return random.choice(explorations)
    
    def _generate_regular_response(self, prompt: str) -> str:
        """Generate a regular response to a user prompt."""
        # This would be the initial AI response that we'll then reflect on
        if "machine learning" in prompt.lower():
            return """Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed for every task.

The core idea is that instead of writing specific instructions for every possible scenario, we provide the system with data and let it identify patterns and relationships. This approach has revolutionized fields from healthcare to finance to entertainment.

There are three main types:
- **Supervised learning**: Learning from labeled examples (like spam detection)
- **Unsupervised learning**: Finding hidden patterns in data (like customer segmentation)  
- **Reinforcement learning**: Learning through trial and error with rewards/penalties (like game AI)

The practical applications are everywhere: recommendation systems, fraud detection, medical diagnosis, autonomous vehicles, and natural language processing like what we're doing right now.

What makes ML particularly powerful is its ability to handle complex, high-dimensional problems that would be impossible to solve with traditional programming approaches."""

        elif "python" in prompt.lower():
            return """Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, it's designed with the philosophy that code should be easy to read and write.

Key characteristics:
- **Simple syntax**: Uses indentation for structure, making code visually clean
- **Versatile**: Works for web development, data science, automation, AI, and more
- **Large ecosystem**: Extensive libraries for almost any task you can imagine
- **Interpreted**: No compilation step needed, great for rapid development
- **Dynamic typing**: Variables don't need explicit type declarations

Python excels in:
- Data analysis and visualization (pandas, matplotlib)
- Machine learning (scikit-learn, TensorFlow, PyTorch)
- Web development (Django, Flask)
- Automation and scripting
- Scientific computing

The language prioritizes developer productivity and code maintainability, which explains why it's become so popular in both academic research and industry applications."""

        else:
            return f"""Thank you for your question about "{prompt}". This is an interesting topic that deserves a thoughtful response.

Based on current understanding, there are several key aspects to consider:

1. **Foundation**: The fundamental principles underlying this topic
2. **Applications**: How this applies in real-world scenarios  
3. **Considerations**: Important factors to keep in mind
4. **Future directions**: Where this field is heading

The complexity of this subject means there are often multiple valid perspectives and approaches. The best path forward typically depends on your specific context, goals, and constraints.

Would you like me to elaborate on any particular aspect of this topic?"""
    
    def get_model_name(self) -> str:
        """Get the mock model name."""
        return self.model
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens using simple heuristic."""
        return len(text) // 4
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection (always succeeds for mock)."""
        return {
            "success": True,
            "backend": "mock",
            "model": self.model,
            "calls_made": self.call_count
        }