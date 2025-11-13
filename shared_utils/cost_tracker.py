"""
Cost tracking and account balance monitoring for OpenAI API usage.
"""

import csv
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

import openai
from .logger import setup_logger


@dataclass
class UsageRecord:
    """Record of API usage for cost tracking."""
    timestamp: str
    technique: str
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float


class CostTracker:
    """Track API usage costs and account balance."""
    
    # GPT-4o-mini pricing (per 1M tokens)
    MODEL_PRICING = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "gpt-4": {"input": 30.0, "output": 60.0},
    }
    
    def __init__(self, session_name: Optional[str] = None):
        """
        Initialize cost tracker.
        
        Args:
            session_name: Optional session identifier
        """
        self.logger = setup_logger("cost_tracker")
        self.session_name = session_name or f"session_{int(time.time())}"
        self.usage_records: List[UsageRecord] = []
        self.total_cost = 0.0
        
    def track_usage(
        self,
        technique: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Track API usage and calculate cost.
        
        Args:
            technique: Name of the technique being used
            model: OpenAI model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Total cost for this request
        """
        if model not in self.MODEL_PRICING:
            self.logger.warning(f"Unknown model {model}, using gpt-4o-mini pricing")
            model = "gpt-4o-mini"
        
        pricing = self.MODEL_PRICING[model]
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        record = UsageRecord(
            timestamp=datetime.now().isoformat(),
            technique=technique,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost
        )
        
        self.usage_records.append(record)
        self.total_cost += total_cost
        
        self.logger.info(
            f"{technique}: {input_tokens} in + {output_tokens} out tokens, "
            f"${total_cost:.4f} (${self.total_cost:.4f} total)"
        )
        
        return total_cost
    
    def get_session_summary(self) -> Dict:
        """Get summary of current session usage."""
        if not self.usage_records:
            return {
                "session": self.session_name,
                "total_requests": 0,
                "total_cost": 0.0,
                "total_tokens": 0
            }
        
        total_input_tokens = sum(r.input_tokens for r in self.usage_records)
        total_output_tokens = sum(r.output_tokens for r in self.usage_records)
        
        return {
            "session": self.session_name,
            "total_requests": len(self.usage_records),
            "total_cost": self.total_cost,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "techniques_used": list(set(r.technique for r in self.usage_records))
        }
    
    async def get_account_balance(self) -> Optional[Dict]:
        """
        Get OpenAI account balance and usage information.
        
        Returns:
            Dictionary with account information or None if unavailable
        """
        try:
            client = openai.OpenAI()
            
            # Note: This endpoint may not be available in all API versions
            # Alternative: Check billing/usage through OpenAI dashboard
            self.logger.info("Account balance checking requires dashboard access")
            return {
                "message": "Check account balance at https://platform.openai.com/usage",
                "session_cost": self.total_cost
            }
        except Exception as e:
            self.logger.error(f"Could not retrieve account balance: {e}")
            return None
    
    def export_to_csv(self, filename: Optional[str] = None) -> str:
        """
        Export usage records to CSV file.
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"usage_{self.session_name}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            if self.usage_records:
                writer = csv.DictWriter(csvfile, fieldnames=asdict(self.usage_records[0]).keys())
                writer.writeheader()
                for record in self.usage_records:
                    writer.writerow(asdict(record))
        
        self.logger.info(f"Usage data exported to {filename}")
        return filename
    
    def print_summary(self) -> None:
        """Print a formatted summary of the session."""
        summary = self.get_session_summary()
        
        print(f"\n{'='*50}")
        print(f"SESSION SUMMARY: {summary['session']}")
        print(f"{'='*50}")
        print(f"Total Requests: {summary['total_requests']}")
        print(f"Total Cost: ${summary['total_cost']:.4f}")
        print(f"Total Tokens: {summary['total_tokens']:,}")
        print(f"  - Input: {summary.get('total_input_tokens', 0):,}")
        print(f"  - Output: {summary.get('total_output_tokens', 0):,}")
        print(f"Techniques Used: {', '.join(summary.get('techniques_used', []))}")
        print(f"{'='*50}\n")