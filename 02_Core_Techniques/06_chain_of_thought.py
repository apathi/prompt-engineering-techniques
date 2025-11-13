"""
06: Chain of Thought (CoT) Prompting (LangChain Implementation)

This module demonstrates Chain of Thought prompting techniques where AI models
break down complex problems into step-by-step reasoning processes, following
the hybrid approach combining educational simplicity with advanced validation.

Key concepts:
- Step-by-step reasoning patterns
- Transparent thought processes  
- Problem decomposition strategies
- Reasoning validation and verification
- Comparative analysis of reasoning approaches

"""

import os
import sys
from typing import List, Dict, Any

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ChainOfThoughtPrompting:
    """Chain of Thought Prompting: Step-by-step reasoning with LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("chain_of_thought")
        self.client = LangChainClient(
            model=model,
            temperature=0.2,
            max_tokens=500,
            session_name="chain_of_thought"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
    
    def mathematical_reasoning_progression(self) -> Dict[str, Any]:
        """
        Demonstrate progressive mathematical reasoning with CoT.
        Shows intermediate-level multi-step problem solving.
        
        Why this works:
        CoT prompting forces the model to externalize its reasoning process,
        making errors more visible and solutions more reliable. This is
        particularly effective for multi-step mathematical problems.
        """
        self.logger.info("Running mathematical reasoning progression")
        
        # Problem: Multi-step journey with different speeds
        problem = """
        A delivery truck travels from City A to City B (120 km) at 60 km/h.
        After a 30-minute break, it continues from City B to City C (90 km) at 45 km/h.
        Then it returns directly from City C to City A (150 km) at 50 km/h.
        What is the truck's average speed for the entire journey?
        """
        
        # Standard prompt (for comparison)
        standard_prompt = PromptTemplate.from_template(
            "Solve this problem and provide the final answer:\n\n{problem}\n\nAnswer:"
        )
        
        # Chain of Thought prompt with explicit reasoning steps
        cot_prompt = PromptTemplate.from_template(
            """Solve this problem step by step. For each step:
1. State what you're calculating
2. Show the formula or method
3. Perform the calculation
4. Explain why this step is necessary

Problem: {problem}

Step-by-step solution:"""
        )
        
        # Advanced CoT with validation checks
        advanced_cot_prompt = PromptTemplate.from_template(
            """Solve this complex problem using systematic reasoning:

Problem: {problem}

Use this structured approach:

STEP 1 - PROBLEM ANALYSIS:
- Identify all given information
- Determine what needs to be calculated
- Note any special conditions

STEP 2 - SOLUTION STRATEGY:
- Break down into sub-problems
- Choose appropriate formulas
- Plan the calculation sequence

STEP 3 - DETAILED CALCULATIONS:
- Show each calculation with units
- Verify intermediate results
- Check for logical consistency

STEP 4 - VALIDATION:
- Does the answer make sense?
- Are units correct?
- Final answer with explanation

Solution:"""
        )
        
        results = []
        
        # Standard approach
        standard_chain = standard_prompt | self.llm | self.parser
        standard_response = standard_chain.invoke(
            {"problem": problem},
            config={"tags": ["cot_standard_math"]}
        )
        
        results.append({
            "approach": "Standard",
            "description": "Direct problem solving without explicit reasoning",
            "response": standard_response
        })
        
        # Basic CoT approach
        cot_chain = cot_prompt | self.llm | self.parser
        cot_response = cot_chain.invoke(
            {"problem": problem},
            config={"tags": ["cot_basic_math"]}
        )
        
        results.append({
            "approach": "Chain of Thought",
            "description": "Step-by-step reasoning with explicit calculations",
            "response": cot_response
        })
        
        # Advanced CoT with validation
        advanced_chain = advanced_cot_prompt | self.llm | self.parser
        advanced_response = advanced_chain.invoke(
            {"problem": problem},
            config={"tags": ["cot_advanced_math"]}
        )
        
        results.append({
            "approach": "Advanced CoT with Validation",
            "description": "Systematic reasoning with validation checks and structured analysis",
            "response": advanced_response
        })
        
        return {
            "technique": "Mathematical Reasoning Progression",
            "examples": results,
            "problem_statement": problem,
            "why_this_works": """CoT prompting improves mathematical reasoning by:
