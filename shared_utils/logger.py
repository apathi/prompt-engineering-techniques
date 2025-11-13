"""
Simple logging setup for prompt engineering implementations.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "prompt_engineering",
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
        format_string: Custom format string (optional)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Set format
    if format_string is None:
        format_string = "%(asctime)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger