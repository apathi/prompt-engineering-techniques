"""
01: Introduction to Prompt Engineering (LangChain Implementation)

This module demonstrates fundamental prompt engineering concepts using LangChain:
- Basic prompt structures and clarity
- Structured prompt templates
- Comparative prompt analysis
- Fact-checking patterns
- Problem-solving approaches

"""

import os
import sys
from typing import List, Dict, Any

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class IntroPromptEngineering:
    """Introduction to Prompt Engineering techniques using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("intro_prompt_engineering")
        self.client = LangChainClient(
            model=model,
            temperature=0.2,
            max_tokens=500,
            session_name="intro_prompt_engineering"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        
    def basic_prompt_structure(self) -> Dict[str, Any]:
        """
        Demonstrate basic prompt structure principles.
        Shows the importance of clear, specific language.
        """
        self.logger.info("Running basic prompt structure examples")
        
        # Demonstrate progression from vague to clear to structured
        prompts = [
            {
                "clarity": "vague",
                "prompt": "Explain prompt engineering",
                "description": "Minimal context, unclear expectations"
            },
            {
                "clarity": "clear",
                "prompt": "Explain the concept of prompt engineering in one clear sentence.",
                "description": "Specific format and length requirements"
            },
            {
                "clarity": "structured",
                "prompt": "Define prompt engineering and explain why it's important for AI applications.",
                "description": "Clear task structure with multiple components"
            }
        ]
        
        results = []
        for prompt_info in prompts:
            # Create simple prompt template
            prompt_template = ChatPromptTemplate.from_template("{input}")
            chain = prompt_template | self.llm | self.parser
            
            # Invoke with tags for cost tracking
            response = chain.invoke(
                {"input": prompt_info["prompt"]},
                config={"tags": [f"intro_clarity_{prompt_info['clarity']}"]}
            )
            
            results.append({
                "clarity_level": prompt_info["clarity"],
                "prompt": prompt_info["prompt"],
                "description": prompt_info["description"],
                "response": response
            })
        
        return {"technique": "Basic Prompt Structure", "examples": results}
    
    def template_structure_comparison(self) -> Dict[str, Any]:
        """
        Compare different template structures for the same task.
        Shows how structure affects response quality.
        """
        self.logger.info("Running template structure comparison")
        
        task = "summarizing a technical article"
        
        templates = [
            {
                "type": "minimal",
                "template": "Summarize this: {article}",
                "structure": "Single instruction, no constraints"
            },
            {
                "type": "guided",
                "template": """Article: {article}
                
Task: Provide a summary that includes:
1. Main topic
2. Key findings
3. Conclusion""",
                "structure": "Structured with specific requirements"
            },
            {
                "type": "constrained",
                "template": """Article: {article}

