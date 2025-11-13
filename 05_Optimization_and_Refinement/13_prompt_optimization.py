#!/usr/bin/env python3
"""
Technique 13: Prompt Optimization - Systematic Performance Improvement

Demonstrates A/B testing and iterative optimization to improve prompt 
performance through systematic refinement and measurement.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, OutputManager
from typing import Dict, List, Any
import time


class PromptOptimization:
    """Clean prompt optimization with A/B testing."""
    
    def __init__(self):
        self.client = LangChainClient()
        self.llm = self.client.get_llm()
        self.output_manager = OutputManager("13-prompt-optimization")
    
    def run_examples(self):
        """Execute two progressive examples."""
        
        self.output_manager.add_header("TECHNIQUE 13: PROMPT OPTIMIZATION")
        self.output_manager.add_line("Systematic A/B testing and performance improvement")
        self.output_manager.add_line()
        
        results = {
            "examples": [
                self._example_1_ab_testing(),
                self._example_2_optimization_pipeline()
            ]
        }
        
        self.output_manager.display_results(results)
        
        # Add final cost summary
        self.client.print_cost_summary()
        
        self.output_manager.save_to_file()
        return results
    
    def _test_variant(self, prompt: str, content: str) -> Dict[str, Any]:
        """Test a single prompt variant."""
        start_time = time.time()
        response = self.llm.invoke(f"{prompt}\n\n{content}").content
        execution_time = time.time() - start_time
        
        return {
            "response": response,
            "execution_time": round(execution_time, 2),
            "word_count": len(response.split()),
            "has_bullets": "•" in response or "-" in response
        }
    
    def _score_response(self, result: Dict[str, Any], target_words: int = 40) -> float:
        """Simple response quality scoring."""
        score = 5.0
        
        # Word count efficiency
        if result["word_count"] <= target_words:
            score += 1.5
        elif result["word_count"] <= target_words * 1.5:
            score += 0.5
        
        # Format bonus
        if result["has_bullets"]:
            score += 1.0
        
        # Speed bonus
        if result["execution_time"] < 3.0:
            score += 0.5
        
        return min(score, 8.0)
    
    def _example_1_ab_testing(self):
        """Example 1: Simple A/B Testing Framework"""
        
        article = """The renewable energy sector experienced unprecedented growth in 2023, 
        with solar installations increasing by 47% globally. Wind energy capacity expanded 
        by 32%, driven by technological improvements and decreasing costs. However, grid 
        integration challenges remain a significant obstacle."""
        
        # Test variants
        variants = {
            "Basic": "Summarize this article in 2 sentences.",
            "Structured": "Summarize this article in exactly 2 bullet points, each under 25 words.",
            "Focused": "Extract the 2 most important facts as brief bullet points."
        }
        
        # Test each variant
        results = {}
        for name, prompt in variants.items():
            results[name] = self._test_variant(prompt, f"Article: {article}")
            results[name]["score"] = self._score_response(results[name])
        
        # Find winner
        winner = max(results.keys(), key=lambda k: results[k]["score"])
        
        return {
            "technique": "A/B Testing Framework",
            "examples": [
                {
                    "approach": "Multi-Variant Performance Testing",
                    "problem": "Optimize article summarization for consistency and format",
                    "variants_tested": len(variants),
                    "winner": winner,
                    "winning_score": f"{results[winner]['score']}/8.0",
                    "response": results[winner]["response"],
                    "why_this_works": "A/B testing reveals which prompt elements drive better performance. Systematic scoring enables data-driven optimization decisions."
                }
            ]
        }
    
    def _example_2_optimization_pipeline(self):
        """Example 2: Multi-Stage Optimization Pipeline"""
        
        product = "Wireless noise-canceling headphones with 30-hour battery life"
        
        # Progressive optimization stages
        stages = [
            ("Baseline", "Describe this product for an e-commerce site."),
            ("Add_Structure", "Create a product description with: Features, Benefits, Target audience."),
            ("Add_Constraints", "Write a 75-word product description with: 3 key features, 2 benefits, target audience."),
            ("Optimize_Format", """Create an e-commerce product description (75 words max):

Format:
🎧 [Key Feature 1]
🎧 [Key Feature 2] 
🎧 [Key Feature 3]
Perfect for: [Target audience]""")
        ]
        
        stage_results = []
        for stage_name, prompt in stages:
            result = self._test_variant(prompt, f"Product: {product}")
            
            # Quality metrics
            quality_score = 0
            if result["word_count"] <= 85:  # Within constraint
                quality_score += 2
            if any(marker in result["response"] for marker in ["🎧", "•", "-", ":"]):
                quality_score += 2
            if any(word in result["response"].lower() for word in ["for", "perfect", "ideal"]):
                quality_score += 2
            
            stage_results.append({
                "stage": stage_name,
                "quality_score": f"{quality_score}/6",
                "word_count": result["word_count"],
                "response": result["response"]
            })
        
        # Calculate improvement
        final_score = int(stage_results[-1]["quality_score"].split("/")[0])
        initial_score = int(stage_results[0]["quality_score"].split("/")[0])
        improvement = ((final_score - initial_score) / 6) * 100
        
        return {
            "technique": "Multi-Stage Optimization Pipeline", 
            "examples": [
                {
                    "approach": "Progressive Enhancement",
                    "problem": "E-commerce product description optimization through iterative refinement",
                    "stages": len(stages),
                    "improvement": f"{improvement:.0f}%",
                    "final_quality": stage_results[-1]["quality_score"],
                    "response": stage_results[-1]["response"],
                    "why_this_works": "Multi-stage optimization allows systematic improvement through incremental refinement. Each stage addresses specific quality dimensions, ensuring measurable progress."
                }
            ]
        }


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("TECHNIQUE 13: PROMPT OPTIMIZATION")
    print("="*60)
    
    optimization = PromptOptimization()
    results = optimization.run_examples()
    return results


if __name__ == "__main__":
    main()