#!/usr/bin/env python3
"""
Technique 15: Length Management - Dynamic Optimization

Demonstrates length optimization and readability balance to avoid 
overwhelming models while maintaining necessary detail.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, OutputManager
from typing import Dict, List, Any
import re


class LengthManagement:
    """Clean length optimization with readability scoring."""
    
    def __init__(self):
        self.client = LangChainClient()
        self.llm = self.client.get_llm()
        self.output_manager = OutputManager("15-length-management")
    
    def run_examples(self):
        """Execute two progressive examples."""
        
        self.output_manager.add_header("TECHNIQUE 15: LENGTH MANAGEMENT")
        self.output_manager.add_line("Dynamic length optimization and readability balance")
        self.output_manager.add_line()
        
        results = {
            "examples": [
                self._example_1_length_optimization(),
                self._example_2_context_hierarchy()
            ]
        }
        
        self.output_manager.display_results(results)
        
        # Add final cost summary
        self.client.print_cost_summary()
        
        self.output_manager.save_to_file()
        return results
    
    def _analyze_length(self, text: str) -> Dict[str, Any]:
        """Analyze text length and readability."""
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = len(re.findall(r'[.!?]+', text))
        
        # Simple readability scoring
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        readability_score = 10 - min(avg_words_per_sentence / 3, 8)  # Prefer shorter sentences
        
        return {
            "word_count": word_count,
            "char_count": char_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_words_per_sentence, 1),
            "readability_score": round(readability_score, 1)
        }
    
    def _optimize_prompt_length(self, base_prompt: str, target_length: str) -> str:
        """Optimize prompt for specific length requirements."""
        optimization_prompt = f"""Rewrite this prompt to be {target_length} while maintaining clarity:

Original: {base_prompt}

Optimized version:"""
        
        return self.llm.invoke(optimization_prompt).content
    
    def _example_1_length_optimization(self):
        """Example 1: Content Length Optimization with Readability Scoring"""
        
        # Long, detailed prompt
        verbose_prompt = """Please analyze the comprehensive quarterly financial performance 
        of technology companies in the renewable energy sector, taking into consideration 
        their revenue growth patterns, market share dynamics, competitive positioning 
        strategies, operational efficiency improvements, capital expenditure allocations, 
        research and development investments, regulatory compliance costs, supply chain 
        optimization initiatives, customer acquisition metrics, and long-term sustainability 
        goals while also evaluating their environmental impact assessments."""
        
        # Test different length optimizations
        length_variants = {
            "Original": verbose_prompt,
            "Concise": self._optimize_prompt_length(verbose_prompt, "concise and focused"),
            "Minimal": self._optimize_prompt_length(verbose_prompt, "under 30 words"),
            "Balanced": self._optimize_prompt_length(verbose_prompt, "clear and comprehensive but under 50 words")
        }
        
        # Test each variant
        variant_analysis = {}
        for variant_name, prompt in length_variants.items():
            response = self.llm.invoke(prompt).content
            analysis = self._analyze_length(prompt)
            analysis["response_quality"] = len(response.split())  # Response length as quality proxy
            variant_analysis[variant_name] = {
                "prompt_analysis": analysis,
                "response": response,
                "efficiency_score": analysis["readability_score"] + (100 / max(analysis["word_count"], 1))
            }
        
        # Find optimal variant
        best_variant = max(variant_analysis.keys(), 
                          key=lambda k: variant_analysis[k]["efficiency_score"])
        
        return {
            "technique": "Content Length Optimization with Readability Scoring",
            "examples": [
                {
                    "approach": "Multi-Length Variant Analysis",
                    "problem": "Verbose prompt needs length optimization while preserving clarity",
                    "original_words": variant_analysis["Original"]["prompt_analysis"]["word_count"],
                    "optimized_words": variant_analysis[best_variant]["prompt_analysis"]["word_count"],
                    "reduction_percentage": f"{(1 - variant_analysis[best_variant]['prompt_analysis']['word_count'] / variant_analysis['Original']['prompt_analysis']['word_count']) * 100:.0f}%",
                    "best_variant": best_variant,
                    "readability_score": f"{variant_analysis[best_variant]['prompt_analysis']['readability_score']}/10",
                    "response": variant_analysis[best_variant]["response"],
                    "why_this_works": "Length optimization reduces cognitive load on models while maintaining essential information. Readability scoring ensures clarity isn't sacrificed for brevity. Different length targets serve different use cases."
                }
            ]
        }
    
    def _example_2_context_hierarchy(self):
        """Example 2: Dynamic Context Hierarchy Management"""
        
        # Complex context with multiple layers
        full_context = """
        Company: TechFlow Solutions
        Industry: Software Development
        Team Size: 150 employees
        Revenue: $50M annually
        Main Products: Cloud management platform, API gateway, data analytics suite
        Recent Challenges: Scaling infrastructure, talent retention, market competition
        Current Project: Migrating legacy systems to microservices architecture
        Timeline: 18-month project, currently 6 months in
        Budget: $2.5M allocated, 40% spent
        Technical Stack: Python, React, PostgreSQL, Docker, Kubernetes
        Key Stakeholders: CTO, Engineering VP, Product Managers, DevOps team
        """
        
        task = "Create a project status report for executive leadership."
        
        # Test different context levels
        context_levels = {
            "Full_Context": f"{full_context}\n\nTask: {task}",
            "Essential_Only": """Company: TechFlow Solutions ($50M revenue)
