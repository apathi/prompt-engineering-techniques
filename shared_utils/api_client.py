"""
OpenAI API client wrapper with error handling and token counting.
"""

import os
import time
from typing import Dict, Any, Optional, List
import tiktoken
import openai
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

from .cost_tracker import CostTracker
from .logger import setup_logger

# Load environment variables from .env file
load_dotenv()


class OpenAIClient:
    """OpenAI API client with cost tracking and error handling."""
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: int = 1000,
        cost_tracker: Optional[CostTracker] = None
    ):
        """
        Initialize OpenAI client.
        
        Args:
            model: OpenAI model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            cost_tracker: Cost tracking instance
        """
        self.logger = setup_logger("openai_client")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.cost_tracker = cost_tracker or CostTracker()
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        
        # Initialize tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            self.logger.warning(f"No tokenizer found for {model}, using cl100k_base")
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        self.logger.info(f"OpenAI client initialized with model: {model}")
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Input text
            
        Returns:
            Number of tokens
        """
        try:
            return len(self.tokenizer.encode(text))
        except Exception as e:
            self.logger.error(f"Token counting failed: {e}")
            # Fallback estimation: ~4 characters per token
            return len(text) // 4
    
    def generate_response(
        self,
        prompt: str,
        technique_name: str = "unknown",
        system_message: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using OpenAI API.
        
        Args:
            prompt: User prompt
            technique_name: Name of technique for tracking
            system_message: Optional system message
            **kwargs: Additional parameters for API call
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Prepare messages
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            # Count input tokens
            input_text = (system_message or "") + prompt
            input_tokens = self.count_tokens(input_text)
            
            # API parameters
            api_params = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get("temperature", self.temperature),
                "max_tokens": kwargs.get("max_tokens", self.max_tokens)
            }
            
            self.logger.info(f"Generating response for {technique_name}")
            
            # Make API call with retry logic
            response = self._make_api_call_with_retry(api_params)
            
            # Extract response data
            content = response.choices[0].message.content
            usage = response.usage
            
            # Track costs
            if usage:
                cost = self.cost_tracker.track_usage(
                    technique=technique_name,
                    model=self.model,
                    input_tokens=usage.prompt_tokens,
                    output_tokens=usage.completion_tokens
                )
            else:
                # Fallback token counting
                output_tokens = self.count_tokens(content or "")
                cost = self.cost_tracker.track_usage(
                    technique=technique_name,
                    model=self.model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
            
            return {
                "response": content,
                "model": self.model,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens if usage else input_tokens,
                    "completion_tokens": usage.completion_tokens if usage else self.count_tokens(content or ""),
                    "total_tokens": usage.total_tokens if usage else input_tokens + self.count_tokens(content or "")
                },
                "cost": cost,
                "technique": technique_name
            }
            
        except OpenAIError as e:
            self.logger.error(f"OpenAI API error in {technique_name}: {e}")
            return {
                "error": str(e),
                "technique": technique_name,
                "response": None
            }
        except Exception as e:
            self.logger.error(f"Unexpected error in {technique_name}: {e}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "technique": technique_name,
                "response": None
            }
    
    def _make_api_call_with_retry(self, params: Dict[str, Any], max_retries: int = 3) -> Any:
        """
        Make API call with exponential backoff retry.
        
        Args:
            params: API call parameters
            max_retries: Maximum number of retries
            
        Returns:
            API response
        """
        for attempt in range(max_retries + 1):
            try:
                return self.client.chat.completions.create(**params)
            except openai.RateLimitError as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    self.logger.warning(f"Rate limit hit, waiting {wait_time}s (attempt {attempt + 1})")
                    time.sleep(wait_time)
                else:
                    raise e
            except openai.APIError as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    self.logger.warning(f"API error, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    raise e
    
    def generate_multiple_responses(
        self,
        prompt: str,
        n_responses: int,
        technique_name: str = "unknown",
        system_message: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple responses for techniques like self-consistency.
        
        Args:
            prompt: User prompt
            n_responses: Number of responses to generate
            technique_name: Name of technique for tracking
            system_message: Optional system message
            **kwargs: Additional parameters
            
        Returns:
            List of response dictionaries
        """
        responses = []
        for i in range(n_responses):
            response = self.generate_response(
                prompt=prompt,
                technique_name=f"{technique_name}_response_{i+1}",
                system_message=system_message,
                **kwargs
            )
            responses.append(response)
        
        return responses
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost tracking summary."""
        return self.cost_tracker.get_session_summary()