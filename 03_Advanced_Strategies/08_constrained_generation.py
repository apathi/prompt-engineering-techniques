"""
08: Constrained Generation (LangChain Implementation)

This module demonstrates constrained generation techniques where AI output
is guided to follow specific formats, rules, and structural requirements,
using simplified validation without complex optimization features.

Key concepts:
- Format specification and validation
- Content constraint enforcement  
- Structured output generation
- Rule-based compliance checking
- Multi-constraint satisfaction

"""

import os
import sys
from typing import List, Dict, Any

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from shared_utils.constraint_validator import ConstraintValidator, validate_output_format, create_format_prompt_suffix
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ConstrainedGeneration:
    """Constrained Generation: Format and rule-based output control using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("constrained_generation")
        self.client = LangChainClient(
            model=model,
            temperature=0.3,  # Balanced creativity with format compliance
            max_tokens=400,
            session_name="constrained_generation"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        self.validator = ConstraintValidator()
    
    def structured_format_generation(self) -> Dict[str, Any]:
        """
        Demonstrate structured format generation with validation.
        Shows intermediate-level format compliance and constraint checking.
        
        Why this works:
        Explicit format instructions combined with validation creates
        reliable structured outputs. This is essential for systems that
        need to process AI-generated content programmatically.
        """
        self.logger.info("Running structured format generation")
        
        # Task requiring structured JSON output
        task = """
        Create a product recommendation for a sustainable water bottle based on these requirements:
        - Target audience: Environmentally conscious professionals
        - Price range: $20-50
        - Key features: Insulation, durability, eco-friendly materials
        - Include pros, cons, and rating
        """
        
        # Format specifications to test
        format_specs = [
            {
                "format": "json",
                "description": "JSON with required fields",
                "required_fields": ["product_name", "price", "features", "pros", "cons", "rating"],
                "prompt_suffix": create_format_prompt_suffix("json", {"required_fields": ["product_name", "price", "features", "pros", "cons", "rating"]})
            },
            {
                "format": "bullet_list",
                "description": "Structured bullet list format",
                "prompt_suffix": create_format_prompt_suffix("bullet_list") + " Organize with clear headings."
            }
        ]
        
        results = []
        
        for spec in format_specs:
            # Create constrained prompt
            constrained_prompt = PromptTemplate.from_template(
                """Complete this task following the specified format requirements:

Task: {task}

Format Requirements: {format_requirements}

Response:"""
            )
            
            # Generate response
            chain = constrained_prompt | self.llm | self.parser
            response = chain.invoke(
                {
                    "task": task,
                    "format_requirements": spec["prompt_suffix"]
                },
                config={"tags": [f"constrained_{spec['format']}"]}
            )
            
            # Validate response
            if spec["format"] == "json":
                validation = validate_output_format(response, "json", required_fields=spec.get("required_fields"))
            else:
                validation = validate_output_format(response, spec["format"])
            
            results.append({
                "format_type": spec["format"],
                "description": spec["description"],
                "response": response,
                "validation": {
                    "is_valid": validation["is_valid"],
                    "details": validation.get("errors", validation.get("error", "Format validated successfully"))
                }
            })
        
        return {
            "technique": "Structured Format Generation",
            "examples": results,
            "task_description": task,
            "why_this_works": """Constrained format generation works because:
