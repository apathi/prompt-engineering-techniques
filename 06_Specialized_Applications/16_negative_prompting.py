"""
16: Negative Prompting and Avoiding Undesired Outputs (LangChain Implementation)

This module demonstrates negative prompting techniques to guide AI outputs by
explicitly specifying what should NOT be included, following advanced constraint
validation and systematic exclusion patterns.

Key concepts:
- Multi-layer constraint validation
- Systematic exclusion pattern engines
- Output filtering and violation detection
- Constraint refinement and optimization
- Advanced negative prompting strategies

"""

import os
import sys
from typing import List, Dict, Any, Optional
import re
from dataclasses import dataclass

# Add shared_utils to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


@dataclass
class ConstraintViolation:
    """Represents a constraint violation in generated content."""
    constraint_type: str
    violation_text: str
    severity: str
    suggestion: str


class ConstraintValidator:
    """Advanced constraint validation and exclusion pattern engine."""
    
    def __init__(self):
        self.constraint_patterns = {
            "forbidden_words": [],
            "forbidden_phrases": [],
            "style_constraints": [],
            "content_constraints": [],
            "format_constraints": []
        }
    
    def add_constraint(self, constraint_type: str, pattern: str, severity: str = "medium"):
        """Add a constraint pattern."""
        if constraint_type not in self.constraint_patterns:
            self.constraint_patterns[constraint_type] = []
        
        self.constraint_patterns[constraint_type].append({
            "pattern": pattern,
            "severity": severity
        })
    
    def validate_output(self, text: str) -> List[ConstraintViolation]:
        """Validate text against all constraints."""
        violations = []
        
        # Check forbidden words
        for constraint in self.constraint_patterns.get("forbidden_words", []):
            pattern = constraint["pattern"]
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(ConstraintViolation(
                    constraint_type="forbidden_words",
                    violation_text=pattern,
                    severity=constraint["severity"],
                    suggestion=f"Remove or replace instances of '{pattern}'"
                ))
        
        # Check forbidden phrases
        for constraint in self.constraint_patterns.get("forbidden_phrases", []):
            pattern = constraint["pattern"]
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(ConstraintViolation(
                    constraint_type="forbidden_phrases",
                    violation_text=pattern,
                    severity=constraint["severity"],
                    suggestion=f"Rewrite to avoid '{pattern}'"
                ))
        
        return violations
    
    def get_violation_score(self, violations: List[ConstraintViolation]) -> float:
        """Calculate a score based on constraint violations."""
        if not violations:
            return 1.0
        
        severity_weights = {"low": 0.1, "medium": 0.3, "high": 0.6}
        total_penalty = sum(severity_weights.get(v.severity, 0.3) for v in violations)
        return max(0.0, 1.0 - (total_penalty / len(violations)))


class NegativePrompting:
    """Negative Prompting: Guiding outputs by specifying exclusions using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("negative_prompting")
        self.client = LangChainClient(
            model=model,
            temperature=0.3,
            max_tokens=500,
            session_name="negative_prompting"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        self.validator = ConstraintValidator()
    
    def basic_negative_constraints(self) -> Dict[str, Any]:
        """
        Demonstrate intermediate negative constraint techniques.
        Shows systematic exclusion patterns with validation.
        """
        self.logger.info("Running basic negative constraints examples")
        
        # Set up constraint validator
        validator = ConstraintValidator()
        validator.add_constraint("forbidden_words", r"\btechnical jargon\b", "medium")
        validator.add_constraint("forbidden_words", r"\bcomplex\b", "low")
        validator.add_constraint("forbidden_phrases", r"historically speaking", "high")
        validator.add_constraint("content_constraints", r"comparison.*other", "medium")
        
        examples = [
            {
                "topic": "Artificial Intelligence",
                "constraints": [
                    "No technical jargon or complex terminology",
                    "No historical background or dates", 
                    "No comparisons to other technologies",
                    "Keep under 150 words",
                    "Focus only on current practical applications"
                ]
            },
            {
                "topic": "Climate Change",
                "constraints": [
                    "No political opinions or blame assignment",
                    "No catastrophic language or fear-mongering",
                    "No specific country examples",
                    "Keep scientific and objective",
                    "Focus on actionable solutions"
                ]
            },
            {
                "topic": "Cryptocurrency", 
                "constraints": [
                    "No investment advice or financial recommendations",
                    "No price predictions or market speculation",
                    "No promotion of specific coins or platforms",
                    "Explain concepts only, not opportunities",
                    "Keep neutral and educational"
                ]
            }
        ]
        
        results = []
        for example in examples:
            # Create negative constraint prompt
            constraint_list = "\n".join([f"- {constraint}" for constraint in example["constraints"]])
            
            prompt = ChatPromptTemplate.from_template(
                """Provide a clear explanation of {topic}.

STRICT CONSTRAINTS - DO NOT include any of the following:
{constraints}

Your explanation should be simple, direct, and focus only on the core concept with practical relevance.

Topic: {topic}

