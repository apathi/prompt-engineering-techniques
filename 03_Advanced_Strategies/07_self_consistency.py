"""
07: Self-Consistency Prompting (LangChain Implementation)

This module demonstrates self-consistency techniques where AI generates multiple
reasoning paths for the same problem and uses voting to determine the most
reliable answer, following the simplified approach without cost optimization.

Key concepts:
- Multiple reasoning path generation
- Democratic voting mechanisms
- Consistency analysis and validation
- Reliability improvement through consensus
- Confidence scoring based on agreement

"""

import os
import sys
from typing import List, Dict, Any

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from shared_utils.voting_utils import simple_majority_vote, semantic_similarity_vote, analyze_consistency
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class SelfConsistencyPrompting:
    """Self-Consistency Prompting: Multiple reasoning paths with voting using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("self_consistency")
        self.client = LangChainClient(
            model=model,
            temperature=0.7,  # Higher temperature for diverse reasoning paths
            max_tokens=400,
            session_name="self_consistency"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
    
    def multiple_reasoning_paths_analysis(self) -> Dict[str, Any]:
        """
        Demonstrate multiple reasoning paths for ambiguous problems.
        Shows intermediate-level problem solving with path diversity.
        
        Why this works:
        Self-consistency leverages the fact that correct reasoning tends to
        converge on similar answers, while errors are typically inconsistent.
        Multiple diverse paths help identify the most reliable solution.
        """
        self.logger.info("Running multiple reasoning paths analysis")
        
        # Ambiguous problem that could be interpreted multiple ways
        problem = """
        A company's profit increased by 25% in Year 1, then decreased by 20% in Year 2.
        If the profit at the end of Year 2 was $120,000, what was the original profit?
        """
        
        # Template for generating diverse reasoning paths
        reasoning_prompt = PromptTemplate.from_template(
            """Solve this problem using approach #{path_number}. Use a unique reasoning method.

Problem: {problem}

Approach {path_number} - Think about this differently than other approaches:
- If path 1: Work backwards from the final amount
- If path 2: Set up algebraic equations
- If path 3: Use step-by-step percentage calculations
- If path 4: Create a visualization or table approach

Show your reasoning and provide a clear final answer:"""
        )
        
        # Generate multiple reasoning paths (fixed at 3 for simplicity)
        paths = []
        reasoning_chain = reasoning_prompt | self.llm | self.parser
        
        for i in range(3):
            response = reasoning_chain.invoke(
                {"problem": problem, "path_number": i + 1},
                config={"tags": [f"self_consistency_path_{i+1}"]}
            )
            paths.append(response)
        
        # Analyze consistency and vote
        voting_result = semantic_similarity_vote(paths)
        consistency_analysis = analyze_consistency(paths)
        
        results = []
        
        # Show individual paths
        for i, path in enumerate(paths, 1):
            results.append({
                "path": f"Reasoning Path {i}",
                "description": f"Unique approach #{i} to the problem",
                "response": path
            })
        
        # Show voting results
        results.append({
            "path": "Voting Analysis",
            "description": "Democratic selection of most consistent answer",
            "response": f"""Winner: {voting_result['winner']}
Confidence: {voting_result['confidence']:.1%}
Vote Distribution: {voting_result['vote_counts']}
Analysis: {voting_result['analysis']}

Consistency Metrics:
{consistency_analysis['analysis']}"""
        })
        
        return {
            "technique": "Multiple Reasoning Paths Analysis", 
            "examples": results,
            "problem_statement": problem,
            "why_this_works": """Multiple reasoning paths improve reliability by:
1. Reducing the impact of single reasoning errors
2. Revealing different valid approaches to the same problem
3. Building confidence through convergent answers
4. Identifying ambiguities that need clarification
5. Leveraging wisdom-of-crowds principles for AI reasoning"""
        }
    
    def complex_decision_making_consensus(self) -> Dict[str, Any]:
        """
        Demonstrate complex decision-making with multiple perspectives.
        Shows advanced multi-criteria analysis with voting consensus.
        
        Why this works:
        Complex decisions benefit from multiple analytical perspectives.
        Self-consistency helps balance different criteria and approaches
        to reach more robust decisions.
        """
        self.logger.info("Running complex decision-making consensus")
        
        # Complex decision-making scenario
        scenario = """
        A tech startup with $500K funding must choose between three strategic options:

        Option A: Develop mobile app (6-month timeline, 70% success probability, $2M potential revenue)
        Option B: Expand to enterprise market (12-month timeline, 50% success probability, $5M potential revenue)  
        Option C: Acquire smaller competitor (3-month timeline, 80% success probability, $1M potential revenue)

        Additional constraints:
        - Company has 18 months of runway
        - Team of 8 developers (mobile-focused)
        - Two major competitors launching similar products in 9 months
        - Customer acquisition cost is rising 15% quarterly

        Which option should the startup choose and why?
        """
        
        # Different analytical perspective templates
        perspectives = [
            {
                "name": "Risk Analysis",
                "prompt": """Analyze this decision from a RISK MANAGEMENT perspective.

{scenario}

Focus on:
- Probability of failure and mitigation strategies
- Financial risk vs reward ratios
- Market timing risks
- Resource allocation risks

Risk-based recommendation:"""
            },
            {
                "name": "Financial Analysis", 
                "prompt": """Analyze this decision from a FINANCIAL OPTIMIZATION perspective.

{scenario}

Focus on:
- Expected value calculations
- Cash flow implications
- ROI and payback periods
- Funding runway considerations

Financial recommendation:"""
            },
            {
                "name": "Strategic Analysis",
                "prompt": """Analyze this decision from a STRATEGIC POSITIONING perspective.

{scenario}

Focus on:
- Competitive advantage creation
- Market positioning implications
- Long-term strategic value
- Core competency alignment

Strategic recommendation:"""
            }
        ]
        
        # Generate different analytical perspectives
        analyses = []
        for perspective in perspectives:
            perspective_prompt = PromptTemplate.from_template(perspective["prompt"])
            analysis_chain = perspective_prompt | self.llm | self.parser
            
            response = analysis_chain.invoke(
                {"scenario": scenario},
                config={"tags": [f"self_consistency_{perspective['name'].lower().replace(' ', '_')}"]}
            )
            
            analyses.append({
                "perspective": perspective["name"],
                "analysis": response
            })
        
        # Extract recommendations for voting
        recommendations = [analysis["analysis"] for analysis in analyses]
        voting_result = simple_majority_vote(recommendations)
        
        results = []
        
        # Show individual analyses
        for analysis in analyses:
            results.append({
                "perspective": analysis["perspective"],
                "description": f"Decision analysis from {analysis['perspective'].lower()} viewpoint",
                "response": analysis["analysis"]
            })
        
        # Show consensus analysis
        results.append({
            "perspective": "Consensus Decision",
            "description": "Integration of multiple analytical perspectives",
            "response": f"""Voting Results:
Most Common Recommendation: {voting_result['winner']}
Confidence Level: {voting_result['confidence']:.1%}
Agreement Analysis: {voting_result['analysis']}

Decision Rationale:
The consensus emerges from weighing multiple analytical frameworks.
Each perspective contributes unique insights that strengthen the final decision."""
        })
        
        return {
            "technique": "Complex Decision Making Consensus",
            "examples": results,
            "scenario_description": scenario,
            "why_this_works": """Multi-perspective decision making works because:
1. Different analytical frameworks reveal different aspects of the problem
2. Consensus decisions are typically more robust and defensible
3. Multiple viewpoints reduce cognitive biases in single-perspective analysis
4. Voting mechanisms balance competing criteria effectively
5. Transparency in reasoning builds confidence in final decisions"""
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all self-consistency prompting examples."""
        self.logger.info("Starting Self-Consistency demonstrations")
        
        results = {
            "technique_overview": "Self-Consistency Prompting",
            "examples": []
        }
        
        # Run example methods
        examples = [
            self.multiple_reasoning_paths_analysis(),
            self.complex_decision_making_consensus()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager with folder name format
    output_manager = OutputManager("07-self-consistency")
    output_manager.add_header("07: SELF-CONSISTENCY PROMPTING - LANGCHAIN")
    
    # Initialize technique
    self_consistency = SelfConsistencyPrompting()
    
    try:
        # Run examples
        results = self_consistency.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(self_consistency.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        self_consistency.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()