1. Explicit format instructions guide model output structure
2. Validation ensures compliance with specified requirements  
3. Structured formats enable reliable downstream processing
4. Clear constraints reduce ambiguity in output expectations
5. Format compliance builds trust in automated systems"""
        }
    
    def multi_constraint_compliance(self) -> Dict[str, Any]:
        """
        Demonstrate complex multi-constraint satisfaction.
        Shows advanced constraint layering with content and format rules.
        
        Why this works:
        Real-world applications often require multiple overlapping constraints.
        Layered validation ensures all requirements are met simultaneously.
        """
        self.logger.info("Running multi-constraint compliance")
        
        # Complex task with multiple constraint types
        task = """
        Write a professional email response to a client complaint about delayed delivery.
        The client ordered custom furniture 8 weeks ago with a promised 6-week delivery.
        """
        
        # Multiple constraint sets to test
        constraint_sets = [
            {
                "name": "Format + Length Constraints",
                "constraints": {
                    "format": "Professional email with Subject, Greeting, Body, Closing",
                    "max_length": 300,
                    "required_keywords": ["apologize", "solution", "compensation"]
                }
            },
            {
                "name": "Content + Tone Constraints", 
                "constraints": {
                    "format": "Email format with clear action items",
                    "required_keywords": ["acknowledge", "timeline", "follow-up"],
                    "forbidden_words": ["excuse", "blame", "unfortunately"],
                    "max_sentences": 8
                }
            }
        ]
        
        results = []
        
        for constraint_set in constraint_sets:
            constraints = constraint_set["constraints"]
            
            # Build comprehensive prompt with constraints
            constraint_prompt = PromptTemplate.from_template(
                """Write a response to this situation following ALL specified constraints:

Situation: {task}

CONSTRAINTS TO FOLLOW:
Format: {format_req}
Maximum Length: {max_length} characters (if specified)
Required Keywords: {required_keywords}
Forbidden Words: {forbidden_words} (avoid these)
Maximum Sentences: {max_sentences} (if specified)

Response:"""
            )
            
            # Generate constrained response
            chain = constraint_prompt | self.llm | self.parser
            response = chain.invoke(
                {
                    "task": task,
                    "format_req": constraints.get("format", "Standard format"),
                    "max_length": constraints.get("max_length", "No limit"),
                    "required_keywords": constraints.get("required_keywords", []),
                    "forbidden_words": constraints.get("forbidden_words", []),
                    "max_sentences": constraints.get("max_sentences", "No limit")
                },
                config={"tags": [f"multi_constraint_{constraint_set['name'].lower().replace(' ', '_')}"]}
            )
            
            # Validate against content constraints
            validation = self.validator.validate_content_constraints(response, {
                k: v for k, v in constraints.items() 
                if k in ["max_length", "min_length", "required_keywords", "forbidden_words", "max_sentences"]
            })
            
            # Check format if specified
            format_validation = {"is_valid": True, "details": "No format validation specified"}
            if "email" in constraints.get("format", "").lower():
                # Simple email format check
                has_subject = "subject:" in response.lower() or response.startswith("subject:")
                has_greeting = any(greeting in response.lower() for greeting in ["dear", "hi", "hello"])
                has_closing = any(closing in response.lower() for closing in ["sincerely", "best regards", "thank you"])
                
                email_valid = has_subject or (has_greeting and has_closing)
                format_validation = {
                    "is_valid": email_valid,
                    "details": f"Email format check: {'Valid' if email_valid else 'Missing standard email elements'}"
                }
            
            results.append({
                "constraint_set": constraint_set["name"],
                "description": f"Multi-layered constraints: {', '.join(constraints.keys())}",
                "response": response,
                "validation": {
                    "content_valid": validation["is_valid"],
                    "content_details": validation.get("violations", ["All content constraints satisfied"]),
                    "format_valid": format_validation["is_valid"],
                    "format_details": format_validation["details"]
                }
            })
        
        return {
            "technique": "Multi-Constraint Compliance",
            "examples": results,
            "task_description": task,
            "why_this_works": """Multi-constraint satisfaction works because:
1. Layered constraints ensure comprehensive requirement coverage
2. Simultaneous validation catches violations across all dimensions
3. Clear constraint specification guides model behavior effectively
4. Multiple validation passes increase output reliability
5. Constraint prioritization helps resolve conflicting requirements"""
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all constrained generation examples."""
        self.logger.info("Starting Constrained Generation demonstrations")
        
        results = {
            "technique_overview": "Constrained Generation",
            "examples": []
        }
        
        # Run example methods
        examples = [
            self.structured_format_generation(),
            self.multi_constraint_compliance()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager with folder name format
    output_manager = OutputManager("08-constrained-generation")
    output_manager.add_header("08: CONSTRAINED GENERATION - LANGCHAIN")
    
    # Initialize technique
    constrained = ConstrainedGeneration()
    
    try:
        # Run examples
        results = constrained.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(constrained.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        constrained.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()