Explanation:"""
            )
            
            chain = prompt | self.llm | self.parser
            response = chain.invoke(
                {
                    "topic": example["topic"],
                    "constraints": constraint_list
                },
                config={"tags": [f"basic_negative_{example['topic'].lower().replace(' ', '_')}"]}
            )
            
            # Validate against constraints
            violations = validator.validate_output(response)
            compliance_score = validator.get_violation_score(violations)
            
            results.append({
                "topic": example["topic"],
                "constraints": example["constraints"],
                "response": response,
                "violations": [{"type": v.constraint_type, "text": v.violation_text, "severity": v.severity} for v in violations],
                "compliance_score": compliance_score
            })
        
        return {
            "technique": "Basic Negative Constraints",
            "description": "Uses explicit exclusion lists to guide model behavior away from undesired content",
            "why_this_works": "By clearly specifying what NOT to include, we create boundaries that help the model focus on desired content while avoiding problematic areas. The constraint validation provides measurable compliance.",
            "examples": results
        }
    
    def advanced_constraint_layering(self) -> Dict[str, Any]:
        """
        Demonstrate advanced multi-dimensional constraint validation.
        Shows sophisticated exclusion engines with refinement loops.
        """
        self.logger.info("Running advanced constraint layering examples")
        
        # Advanced constraint scenarios
        scenarios = [
            {
                "task": "Business Email Communication",
                "context": "Write a professional email declining a business proposal",
                "multi_constraints": {
                    "tone": ["Do not be rude, dismissive, or unprofessional", "Avoid overly casual language"],
                    "content": ["Do not provide detailed reasons for rejection", "Avoid mentioning competitors"],
                    "structure": ["Do not exceed 100 words", "Do not include attachments or links"],
                    "legal": ["Do not make binding commitments", "Avoid discriminatory language"]
                }
            },
            {
                "task": "Medical Information Summary",
                "context": "Explain common symptoms of seasonal allergies",
                "multi_constraints": {
                    "medical": ["Do not provide specific medical advice", "Avoid suggesting specific medications"],
                    "liability": ["Do not replace professional medical consultation", "Avoid definitive diagnostic language"],
                    "content": ["Do not include rare or severe complications", "Avoid medical jargon"],
                    "scope": ["Focus only on seasonal allergies", "Do not discuss food allergies"]
                }
            }
        ]
        
        results = []
        for scenario in scenarios:
            # Build advanced constraint prompt
            constraint_sections = []
            for category, constraints in scenario["multi_constraints"].items():
                constraint_text = "\n".join([f"  • {constraint}" for constraint in constraints])
                constraint_sections.append(f"{category.upper()} CONSTRAINTS:\n{constraint_text}")
            
            full_constraints = "\n\n".join(constraint_sections)
            
            prompt = ChatPromptTemplate.from_template(
                """Task: {task}
Context: {context}

MULTI-LAYER CONSTRAINT FRAMEWORK:
{constraints}

CRITICAL: Violating any constraint will result in response rejection. Focus on providing helpful information while strictly adhering to all constraint categories.

Response:"""
            )
            
            chain = prompt | self.llm | self.parser
            
            # First attempt
            response = chain.invoke(
                {
                    "task": scenario["task"],
                    "context": scenario["context"], 
                    "constraints": full_constraints
                },
                config={"tags": [f"advanced_constraint_{scenario['task'].lower().replace(' ', '_')}"]}
            )
            
            # Advanced validation with category-specific checking
            category_violations = {}
            total_compliance = 1.0
            
            for category, constraints in scenario["multi_constraints"].items():
                category_validator = ConstraintValidator()
                for constraint in constraints:
                    # Extract key prohibition words for validation
                    if "not" in constraint.lower():
                        prohibited_terms = self._extract_prohibited_terms(constraint)
                        for term in prohibited_terms:
                            category_validator.add_constraint("forbidden_phrases", term, "high")
                
                violations = category_validator.validate_output(response)
                category_score = category_validator.get_violation_score(violations)
                category_violations[category] = {
                    "violations": violations,
                    "score": category_score
                }
                total_compliance *= category_score
            
            results.append({
                "task": scenario["task"],
                "context": scenario["context"],
                "constraint_categories": list(scenario["multi_constraints"].keys()),
                "response": response,
                "category_compliance": {k: v["score"] for k, v in category_violations.items()},
                "overall_compliance": total_compliance,
                "word_count": len(response.split())
            })
        
        return {
            "technique": "Advanced Constraint Layering",
            "description": "Multi-dimensional constraint validation with category-specific compliance scoring",
            "why_this_works": "Layered constraints create a comprehensive framework that addresses different risk categories simultaneously. This prevents single-point failures and ensures holistic compliance across multiple dimensions of content quality and safety.",
            "examples": results
        }
    
    def _extract_prohibited_terms(self, constraint: str) -> List[str]:
        """Extract key terms that should be avoided from constraint text."""
        # Simple extraction - in production, this would be more sophisticated
        prohibited = []
        constraint_lower = constraint.lower()
        
        # Extract terms after "not" and "avoid"
        import re
        not_patterns = re.findall(r"(?:do not|avoid|not)[\s\w]*?([\w\s]{3,20})(?:,|\.|\b)", constraint_lower)
        for match in not_patterns:
            clean_term = match.strip()
            if len(clean_term) > 2 and clean_term not in ["provide", "include", "mention"]:
                prohibited.append(clean_term)
        
        return prohibited
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all negative prompting examples."""
        self.logger.info("Starting Negative Prompting demonstrations")
        
        results = {
            "technique_overview": "Negative Prompting and Avoiding Undesired Outputs",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.basic_negative_constraints(),
            self.advanced_constraint_layering()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("16-negative-prompting")
    output_manager.add_header("16: NEGATIVE PROMPTING - AVOIDING UNDESIRED OUTPUTS")
    
    # Initialize technique
    negative_prompting = NegativePrompting()
    
    try:
        # Run examples
        results = negative_prompting.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(negative_prompting.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        negative_prompting.logger.error(f"Exebut dontcution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()