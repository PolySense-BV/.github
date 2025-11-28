"""
LLM client interface and implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMClient(ABC):
    """Base class for LLM clients."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: Input prompt
            **kwargs: Additional parameters

        Returns:
            Generated response
        """
        pass


class MockLLMClient(BaseLLMClient):
    """Mock LLM client for testing."""

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a mock response."""
        # Simple mock that returns JSON structure
        if "image" in prompt.lower():
            return """{
    "summary": "Mock image analysis: Images show normal production conditions with minor variations.",
    "observations": [
        {
            "image_timestamp": "2024-01-15T14:30:00",
            "finding": "Normal production flow observed",
            "severity": "low",
            "confidence": 0.7
        }
    ],
    "root_cause_hypotheses": ["Normal variation in production"],
    "recommendations": ["Continue monitoring"]
}"""
        else:
            return """{
    "summary": "Mock analysis: Production quality is stable with minor fluctuations.",
    "findings": [
        {
            "type": "trend",
            "description": "Defect rate has increased slightly over the past week",
            "significance": "May indicate equipment wear or material quality issues",
            "needs_images": false,
            "image_timestamps": [],
            "image_reason": ""
        }
    ],
    "recommendations": [
        "Monitor defect rate trend over next few days",
        "Check equipment maintenance schedule"
    ]
}"""


class OpenAILLMClient(BaseLLMClient):
    """OpenAI API client implementation."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key
            model: Model name to use
        """
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError(
                "openai package required. Install with: pip install openai"
            )

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a production quality analysis expert."},
                {"role": "user", "content": prompt},
            ],
            **kwargs,
        )
        return response.choices[0].message.content


class GeminiLLMClient(BaseLLMClient):
    """Google Gemini API client implementation."""

    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """
        Initialize Gemini client.

        Args:
            api_key: Google API key
            model: Model name to use
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model)
        except ImportError:
            raise ImportError(
                "google-generativeai package required. "
                "Install with: pip install google-generativeai"
            )

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Gemini API."""
        response = self.model.generate_content(prompt, **kwargs)
        return response.text
