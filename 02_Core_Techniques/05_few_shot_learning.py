"""
05: Few-Shot Learning (LangChain Implementation)

This module demonstrates few-shot learning techniques where AI learns from
a small number of examples (typically 2-5) to perform similar tasks,
following the original notebook's approach.

Key concepts:
- Example selection strategies
- Consistent input/output formatting
- Pattern recognition from minimal examples
- Multi-task few-shot learning
- In-context learning capabilities

"""

import os
import sys
from typing import List, Dict, Any, Tuple

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class FewShotLearning:
    """Few-Shot Learning: Learning from small example sets using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("few_shot_learning")
        self.client = LangChainClient(
            model=model,
            temperature=0.2,
            max_tokens=400,
            session_name="few_shot_learning"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
    
    def basic_few_shot_classification(self) -> Dict[str, Any]:
        """
        Demonstrate basic few-shot sentiment classification.
        Following original's pattern with clear examples.
        """
        self.logger.info("Running basic few-shot classification")
        
        # Create few-shot prompt template (following original structure)
        example_prompt = PromptTemplate(
            input_variables=["input", "output"],
            template="Text: {input}\nSentiment: {output}"
        )
        
        # Examples from original notebook
        examples = [
            {"input": "I love this product! It's amazing.", "output": "Positive"},
            {"input": "This movie was terrible. I hated it.", "output": "Negative"},
            {"input": "The weather today is okay.", "output": "Neutral"}
        ]
        
        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix="Classify the sentiment as Positive, Negative, or Neutral.",
            suffix="Text: {input}\nSentiment:",
            input_variables=["input"]
        )
        
        # Test cases
        test_inputs = [
            "I can't believe how great this new restaurant is!",
            "Complete waste of money and time.",
            "It does what it's supposed to do, nothing special.",
            "Absolutely fantastic experience, highly recommended!",
            "Not good, not bad, just average."
        ]
        
        results = []
        chain = few_shot_prompt | self.llm | self.parser
        
        for test_input in test_inputs:
            response = chain.invoke(
                {"input": test_input},
                config={"tags": ["few_shot_sentiment"]}
            )
            results.append({
                "input": test_input,
                "prediction": response.strip()
            })
        
        return {"technique": "Basic Few-Shot Classification", "examples": results}
    
    def multi_task_few_shot(self) -> Dict[str, Any]:
        """
        Demonstrate multi-task few-shot learning.
        Following original's sentiment + language detection pattern.
        """
        self.logger.info("Running multi-task few-shot learning")
        
        # Multi-task template (like original)
        multi_task_template = PromptTemplate.from_template(
            """Perform the specified task on the given text.

Examples:
Text: I love this product! It's amazing.
Task: sentiment
Result: Positive

Text: Bonjour, comment allez-vous?
Task: language
Result: French

Text: This is awful.
Task: sentiment
Result: Negative

Text: Guten Tag, wie geht es dir?
Task: language
Result: German

Now, perform the following task:
Text: {text}
Task: {task}
Result:"""
        )
        
        # Test cases for both tasks
        test_cases = [
            {"text": "This exceeded my expectations!", "task": "sentiment"},
            {"text": "Hola, ¿cómo estás?", "task": "language"},
            {"text": "I'm disappointed with this purchase.", "task": "sentiment"},
            {"text": "Ciao, come stai?", "task": "language"},
            {"text": "Pretty good overall.", "task": "sentiment"},
            {"text": "Привет, как дела?", "task": "language"}
        ]
        
        results = []
        chain = multi_task_template | self.llm | self.parser
        
        for test_case in test_cases:
            response = chain.invoke(
                test_case,
                config={"tags": [f"multi_task_{test_case['task']}"]}
            )
            results.append({
                "text": test_case["text"],
                "task": test_case["task"],
                "result": response.strip()
            })
        
        return {"technique": "Multi-Task Few-Shot Learning", "examples": results}
    
    def in_context_learning_custom_task(self) -> Dict[str, Any]:
        """
        Demonstrate in-context learning for a custom task.
        Following original's pig latin transformation example.
        """
        self.logger.info("Running in-context learning for custom task")
        
        # Custom task: Convert text to pig latin (from original)
        pig_latin_template = PromptTemplate.from_template(
            """Convert the given text to pig latin.

