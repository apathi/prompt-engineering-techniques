#!/usr/bin/env python3
"""
Technique 12: Instruction Engineering - Clear, Precise Communication

Demonstrates systematic instruction crafting to maximize alignment between
user intent and model output through clarity validation and refinement.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, OutputManager
from typing import Dict, List, Any
import re


class InstructionEngineering:
    """Clean instruction engineering with clarity validation."""
    
    def __init__(self):
        self.client = LangChainClient()
        self.llm = self.client.get_llm()
        self.output_manager = OutputManager("12-instruction-engineering")
    
    def run_examples(self):
        """Execute two progressive examples."""
        
        self.output_manager.add_header("TECHNIQUE 12: INSTRUCTION ENGINEERING")
        self.output_manager.add_line("Clear, precise instructions for maximum alignment")
        self.output_manager.add_line()
        
        results = {
            "examples": [
                self._example_1_instruction_refinement(),
                self._example_2_advanced_validation()
            ]
        }
        
        self.output_manager.display_results(results)
        
        # Add final cost summary
        self.client.print_cost_summary()
        
        self.output_manager.save_to_file()
        return results
    
    def _example_1_instruction_refinement(self):
        """Example 1: Business Documentation - Instruction Quality Scoring"""
        
        # Poor instruction vs refined instruction
        poor_instruction = "Write something about quarterly planning."
        
        refined_instruction = """Write a 300-word business memo about Q4 planning priorities.
        
Structure:
- Executive summary (1 paragraph)
- 3 key priorities with rationale
- Resource requirements
- Success metrics

Tone: Professional, action-oriented
Audience: Department heads"""
        
        # Test both instructions
        poor_response = self.llm.invoke(poor_instruction).content
        refined_response = self.llm.invoke(refined_instruction).content
        
        # Simple clarity scoring
        def score_clarity(instruction: str) -> Dict[str, Any]:
            score = 0
            feedback = []
            
            # Length specificity
            if any(word in instruction.lower() for word in ['word', 'paragraph', 'sentence']):
                score += 2
                feedback.append("✓ Length specified")
            
            # Structure guidance
            if any(word in instruction.lower() for word in ['structure', 'format', 'sections']):
                score += 2
                feedback.append("✓ Structure provided")
            
            # Audience clarity
            if any(word in instruction.lower() for word in ['audience', 'for', 'tone']):
                score += 2
                feedback.append("✓ Audience/tone specified")
            
            # Specificity
            if len(instruction.split()) > 20:
                score += 2
                feedback.append("✓ Detailed instruction")
            
            return {"score": min(score, 8), "feedback": feedback}
        
        poor_score = score_clarity(poor_instruction)
        refined_score = score_clarity(refined_instruction)
        
        return {
            "technique": "Instruction Refinement with Quality Scoring",
            "examples": [
                {
                    "approach": "Poor vs Refined Instruction Comparison",
                    "problem": "Vague business documentation request needs clarity",
                    "poor_instruction": poor_instruction,
                    "poor_score": f"{poor_score['score']}/8",
                    "poor_feedback": " | ".join(poor_score['feedback']) or "No positive elements",
                    "refined_instruction": refined_instruction,
                    "refined_score": f"{refined_score['score']}/8", 
                    "refined_feedback": " | ".join(refined_score['feedback']),
                    "response": refined_response,
                    "why_this_works": "Clear instructions eliminate ambiguity. Specific length, structure, tone, and audience requirements ensure consistent, targeted output. Quality scoring helps identify instruction weaknesses systematically."
                }
            ]
        }
    
    def _example_2_advanced_validation(self):
        """Example 2: Multi-Constraint Instruction with Validation Framework"""
        
        # Complex instruction with multiple constraints
        complex_instruction = """Analyze this customer feedback and provide actionable insights.

Constraints:
- Exactly 3 insights maximum
- Each insight: problem + solution + priority (High/Medium/Low)
- Response format: JSON only
- Include confidence score (0.0-1.0) for each insight
- Total word count under 150 words

Customer feedback: "The app crashes when uploading large files. The UI is confusing for new users. Loading times are terrible on mobile. Support takes forever to respond. But I love the core features when it works."""
        
        response = self.llm.invoke(complex_instruction).content
        
        # Advanced validation framework
        def validate_response(response: str, instruction: str) -> Dict[str, Any]:
            validations = {}
            
            # JSON format validation
            try:
                import json
                json.loads(response.strip())
                validations["json_format"] = "✓ Valid JSON"
            except:
                validations["json_format"] = "✗ Invalid JSON"
            
            # Word count validation
            word_count = len(response.split())
            if word_count <= 150:
                validations["word_count"] = f"✓ {word_count}/150 words"
            else:
                validations["word_count"] = f"✗ {word_count}/150 words (exceeded)"
            
            # Insight count validation
            insight_count = response.lower().count('insight') + response.lower().count('problem')
            if insight_count <= 6:  # 3 insights max, looking for problem/solution pairs
                validations["insight_count"] = "✓ Within limits"
            else:
                validations["insight_count"] = "✗ Too many insights"
            
            # Priority validation
            priority_count = sum([
                response.lower().count('high'),
                response.lower().count('medium'), 
                response.lower().count('low')
            ])
            if priority_count >= 3:
                validations["priority_labels"] = "✓ Priorities included"
            else:
                validations["priority_labels"] = "✗ Missing priorities"
            
            # Confidence score validation
            confidence_patterns = ['confidence', 'score', '0.', '1.0']
            has_confidence = any(pattern in response.lower() for pattern in confidence_patterns)
            validations["confidence_scores"] = "✓ Confidence included" if has_confidence else "✗ No confidence scores"
            
            passed = sum(1 for v in validations.values() if v.startswith("✓"))
            total = len(validations)
            
            return {
                "validation_score": f"{passed}/{total}",
                "details": validations,
                "compliance_rate": f"{(passed/total)*100:.0f}%"
            }
        
        validation_results = validate_response(response, complex_instruction)
        
        return {
            "technique": "Advanced Multi-Constraint Validation",
            "examples": [
                {
                    "approach": "Complex Business Analysis with Validation",
                    "problem": "Customer feedback analysis with multiple format and content constraints",
                    "instruction_complexity": "5 constraints: format, count, structure, scoring, length",
                    "validation_score": validation_results["validation_score"],
                    "compliance_rate": validation_results["compliance_rate"],
                    "validation_details": str(validation_results["details"]),
                    "response": response,
                    "why_this_works": "Multi-constraint instructions ensure precise output format and content. Systematic validation confirms compliance with all requirements. This approach scales to complex business scenarios requiring specific deliverables with measurable quality standards."
                }
            ]
        }


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("TECHNIQUE 12: INSTRUCTION ENGINEERING")
    print("="*60)
    
    engineering = InstructionEngineering()
    results = engineering.run_examples()
    return results


if __name__ == "__main__":
    main()