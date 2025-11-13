"""
LangChain client with cost tracking integration.

This module provides a unified LangChain client that integrates with
the existing cost tracking system while using modern LangChain patterns.
"""

from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from .cost_tracker import CostTracker


class TokenUsageCallback(BaseCallbackHandler):
    """Callback handler to track token usage for cost tracking."""
    
    def __init__(self, cost_tracker: CostTracker):
        """Initialize callback with cost tracker.
        
        Args:
            cost_tracker: CostTracker instance to record usage
        """
        self.cost_tracker = cost_tracker
        self.current_technique = "unknown"
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """Capture technique name from tags when LLM starts."""
        if "tags" in kwargs and kwargs["tags"]:
            self.current_technique = kwargs["tags"][0]
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Extract token usage from LangChain response and track costs.
        
        Args:
            response: LLMResult containing token usage information
            kwargs: Additional keyword arguments
        """
        if response.llm_output and "token_usage" in response.llm_output:
            usage = response.llm_output["token_usage"]
            self.cost_tracker.track_usage(
                technique=kwargs.get("tags", ["unknown"])[0] if kwargs.get("tags") else "unknown",
                model="gpt-4o-mini",  # Default model
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0)
            )


class LangChainClient:
    """Unified LangChain client with cost tracking."""
    
    def __init__(
        self, 
        model: str = "gpt-4o-mini", 
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
        cost_tracker: Optional[CostTracker] = None,
        session_name: Optional[str] = None
    ):
        """Initialize LangChain client with configuration.
        
        Args:
            model: OpenAI model to use
            temperature: Temperature for response generation
            max_tokens: Maximum tokens for response
            cost_tracker: Optional existing cost tracker
            session_name: Optional session name for cost tracking
        """
        self.cost_tracker = cost_tracker or CostTracker(session_name or "langchain_session")
        self.callback = TokenUsageCallback(self.cost_tracker)
        
        # Create LLM with callbacks
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=[self.callback],
            verbose=True
        )
    
    def get_llm(self) -> ChatOpenAI:
        """Get the configured LLM instance.
        
        Returns:
            ChatOpenAI instance with callbacks configured
        """
        return self.llm
    
    def print_cost_summary(self) -> None:
        """Print the cost tracking summary."""
        self.cost_tracker.print_summary()


def get_llm(
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
    verbose: bool = True
) -> ChatOpenAI:
    """Get a simple configured LLM instance without cost tracking.
    
    This is a convenience function for quick prototyping following
    the original notebook patterns.
    
    Args:
        model: OpenAI model to use
        temperature: Temperature for response generation  
        verbose: Whether to enable verbose logging
        
    Returns:
        Configured ChatOpenAI instance
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        verbose=verbose
    )