1. Making calculation steps explicit and verifiable
2. Reducing arithmetic errors through systematic approach
3. Enabling validation of intermediate results
4. Providing transparency for error detection and correction"""
        }
    
    def complex_logical_reasoning(self) -> Dict[str, Any]:
        """
        Demonstrate advanced logical reasoning with systematic analysis.
        Shows complex constraint satisfaction and scenario validation.
        
        Why this works:
        Complex logical problems benefit from systematic enumeration of possibilities
        and constraint checking. CoT makes this process explicit and verifiable.
        """
        self.logger.info("Running complex logical reasoning analysis")
        
        # Complex logical puzzle with multiple constraints
        puzzle = """
        Five friends (Alice, Bob, Carol, Dave, Emma) are seated around a circular table.
        Each person likes a different color (Red, Blue, Green, Yellow, Purple) and
        owns a different pet (Cat, Dog, Bird, Fish, Rabbit).

        Constraints:
        1. Alice sits directly across from the person who likes Blue
        2. The person with the Cat sits next to Bob
        3. Carol likes Green and sits two seats clockwise from Dave
        4. The person with the Dog sits directly across from Emma
        5. Dave doesn't like Red or Purple
        6. The person who likes Yellow sits next to the person with the Bird
        7. Bob doesn't have the Fish or Rabbit

        Determine who sits where, what color each person likes, and what pet each person owns.
        """
        
        # Systematic logical analysis template
        logical_reasoning_prompt = PromptTemplate.from_template(
            """Solve this complex logical puzzle using systematic constraint analysis.

Puzzle: {puzzle}

Use this methodical approach:

PHASE 1 - CONSTRAINT MAPPING:
List all constraints clearly and identify their types (position, preference, relationship)

PHASE 2 - SCENARIO GENERATION:
Generate possible arrangements systematically
Start with the most restrictive constraints

PHASE 3 - CONSTRAINT VALIDATION:
For each scenario:
- Check every constraint systematically
- Document why scenarios are eliminated
- Track which constraints are satisfied

PHASE 4 - SOLUTION VERIFICATION:
- Verify the final solution against ALL constraints
- Explain why this is the only possible solution
- Double-check for overlooked possibilities

Analysis:"""
        )
        
        # Verification template for double-checking
        verification_prompt = PromptTemplate.from_template(
            """Verify this logical reasoning solution by checking each constraint:

Original Puzzle: {puzzle}

Proposed Solution: {solution}

VERIFICATION CHECKLIST:
Go through each constraint one by one and verify it's satisfied.
If any constraint is violated, explain the error.
If all constraints are satisfied, confirm the solution is correct.

Verification Result:"""
        )
        
        # Generate initial solution
        logical_chain = logical_reasoning_prompt | self.llm | self.parser
        solution = logical_chain.invoke(
            {"puzzle": puzzle},
            config={"tags": ["cot_logical_puzzle"]}
        )
        
        # Verify the solution
        verify_chain = verification_prompt | self.llm | self.parser
        verification = verify_chain.invoke(
            {"puzzle": puzzle, "solution": solution[:1000]},
            config={"tags": ["cot_solution_verification"]}
        )
        
        results = [
            {
                "stage": "Initial Systematic Analysis",
                "description": "Step-by-step constraint analysis and scenario generation",
                "response": solution
            },
            {
                "stage": "Solution Verification",
                "description": "Independent verification of proposed solution against all constraints",
                "response": verification
            }
        ]
        
        return {
            "technique": "Complex Logical Reasoning",
            "examples": results,
            "puzzle_statement": puzzle,
            "why_this_works": """Complex logical reasoning benefits from CoT because:
1. Systematic constraint enumeration prevents overlooked conditions
2. Explicit scenario generation ensures comprehensive coverage
3. Step-by-step validation makes errors detectable
4. Verification phase catches logical inconsistencies
5. Transparent reasoning allows for error correction and learning"""
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all Chain of Thought prompting examples."""
        self.logger.info("Starting Chain of Thought demonstrations")
        
        results = {
            "technique_overview": "Chain of Thought Prompting",
            "examples": []
        }
        
        # Run example methods
        examples = [
            self.mathematical_reasoning_progression(),
            self.complex_logical_reasoning()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager with folder name format
    output_manager = OutputManager("06-chain-of-thought")
    output_manager.add_header("06: CHAIN OF THOUGHT PROMPTING - LANGCHAIN")
    
    # Initialize technique
    cot = ChainOfThoughtPrompting()
    
    try:
        # Run examples
        results = cot.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(cot.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        cot.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()