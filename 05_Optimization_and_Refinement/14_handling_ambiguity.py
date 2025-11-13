#!/usr/bin/env python3
"""
Technique 14: Handling Ambiguity - Context-Aware Resolution

Demonstrates systematic ambiguity detection and resolution through
context clarification and precision enhancement techniques.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, OutputManager
from typing import Dict, List, Any


class HandlingAmbiguity:
    """Clean ambiguity detection and resolution."""
    
    def __init__(self):
        self.client = LangChainClient()
        self.llm = self.client.get_llm()
        self.output_manager = OutputManager("14-handling-ambiguity")
    
    def run_examples(self):
        """Execute two progressive examples."""
        
        self.output_manager.add_header("TECHNIQUE 14: HANDLING AMBIGUITY")
        self.output_manager.add_line("Context-aware ambiguity detection and resolution")
        self.output_manager.add_line()
        
        results = {
            "examples": [
                self._example_1_context_disambiguation(),
                self._example_2_systematic_clarification()
            ]
        }
        
        self.output_manager.display_results(results)
        
        # Add final cost summary
        self.client.print_cost_summary()
        
        self.output_manager.save_to_file()
        return results
    
    def _detect_ambiguity(self, text: str) -> Dict[str, Any]:
        """Simple ambiguity detection."""
        ambiguous_words = ['bank', 'bat', 'bark', 'fair', 'light', 'spring', 'table', 'charge']
        vague_words = ['something', 'things', 'stuff', 'good', 'bad', 'nice', 'better']
        
        found_ambiguous = [word for word in ambiguous_words if word in text.lower()]
        found_vague = [word for word in vague_words if word in text.lower()]
        
        ambiguity_score = len(found_ambiguous) + len(found_vague)
        
        return {
            "ambiguity_score": ambiguity_score,
            "ambiguous_terms": found_ambiguous,
            "vague_terms": found_vague,
            "needs_clarification": ambiguity_score > 0
        }
    
    def _resolve_with_context(self, prompt: str, context: str) -> str:
        """Resolve ambiguity by adding context."""
        clarified_prompt = f"{context}\n\nBased on this context: {prompt}"
        return self.llm.invoke(clarified_prompt).content
    
    def _example_1_context_disambiguation(self):
        """Example 1: Multi-Context Resolution"""
        
        # Ambiguous prompt
        ambiguous_prompt = "Tell me about the bank."
        
        # Different contexts
        contexts = {
            "Financial": "You are a financial advisor discussing banking services and investments.",
            "Geographic": "You are a geographer explaining river formations and landscape features.",
            "Data": "You are a data scientist discussing data storage and information repositories."
        }
        
        # Test without context first
        no_context_response = self.llm.invoke(ambiguous_prompt).content
        ambiguity_analysis = self._detect_ambiguity(ambiguous_prompt)
        
        # Test with each context
        context_responses = {}
        for context_name, context in contexts.items():
            context_responses[context_name] = self._resolve_with_context(ambiguous_prompt, context)
        
        return {
            "technique": "Multi-Context Disambiguation",
            "examples": [
                {
                    "approach": "Context-Driven Ambiguity Resolution",
                    "problem": "Ambiguous term 'bank' requires context specification",
                    "ambiguous_prompt": ambiguous_prompt,
                    "ambiguity_score": ambiguity_analysis["ambiguity_score"],
                    "ambiguous_terms": str(ambiguity_analysis["ambiguous_terms"]),
                    "contexts_tested": len(contexts),
                    "no_context_response": no_context_response,
                    "financial_context": context_responses["Financial"],
                    "geographic_context": context_responses["Geographic"],
                    "response": context_responses["Financial"],
                    "why_this_works": "Context injection eliminates ambiguity by providing domain-specific framing. Different contexts produce dramatically different but appropriate responses, demonstrating systematic disambiguation."
                }
            ]
        }
    
    def _example_2_systematic_clarification(self):
        """Example 2: Advanced Clarification Framework"""
        
        # Complex ambiguous request
        vague_request = "Make it better and add some good stuff to improve things."
        
        # Systematic clarification process
        clarification_steps = [
            {
                "step": "Identify_Vagueness",
                "prompt": f"What specific information is missing from this request to make it actionable? '{vague_request}'"
            },
            {
                "step": "Request_Specifics", 
                "prompt": f"Rewrite this vague request as 3 specific, actionable questions: '{vague_request}'"
            },
            {
                "step": "Provide_Framework",
                "prompt": f"""Transform this vague request into a clear specification:

Original: "{vague_request}"

Framework:
- What exactly needs improvement?
- What specific enhancements are needed?
- What are the success criteria?
- What constraints apply?

Clarified request:"""
            }
        ]
        
        # Execute clarification pipeline
        step_results = []
        for step in clarification_steps:
            response = self.llm.invoke(step["prompt"]).content
            
            # Simple clarity scoring
            clarity_indicators = ['specific', 'exactly', 'measurable', 'criteria', 'constraint']
            clarity_score = sum(1 for indicator in clarity_indicators if indicator in response.lower())
            
            step_results.append({
                "step": step["step"],
                "clarity_score": f"{clarity_score}/5",
                "response": response
            })
        
        # Final clarified request
        final_response = step_results[-1]["response"]
        initial_ambiguity = self._detect_ambiguity(vague_request)
        
        return {
            "technique": "Systematic Clarification Framework",
            "examples": [
                {
                    "approach": "Multi-Step Ambiguity Resolution Pipeline",
                    "problem": "Extremely vague request needs systematic clarification",
                    "original_request": vague_request,
                    "initial_vague_terms": str(initial_ambiguity["vague_terms"]),
                    "clarification_steps": len(clarification_steps),
                    "final_clarity": step_results[-1]["clarity_score"],
                    "pipeline_stages": " → ".join([r["step"] for r in step_results]),
                    "response": final_response,
                    "why_this_works": "Systematic clarification breaks down vague requests into specific, actionable components. Multi-step refinement ensures comprehensive disambiguation while maintaining user intent."
                }
            ]
        }


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("TECHNIQUE 14: HANDLING AMBIGUITY")
    print("="*60)
    
    ambiguity = HandlingAmbiguity()
    results = ambiguity.run_examples()
    return results


if __name__ == "__main__":
    main()