Generate a 3-sentence summary where:
- Sentence 1: States the main topic
- Sentence 2: Highlights the key finding
- Sentence 3: Presents the conclusion or implication""",
                "structure": "Highly constrained format"
            }
        ]
        
        # Sample article for testing
        test_article = """
        Recent advances in prompt engineering have shown that structured prompts
        significantly improve AI response quality. Researchers found that adding
        clear constraints and format specifications can increase accuracy by 40%.
        This suggests that prompt design is crucial for effective AI applications.
        """
        
        results = []
        for template_info in templates:
            prompt = PromptTemplate.from_template(template_info["template"])
            chain = prompt | self.llm | self.parser
            
            response = chain.invoke(
                {"article": test_article},
                config={"tags": [f"intro_template_{template_info['type']}"]}
            )
            
            results.append({
                "template_type": template_info["type"],
                "structure": template_info["structure"],
                "response": response
            })
        
        return {"technique": "Template Structure Comparison", "examples": results}
    
    def fact_checking_patterns(self) -> Dict[str, Any]:
        """
        Demonstrate fact-checking prompt patterns.
        Shows how to structure prompts for verification tasks.
        """
        self.logger.info("Running fact-checking patterns")
        
        patterns = [
            {
                "pattern": "direct_verification",
                "prompt": ChatPromptTemplate.from_template(
                    "Is this statement true or false? Explain briefly.\n"
                    "Statement: {statement}"
                ),
                "example": "The Earth orbits around the Sun in exactly 365 days."
            },
            {
                "pattern": "source_request",
                "prompt": ChatPromptTemplate.from_template(
                    "Verify this claim and indicate what sources would be needed to confirm it:\n"
                    "{statement}"
                ),
                "example": "Python is the most popular programming language in 2024."
            },
            {
                "pattern": "confidence_rating",
                "prompt": ChatPromptTemplate.from_template(
                    "Evaluate this statement:\n{statement}\n\n"
                    "Provide:\n"
                    "1. True/False/Partially True\n"
                    "2. Confidence level (0-100%)\n"
                    "3. Brief explanation"
                ),
                "example": "Machine learning models always require large datasets to be effective."
            }
        ]
        
        results = []
        for pattern_info in patterns:
            chain = pattern_info["prompt"] | self.llm | self.parser
            
            response = chain.invoke(
                {"statement": pattern_info["example"]},
                config={"tags": [f"intro_fact_{pattern_info['pattern']}"]}
            )
            
            results.append({
                "pattern": pattern_info["pattern"],
                "statement": pattern_info["example"],
                "response": response
            })
        
        return {"technique": "Fact-Checking Patterns", "examples": results}
    
    def problem_solving_approaches(self) -> Dict[str, Any]:
        """
        Demonstrate different problem-solving prompt approaches.
        Shows various strategies for complex tasks.
        """
        self.logger.info("Running problem-solving approaches")
        
        problem = "How can a small business increase customer retention?"
        
        approaches = [
            {
                "approach": "direct_solution",
                "prompt": ChatPromptTemplate.from_template(
                    "Problem: {problem}\nProvide a solution."
                )
            },
            {
                "approach": "step_by_step",
                "prompt": ChatPromptTemplate.from_template(
                    "Problem: {problem}\n\n"
                    "Break down the solution into clear steps:\n"
                    "1. First, identify...\n"
                    "2. Then, implement...\n"
                    "3. Finally, measure..."
                )
            },
            {
                "approach": "analytical",
                "prompt": ChatPromptTemplate.from_template(
                    "Problem: {problem}\n\n"
                    "Provide:\n"
                    "- Root cause analysis\n"
                    "- Top 3 solutions\n"
                    "- Implementation priority"
                )
            },
            {
                "approach": "pros_cons",
                "prompt": ChatPromptTemplate.from_template(
                    "Problem: {problem}\n\n"
                    "For each potential solution, list:\n"
                    "- The approach\n"
                    "- Pros\n"
                    "- Cons\n"
                    "- Recommendation"
                )
            }
        ]
        
        results = []
        for approach_info in approaches:
            chain = approach_info["prompt"] | self.llm | self.parser
            
            response = chain.invoke(
                {"problem": problem},
                config={"tags": [f"intro_problem_{approach_info['approach']}"]}
            )
            
            results.append({
                "approach": approach_info["approach"],
                "problem": problem,
                "response": response
            })
        
        return {"technique": "Problem-Solving Approaches", "examples": results}
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all introduction to prompt engineering examples."""
        self.logger.info("Starting Introduction to Prompt Engineering demonstrations")
        
        results = {
            "technique_overview": "Introduction to Prompt Engineering",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.basic_prompt_structure(),
            self.template_structure_comparison(),
            self.fact_checking_patterns(),
            self.problem_solving_approaches()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("intro-prompt-engineering")
    output_manager.add_header("01: INTRODUCTION TO PROMPT ENGINEERING - LANGCHAIN")
    
    # Initialize technique
    intro = IntroPromptEngineering()
    
    try:
        # Run examples
        results = intro.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(intro.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        intro.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()