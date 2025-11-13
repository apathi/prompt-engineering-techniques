"""
03: Prompt Templates and Variables (LangChain Implementation)

This module demonstrates advanced prompt templating using LangChain's ChatPromptTemplate
for creating reusable, flexible prompt structures with dynamic variable substitution.

Key concepts:
- Variable substitution with {variable}
- Conditional logic through dynamic template selection
- List processing and iteration
- Complex multi-variable scenarios
- Template reusability patterns

"""

import os
import sys
from typing import List, Dict, Any, Optional

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class PromptTemplatesVariables:
    """Prompt Templates and Variables: Advanced templating patterns with LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("prompt_templates_variables")
        self.client = LangChainClient(
            model=model,
            temperature=0.2,
            max_tokens=400,
            session_name="prompt_templates_variables"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
    
    def basic_variable_substitution(self) -> Dict[str, Any]:
        """
        Demonstrate basic variable substitution following original Jinja2 pattern.
        Shows simple to complex variable usage.
        """
        self.logger.info("Running basic variable substitution examples")
        
        # Simple template with one variable (like original)
        simple_template = PromptTemplate.from_template(
            "Provide a brief explanation of {topic}."
        )
        
        # Complex template with multiple variables (like original)
        complex_template = PromptTemplate.from_template(
            "Explain the concept of {concept} in the field of {field} "
            "to a {audience} audience, concisely."
        )
        
        results = []
        
        # Test simple template
        simple_chain = simple_template | self.llm | self.parser
        simple_response = simple_chain.invoke(
            {"topic": "photosynthesis"},
            config={"tags": ["simple_template"]}
        )
        results.append({
            "type": "simple",
            "template": "Single variable template",
            "variables": {"topic": "photosynthesis"},
            "response": simple_response
        })
        
        # Test complex template
        complex_chain = complex_template | self.llm | self.parser
        complex_response = complex_chain.invoke(
            {
                "concept": "neural networks",
                "field": "artificial intelligence",
                "audience": "beginner"
            },
            config={"tags": ["complex_template"]}
        )
        results.append({
            "type": "complex",
            "template": "Multiple variable template",
            "variables": {
                "concept": "neural networks",
                "field": "artificial intelligence",
                "audience": "beginner"
            },
            "response": complex_response
        })
        
        return {"technique": "Basic Variable Substitution", "examples": results}
    
    def conditional_templates(self) -> Dict[str, Any]:
        """
        Demonstrate conditional logic in templates.
        Since LangChain doesn't support Jinja2 conditionals directly,
        we use dynamic template selection (following original's intent).
        """
        self.logger.info("Running conditional template examples")
        
        def get_career_advice_template(has_profession: bool) -> PromptTemplate:
            """Dynamic template selection based on condition."""
            if has_profession:
                return PromptTemplate.from_template(
                    "My name is {name} and I am {age} years old. "
                    "I work as a {profession}. "
                    "Can you give me career advice based on this information? Answer concisely."
                )
            else:
                return PromptTemplate.from_template(
                    "My name is {name} and I am {age} years old. "
                    "I am currently not employed. "
                    "Can you give me career advice based on this information? Answer concisely."
                )
        
        results = []
        
        # Test with profession (like original)
        template_with_prof = get_career_advice_template(has_profession=True)
        chain_with_prof = template_with_prof | self.llm | self.parser
        response_with_prof = chain_with_prof.invoke(
            {
                "name": "Alex",
                "age": "28",
                "profession": "software developer"
            },
            config={"tags": ["conditional_with_profession"]}
        )
        results.append({
            "condition": "with_profession",
            "input": {"name": "Alex", "age": "28", "profession": "software developer"},
            "response": response_with_prof
        })
        
        # Test without profession (like original)
        template_no_prof = get_career_advice_template(has_profession=False)
        chain_no_prof = template_no_prof | self.llm | self.parser
        response_no_prof = chain_no_prof.invoke(
            {
                "name": "Sam",
                "age": "22"
            },
            config={"tags": ["conditional_no_profession"]}
        )
        results.append({
            "condition": "without_profession",
            "input": {"name": "Sam", "age": "22"},
            "response": response_no_prof
        })
        
        return {"technique": "Conditional Templates", "examples": results}
    
    def list_processing_templates(self) -> Dict[str, Any]:
        """
        Demonstrate list processing in templates.
        Following original's pattern of categorizing items.
        """
        self.logger.info("Running list processing templates")
        
        # Template for categorizing items (like original)
        categorize_template = PromptTemplate.from_template(
            "Categorize these items into groups: {items}. "
            "Provide the categories and the items in each category."
        )
        
        # Template with formatted list (simulating Jinja2 iteration)
        formatted_list_template = PromptTemplate.from_template(
            "Analyze the following list of items:\n"
            "{formatted_items}\n"
            "Provide a summary of the list and suggest any patterns or groupings."
        )
        
        results = []
        
        # Test categorization
        items_string = "apple, banana, carrot, hammer, screwdriver, pliers, novel, textbook, magazine"
        categorize_chain = categorize_template | self.llm | self.parser
        categorize_response = categorize_chain.invoke(
            {"items": items_string},
            config={"tags": ["list_categorize"]}
        )
        results.append({
            "type": "categorization",
            "items": items_string,
            "response": categorize_response
        })
        
        # Test formatted list (simulating Jinja2 for loop)
        tech_items = ["Python", "JavaScript", "HTML", "CSS", "React", "Django", "Flask", "Node.js"]
        formatted_items = "\n".join([f"- {item}" for item in tech_items])
        
        formatted_chain = formatted_list_template | self.llm | self.parser
        formatted_response = formatted_chain.invoke(
            {"formatted_items": formatted_items},
            config={"tags": ["list_formatted"]}
        )
        results.append({
            "type": "formatted_analysis",
            "items": tech_items,
            "response": formatted_response
        })
        
        return {"technique": "List Processing Templates", "examples": results}
    
    def dynamic_instruction_templates(self) -> Dict[str, Any]:
        """
        Demonstrate dynamic instruction generation with multiple variables.
        Following original's pattern of complex, structured prompts.
        """
        self.logger.info("Running dynamic instruction templates")
        
        # Dynamic instruction template (like original)
        instruction_template = PromptTemplate.from_template(
            "Task: {task}\n"
            "Context: {context}\n"
            "Constraints: {constraints}\n\n"
            "Please provide a solution that addresses the task, "
            "considers the context, and adheres to the constraints."
        )
        
        test_cases = [
            {
                "task": "Design a logo for a tech startup",
                "context": "The startup focuses on AI-driven healthcare solutions",
                "constraints": "Must use blue and green colors, and should be simple enough to be recognizable when small"
            },
            {
                "task": "Create a marketing strategy",
                "context": "Small local coffee shop wanting to increase customer base",
                "constraints": "Budget limited to $500 per month, must focus on digital channels"
            },
            {
                "task": "Plan a team building event",
                "context": "Remote software development team of 20 people across different time zones",
                "constraints": "Virtual event, 2-hour maximum duration, engaging for all participants"
            }
        ]
        
        results = []
        chain = instruction_template | self.llm | self.parser
        
        for i, test_case in enumerate(test_cases, 1):
            response = chain.invoke(
                test_case,
                config={"tags": [f"dynamic_instruction_{i}"]}
            )
            results.append({
                "case": i,
                "task": test_case["task"],
                "context": test_case["context"],
                "constraints": test_case["constraints"],
                "response": response
            })
        
        return {"technique": "Dynamic Instruction Templates", "examples": results}
    
    def template_composition(self) -> Dict[str, Any]:
        """
        Demonstrate template composition and reusability.
        Shows how to build complex templates from simpler ones.
        """
        self.logger.info("Running template composition examples")
        
        # Base templates that can be composed
        header_template = "Project: {project_name}\nDate: {date}\n"
        body_template = "Description: {description}\nGoals: {goals}\n"
        footer_template = "Next Steps: {next_steps}\nDeadline: {deadline}"
        
        # Compose full template
        full_template = PromptTemplate.from_template(
            header_template + "\n" + body_template + "\n" + footer_template + "\n\n"
            "Based on the above project information, provide a concise executive summary."
        )
        
        # Test with sample data
        project_data = {
            "project_name": "AI Customer Service Bot",
            "date": "2024-01-15",
            "description": "Implement an AI-powered chatbot for customer support",
            "goals": "Reduce response time by 50%, handle 80% of common queries automatically",
            "next_steps": "1. Gather requirements, 2. Select AI platform, 3. Develop prototype",
            "deadline": "Q2 2024"
        }
        
        chain = full_template | self.llm | self.parser
        response = chain.invoke(
            project_data,
            config={"tags": ["template_composition"]}
        )
        
        return {
            "technique": "Template Composition",
            "examples": [{
                "template_parts": ["header", "body", "footer"],
                "project_data": project_data,
                "response": response
            }]
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all prompt template and variable examples."""
        self.logger.info("Starting Prompt Templates and Variables demonstrations")
        
        results = {
            "technique_overview": "Prompt Templates and Variables",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.basic_variable_substitution(),
            self.conditional_templates(),
            self.list_processing_templates(),
            self.dynamic_instruction_templates(),
            self.template_composition()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("prompt-templates-variables")
    output_manager.add_header("03: PROMPT TEMPLATES AND VARIABLES - LANGCHAIN")
    
    # Initialize technique
    templates = PromptTemplatesVariables()
    
    try:
        # Run examples
        results = templates.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(templates.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        templates.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()