Examples:
Input: hello
Output: ellohay

Input: apple
Output: appleay

Input: string
Output: ingstray

Now, convert the following:
Input: {input}
Output:"""
        )
        
        # Test inputs
        test_words = ["python", "computer", "language", "machine", "example"]
        
        results = []
        chain = pig_latin_template | self.llm | self.parser
        
        for word in test_words:
            response = chain.invoke(
                {"input": word},
                config={"tags": ["in_context_pig_latin"]}
            )
            results.append({
                "input": word,
                "output": response.strip()
            })
        
        return {"technique": "In-Context Learning - Custom Task", "examples": results}
    
    def example_selection_strategies(self) -> Dict[str, Any]:
        """
        Demonstrate different example selection strategies.
        Shows how example quality affects performance.
        """
        self.logger.info("Running example selection strategies")
        
        # Different example sets for sentiment classification
        strategies = {
            "balanced": {
                "examples": [
                    {"input": "I love this!", "output": "Positive"},
                    {"input": "This is terrible.", "output": "Negative"},
                    {"input": "It's okay.", "output": "Neutral"}
                ],
                "description": "Balanced examples covering all classes"
            },
            "extreme": {
                "examples": [
                    {"input": "Absolutely amazing, best ever!", "output": "Positive"},
                    {"input": "Worst thing I've ever seen, horrible!", "output": "Negative"},
                    {"input": "Completely average, nothing special.", "output": "Neutral"}
                ],
                "description": "Extreme examples with strong sentiments"
            },
            "subtle": {
                "examples": [
                    {"input": "Pretty good overall.", "output": "Positive"},
                    {"input": "Not quite what I expected.", "output": "Negative"},
                    {"input": "Meets basic requirements.", "output": "Neutral"}
                ],
                "description": "Subtle examples with weak sentiments"
            }
        }
        
        # Test input that could be ambiguous
        test_input = "It's not bad, could be better though."
        
        results = []
        example_prompt = PromptTemplate(
            input_variables=["input", "output"],
            template="Text: {input}\nSentiment: {output}"
        )
        
        for strategy_name, strategy_info in strategies.items():
            few_shot_prompt = FewShotPromptTemplate(
                examples=strategy_info["examples"],
                example_prompt=example_prompt,
                prefix="Classify the sentiment as Positive, Negative, or Neutral.",
                suffix="Text: {input}\nSentiment:",
                input_variables=["input"]
            )
            
            chain = few_shot_prompt | self.llm | self.parser
            response = chain.invoke(
                {"input": test_input},
                config={"tags": [f"strategy_{strategy_name}"]}
            )
            
            results.append({
                "strategy": strategy_name,
                "description": strategy_info["description"],
                "examples_used": strategy_info["examples"],
                "test_input": test_input,
                "prediction": response.strip()
            })
        
        return {"technique": "Example Selection Strategies", "examples": results}
    
    def few_shot_vs_zero_shot_comparison(self) -> Dict[str, Any]:
        """
        Compare few-shot vs zero-shot performance on the same task.
        Shows the value of providing examples.
        """
        self.logger.info("Running few-shot vs zero-shot comparison")
        
        # Test task: Classify product categories
        test_products = [
            "iPhone 13 Pro with 128GB storage",
            "Nike Air Max running shoes size 10",
            "The Great Gatsby paperback novel",
            "Organic green tea bags, 20 count",
            "Sony PlayStation 5 gaming console"
        ]
        
        # Zero-shot approach
        zero_shot_template = PromptTemplate.from_template(
            "Classify this product into a category: {product}\nCategory:"
        )
        
        # Few-shot approach
        few_shot_examples = [
            {"input": "MacBook Pro laptop computer", "output": "Electronics"},
            {"input": "Adidas running sneakers", "output": "Sports & Outdoors"},
            {"input": "Harry Potter hardcover book", "output": "Books"},
            {"input": "Earl Grey tea blend", "output": "Food & Beverages"},
            {"input": "Xbox Series X console", "output": "Electronics"}
        ]
        
        example_prompt = PromptTemplate(
            input_variables=["input", "output"],
            template="Product: {input}\nCategory: {output}"
        )
        
        few_shot_prompt = FewShotPromptTemplate(
            examples=few_shot_examples,
            example_prompt=example_prompt,
            prefix="Classify each product into an appropriate category.",
            suffix="Product: {input}\nCategory:",
            input_variables=["input"]
        )
        
        results = []
        zero_shot_chain = zero_shot_template | self.llm | self.parser
        few_shot_chain = few_shot_prompt | self.llm | self.parser
        
        for product in test_products:
            # Zero-shot prediction
            zero_shot_response = zero_shot_chain.invoke(
                {"product": product},
                config={"tags": ["comparison_zero_shot"]}
            )
            
            # Few-shot prediction
            few_shot_response = few_shot_chain.invoke(
                {"input": product},
                config={"tags": ["comparison_few_shot"]}
            )
            
            results.append({
                "product": product,
                "zero_shot": zero_shot_response.strip(),
                "few_shot": few_shot_response.strip()
            })
        
        return {"technique": "Few-Shot vs Zero-Shot Comparison", "examples": results}
    
    def adaptive_few_shot_learning(self) -> Dict[str, Any]:
        """
        Demonstrate adaptive few-shot learning with different numbers of examples.
        Shows how performance changes with more examples.
        """
        self.logger.info("Running adaptive few-shot learning")
        
        # Base examples for sentiment analysis
        all_examples = [
            {"input": "Amazing product!", "output": "Positive"},
            {"input": "Terrible quality.", "output": "Negative"},
            {"input": "It's average.", "output": "Neutral"},
            {"input": "Exceeded expectations!", "output": "Positive"},
            {"input": "Complete waste of money.", "output": "Negative"},
            {"input": "Does the job adequately.", "output": "Neutral"}
        ]
        
        # Test with different numbers of examples
        example_counts = [1, 2, 3, 6]  # 1, 2, 3, all examples
        test_input = "Pretty disappointed with this purchase."
        
        results = []
        example_prompt = PromptTemplate(
            input_variables=["input", "output"],
            template="Text: {input}\nSentiment: {output}"
        )
        
        for count in example_counts:
            examples_subset = all_examples[:count]
            
            few_shot_prompt = FewShotPromptTemplate(
                examples=examples_subset,
                example_prompt=example_prompt,
                prefix="Classify the sentiment as Positive, Negative, or Neutral.",
                suffix="Text: {input}\nSentiment:",
                input_variables=["input"]
            )
            
            chain = few_shot_prompt | self.llm | self.parser
            response = chain.invoke(
                {"input": test_input},
                config={"tags": [f"adaptive_{count}_examples"]}
            )
            
            results.append({
                "num_examples": count,
                "examples_used": examples_subset,
                "test_input": test_input,
                "prediction": response.strip()
            })
        
        return {"technique": "Adaptive Few-Shot Learning", "examples": results}
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all few-shot learning examples."""
        self.logger.info("Starting Few-Shot Learning demonstrations")
        
        results = {
            "technique_overview": "Few-Shot Learning",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.basic_few_shot_classification(),
            self.multi_task_few_shot(),
            self.in_context_learning_custom_task(),
            self.example_selection_strategies(),
            self.few_shot_vs_zero_shot_comparison(),
            self.adaptive_few_shot_learning()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("few-shot-learning")
    output_manager.add_header("05: FEW-SHOT LEARNING - LANGCHAIN")
    
    # Initialize technique
    few_shot = FewShotLearning()
    
    try:
        # Run examples
        results = few_shot.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(few_shot.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        few_shot.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()