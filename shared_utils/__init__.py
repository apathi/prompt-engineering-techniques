"""
Shared utilities for prompt engineering implementations.

This package provides common functionality for all prompt engineering techniques:
- OpenAI API client wrapper
- Cost tracking and account balance monitoring  
- Logging configuration
"""

from .api_client import OpenAIClient
from .cost_tracker import CostTracker
from .logger import setup_logger
from .langchain_client import LangChainClient, get_llm, TokenUsageCallback
from .output_manager import OutputManager
from .prompt_chaining_utils import (
    PromptChainManager,
    ChainPerformanceMetrics,
    create_adaptive_complexity_chain,
    create_content_pipeline_chain,
    validate_summary_length,
    validate_json_structure,
    validate_bullet_format
)

__version__ = "1.0.0"
__all__ = [
    "OpenAIClient", 
    "CostTracker", 
    "setup_logger",
    "LangChainClient",
    "get_llm",
    "TokenUsageCallback",
    "OutputManager",
    "PromptChainManager",
    "ChainPerformanceMetrics",
    "create_adaptive_complexity_chain",
    "create_content_pipeline_chain",
    "validate_summary_length",
    "validate_json_structure",
    "validate_bullet_format"
]