Current Project: Legacy to microservices migration
Status: 6/18 months, 40% budget used
Task: Create executive status report.""",
            "Minimal_Context": f"TechFlow Solutions microservices migration project.\nTask: {task}",
            "Hierarchical": f"""PRIMARY: TechFlow migration project (6/18 months, 40% budget)
SECONDARY: $50M company, 150 employees, scaling challenges  
TERTIARY: Python/React stack, CTO/VP stakeholders

Task: {task}"""
        }
        
        # Test each context level
        context_results = {}
        for level_name, context_prompt in context_levels.items():
            response = self.llm.invoke(context_prompt).content
            analysis = self._analyze_length(context_prompt)
            
            # Quality indicators
            has_metrics = any(word in response.lower() for word in ['%', 'month', 'budget', 'progress'])
            has_structure = any(word in response for word in ['Status:', 'Progress:', '##', '**'])
            executive_tone = any(word in response.lower() for word in ['recommend', 'strategic', 'priority'])
            
            quality_score = sum([has_metrics, has_structure, executive_tone])
            
            context_results[level_name] = {
                "context_words": analysis["word_count"],
                "response_words": len(response.split()),
                "quality_score": f"{quality_score}/3",
                "efficiency": round(quality_score / max(analysis["word_count"] / 10, 1), 2),
                "response": response
            }
        
        # Find most efficient approach
        most_efficient = max(context_results.keys(), 
                           key=lambda k: context_results[k]["efficiency"])
        
        return {
            "technique": "Dynamic Context Hierarchy Management",
            "examples": [
                {
                    "approach": "Layered Context Optimization",
                    "problem": "Complex project context needs efficient organization for executive reporting",
                    "context_levels_tested": len(context_levels),
                    "most_efficient": most_efficient,
                    "efficiency_score": context_results[most_efficient]["efficiency"],
                    "context_reduction": f"Full: {context_results['Full_Context']['context_words']} → Optimal: {context_results[most_efficient]['context_words']} words",
                    "quality_maintained": context_results[most_efficient]["quality_score"],
                    "response": context_results[most_efficient]["response"],
                    "why_this_works": "Hierarchical context organization prioritizes essential information while keeping supplementary details accessible. This approach prevents context overflow while maintaining response quality through strategic information layering."
                }
            ]
        }


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("TECHNIQUE 15: LENGTH MANAGEMENT")
    print("="*60)
    
    length_mgmt = LengthManagement()
    results = length_mgmt.run_examples()
    return results


if __name__ == "__main__":
    main()