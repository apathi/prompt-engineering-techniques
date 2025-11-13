"""
04: Zero-Shot Prompting (LangChain Implementation)

This module demonstrates zero-shot prompting techniques where AI performs tasks
without specific examples, following the original notebook's approach.

Key concepts:
- Direct task specification
- Role-based prompting
- Format specification for structured outputs
- Multi-step reasoning without examples
- Task generalization capabilities

"""

import os
import sys
from typing import List, Dict, Any

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ZeroShotPrompting:
    """Zero-Shot Prompting: Performing tasks without examples using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("zero_shot_prompting")
        self.client = LangChainClient(
            model=model,
            temperature=0.2,
            max_tokens=400,
            session_name="zero_shot_prompting"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
    
    def direct_task_specification(self) -> Dict[str, Any]:
        """
        Demonstrate direct task specification without examples.
        Following original's clear, specific task instructions.
        """
        self.logger.info("Running direct task specification examples")
        
        # Direct task prompts (following original pattern)
        tasks = [
            {
                "task": "Sentiment Analysis",
                "prompt": PromptTemplate.from_template(
                    "Classify the sentiment of the following text as positive, negative, or neutral.\n"
                    "Do not explain your reasoning, just provide the classification.\n\n"
                    "Text: {text}\n\n"
                    "Sentiment:"
                ),
                "test_input": "This product exceeded all my expectations and works perfectly!"
            },
            {
                "task": "Text Summarization",
                "prompt": PromptTemplate.from_template(
                    "Summarize the following text in one concise sentence:\n\n"
                    "Text: {text}\n\n"
                    "Summary:"
                ),
                "test_input": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. It uses algorithms that iteratively learn from data, allowing computers to find hidden insights without being explicitly programmed where to look."
            },
            {
                "task": "Language Translation",
                "prompt": PromptTemplate.from_template(
                    "Translate the following English text to French:\n\n"
                    "Text: {text}\n\n"
                    "Translation:"
                ),
                "test_input": "Good morning, how are you today?"
            },
            {
                "task": "Named Entity Recognition",
                "prompt": PromptTemplate.from_template(
                    "Extract all named entities (people, places, organizations) from the following text:\n\n"
                    "Text: {text}\n\n"
                    "Entities:"
                ),
                "test_input": "Apple Inc. announced that Tim Cook will visit the Paris office next week to meet with European partners."
            }
        ]
        
        results = []
        for task_info in tasks:
            chain = task_info["prompt"] | self.llm | self.parser
            response = chain.invoke(
                {"text": task_info["test_input"]},
                config={"tags": [f"direct_task_{task_info['task'].lower().replace(' ', '_')}"]}
            )
            
            results.append({
                "task": task_info["task"],
                "input": task_info["test_input"],
                "response": response
            })
        
        return {"technique": "Direct Task Specification", "examples": results}
    
    def role_based_prompting(self) -> Dict[str, Any]:
        """
        Demonstrate role-based zero-shot prompting.
        Assigning specific roles to guide responses.
        """
        self.logger.info("Running role-based prompting examples")
        
        roles = [
            {
                "role": "Financial Advisor",
                "prompt": ChatPromptTemplate.from_template(
                    "You are a professional financial advisor. "
                    "Provide advice on the following question:\n\n"
                    "{question}"
                ),
                "question": "Should I invest in cryptocurrency?"
            },
            {
                "role": "Science Teacher",
                "prompt": ChatPromptTemplate.from_template(
                    "You are an experienced science teacher explaining to high school students. "
                    "Explain the following concept:\n\n"
                    "{question}"
                ),
                "question": "How does photosynthesis work?"
            },
            {
                "role": "Legal Expert",
                "prompt": ChatPromptTemplate.from_template(
                    "You are a legal expert providing general information (not legal advice). "
                    "Explain the following legal concept:\n\n"
                    "{question}"
                ),
                "question": "What is intellectual property?"
            },
            {
                "role": "Chef",
                "prompt": ChatPromptTemplate.from_template(
                    "You are a professional chef. "
                    "Provide guidance on the following culinary question:\n\n"
                    "{question}"
                ),
                "question": "How do I properly season a cast iron skillet?"
            }
        ]
        
        results = []
        for role_info in roles:
            chain = role_info["prompt"] | self.llm | self.parser
            response = chain.invoke(
                {"question": role_info["question"]},
                config={"tags": [f"role_{role_info['role'].lower().replace(' ', '_')}"]}
            )
            
            results.append({
                "role": role_info["role"],
                "question": role_info["question"],
                "response": response[:300] + "..."  # Truncate for display
            })
        
        return {"technique": "Role-Based Prompting", "examples": results}
    
    def format_specification(self) -> Dict[str, Any]:
        """
        Demonstrate format specification for structured outputs.
        Showing how to request specific output formats.
        """
        self.logger.info("Running format specification examples")
        
        format_tasks = [
            {
                "format": "Bullet Points",
                "prompt": PromptTemplate.from_template(
                    "List the main benefits of regular exercise.\n"
                    "Format your response as bullet points.\n\n"
                    "Benefits:"
                )
            },
            {
                "format": "JSON",
                "prompt": PromptTemplate.from_template(
                    "Analyze this product review and return the results in JSON format "
                    "with keys: 'sentiment', 'rating' (1-5), and 'summary'.\n\n"
                    "Review: {review}\n\n"
                    "JSON Output:"
                ),
                "input": "This laptop is amazing! Fast processor, great battery life, and beautiful display. Highly recommend!"
            },
            {
                "format": "Table",
                "prompt": PromptTemplate.from_template(
                    "Compare Python and JavaScript.\n"
                    "Format your response as a table with columns: Feature, Python, JavaScript\n\n"
                    "Table:"
                )
            },
            {
                "format": "Numbered List",
                "prompt": PromptTemplate.from_template(
                    "Provide a step-by-step guide to make coffee.\n"
                    "Format as a numbered list.\n\n"
                    "Steps:"
                )
            }
        ]
        
        results = []
        for format_info in format_tasks:
            chain = format_info["prompt"] | self.llm | self.parser
            
            # Prepare input based on whether the task needs input
            if "input" in format_info:
                invoke_input = {"review": format_info["input"]}
            else:
                invoke_input = {}
            
            response = chain.invoke(
                invoke_input,
                config={"tags": [f"format_{format_info['format'].lower().replace(' ', '_')}"]}
            )
            
            results.append({
                "format": format_info["format"],
                "input": format_info.get("input", "N/A"),
                "response": response
            })
        
        return {"technique": "Format Specification", "examples": results}
    
    def multi_step_reasoning(self) -> Dict[str, Any]:
        """
        Demonstrate multi-step reasoning without examples.
        Breaking down complex tasks into steps.
        """
        self.logger.info("Running multi-step reasoning examples")
        
        reasoning_tasks = [
            {
                "task": "Problem Solving",
                "prompt": ChatPromptTemplate.from_template(
                    "Solve this problem step by step:\n\n"
                    "{problem}\n\n"
                    "Show your reasoning for each step."
                ),
                "problem": "A train travels 120 km in 2 hours. If it maintains the same speed, how far will it travel in 5 hours?"
            },
            {
                "task": "Decision Analysis",
                "prompt": ChatPromptTemplate.from_template(
                    "Analyze this decision step by step:\n\n"
                    "{decision}\n\n"
                    "Consider pros, cons, and provide a recommendation."
                ),
                "decision": "Should a small business invest in social media marketing or traditional advertising?"
            },
            {
                "task": "Process Explanation",
                "prompt": ChatPromptTemplate.from_template(
                    "Explain this process step by step:\n\n"
                    "{process}\n\n"
                    "Break it down into clear, sequential steps."
                ),
                "process": "How does a computer boot up when you press the power button?"
            }
        ]
        
        results = []
        for task_info in reasoning_tasks:
            chain = task_info["prompt"] | self.llm | self.parser
            
            input_key = "problem" if "problem" in task_info else "decision" if "decision" in task_info else "process"
            response = chain.invoke(
                {input_key: task_info[input_key]},
                config={"tags": [f"reasoning_{task_info['task'].lower().replace(' ', '_')}"]}
            )
            
            results.append({
                "task": task_info["task"],
                "input": task_info.get("problem") or task_info.get("decision") or task_info.get("process"),
                "response": response
            })
        
        return {"technique": "Multi-Step Reasoning", "examples": results}
    
    def comparative_zero_shot(self) -> Dict[str, Any]:
        """
        Compare zero-shot performance on the same task with different prompt structures.
        Shows how prompt design affects zero-shot performance.
        """
        self.logger.info("Running comparative zero-shot analysis")
        
        # Same task, different prompt structures
        task = "Determine if this email is spam"
        email = "Congratulations! You've won $1,000,000! Click here immediately to claim your prize before it expires!"
        
        prompt_variations = [
            {
                "style": "Minimal",
                "prompt": PromptTemplate.from_template(
                    "Is this spam? {email}"
                )
            },
            {
                "style": "Detailed",
                "prompt": PromptTemplate.from_template(
                    "Analyze the following email and determine if it is spam or legitimate.\n"
                    "Consider factors like urgency, monetary promises, and credibility.\n\n"
                    "Email: {email}\n\n"
                    "Classification:"
                )
            },
            {
                "style": "Structured",
                "prompt": PromptTemplate.from_template(
                    "Task: Spam Detection\n"
                    "Input: {email}\n"
                    "Required Output: 'SPAM' or 'NOT SPAM' with brief reason\n\n"
                    "Analysis:"
                )
            },
            {
                "style": "Role-Based",
                "prompt": PromptTemplate.from_template(
                    "You are an email security expert. "
                    "Analyze this email for spam characteristics:\n\n"
                    "{email}\n\n"
                    "Expert Assessment:"
                )
            }
        ]
        
        results = []
        for variation in prompt_variations:
            chain = variation["prompt"] | self.llm | self.parser
            response = chain.invoke(
                {"email": email},
                config={"tags": [f"comparative_{variation['style'].lower()}"]}
            )
            
            results.append({
                "prompt_style": variation["style"],
                "response": response
            })
        
        return {
            "technique": "Comparative Zero-Shot Analysis",
            "task": task,
            "test_input": email,
            "examples": results
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all zero-shot prompting examples."""
        self.logger.info("Starting Zero-Shot Prompting demonstrations")
        
        results = {
            "technique_overview": "Zero-Shot Prompting",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.direct_task_specification(),
            self.role_based_prompting(),
            self.format_specification(),
            self.multi_step_reasoning(),
            self.comparative_zero_shot()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("zero-shot-prompting")
    output_manager.add_header("04: ZERO-SHOT PROMPTING - LANGCHAIN")
    
    # Initialize technique
    zero_shot = ZeroShotPrompting()
    
    try:
        # Run examples
        results = zero_shot.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(zero_shot.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        zero_shot.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()