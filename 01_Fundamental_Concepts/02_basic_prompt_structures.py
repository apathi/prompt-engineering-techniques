"""
02: Basic Prompt Structures (LangChain Implementation)

This module demonstrates the fundamental differences between single-turn and multi-turn
prompt structures using modern LangChain patterns, following the original notebook approach.

Key concepts:
- Single-turn prompts: One-shot interactions
- Multi-turn prompts: Conversational context preservation  
- Memory management strategies
- Context comparison

"""

import os
import sys
from typing import List, Dict, Any, Optional

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory


class BasicPromptStructures:
    """Basic Prompt Structures: Single-turn vs Multi-turn patterns using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("basic_prompt_structures")
        self.client = LangChainClient(
            model=model,
            temperature=0.2,
            max_tokens=400,
            session_name="basic_prompt_structures"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        # Store message histories for different strategies
        self.message_histories = {}
        
    def single_turn_prompts(self) -> Dict[str, Any]:
        """
        Demonstrate single-turn prompt patterns following original notebook.
        One-shot interactions without context preservation.
        """
        self.logger.info("Running single-turn prompt examples")
        
        # Following original's simple approach
        prompts = [
            {
                "category": "Factual Query",
                "prompt": "What are the three primary colors?"
            },
            {
                "category": "Explanation Request",
                "prompt": "Explain the concept of machine learning in simple terms."
            },
            {
                "category": "Creative Task",
                "prompt": "Write a haiku about autumn leaves."
            },
            {
                "category": "Problem Solving",
                "prompt": "How do you calculate the area of a circle with radius 5 units?"
            },
            {
                "category": "Analysis Task",
                "prompt": "List three advantages and three disadvantages of renewable energy."
            }
        ]
        
        results = []
        for prompt_info in prompts:
            # Simple single-turn approach like original
            response = self.llm.invoke(
                prompt_info["prompt"],
                config={"tags": [f"single_turn_{prompt_info['category'].lower().replace(' ', '_')}"]}
            )
            
            results.append({
                "category": prompt_info["category"],
                "prompt": prompt_info["prompt"],
                "response": response.content if hasattr(response, 'content') else str(response)
            })
        
        return {"technique": "Single-Turn Prompts", "examples": results}
    
    def multi_turn_conversation(self) -> Dict[str, Any]:
        """
        Demonstrate multi-turn conversation with modern LangChain.
        Replaces deprecated ConversationChain with RunnableWithMessageHistory.
        """
        self.logger.info("Running multi-turn conversation example")
        
        # Create conversation prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant having a conversation about a topic."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Create chain with message history
        chain = prompt | self.llm | self.parser
        
        # Initialize message history for this conversation
        if "multi_turn" not in self.message_histories:
            self.message_histories["multi_turn"] = ChatMessageHistory()
        
        # Create runnable with history
        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: self.message_histories[session_id],
            input_messages_key="input",
            history_messages_key="history"
        )
        
        # Conversation about Paris (following original example)
        conversation_turns = [
            "Tell me about Paris.",
            "What's the population of that city?",
            "What are some famous landmarks there?",
            "How's the weather typically like in the city we've been discussing?",
            "What's the best time of year to visit?"
        ]
        
        results = []
        for i, user_input in enumerate(conversation_turns, 1):
            response = chain_with_history.invoke(
                {"input": user_input},
                config={
                    "configurable": {"session_id": "multi_turn"},
                    "tags": [f"multi_turn_{i}"]
                }
            )
            
            results.append({
                "turn": i,
                "user_input": user_input,
                "response": response,
                "context_used": i > 1  # Context is used after first turn
            })
        
        return {"technique": "Multi-Turn Conversation", "conversation": results}
    
    def context_comparison(self) -> Dict[str, Any]:
        """
        Compare responses with and without context.
        Demonstrates the importance of conversation history.
        """
        self.logger.info("Running context comparison analysis")
        
        # Initial context-setting statement
        initial_context = "Python is a high-level programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991."
        follow_up_question = "What are its main advantages?"
        
        # Response WITHOUT context (single-turn)
        response_no_context = self.llm.invoke(
            follow_up_question,
            config={"tags": ["no_context_followup"]}
        )
        
        # Response WITH context (using a prompt that includes context)
        context_prompt = ChatPromptTemplate.from_template(
            "{context}\n\nBased on the above information, {question}"
        )
        chain_with_context = context_prompt | self.llm | self.parser
        
        response_with_context = chain_with_context.invoke(
            {"context": initial_context, "question": follow_up_question},
            config={"tags": ["with_context_followup"]}
        )
        
        return {
            "technique": "Context Comparison",
            "initial_context": initial_context,
            "follow_up_question": follow_up_question,
            "without_context": {
                "response": response_no_context.content if hasattr(response_no_context, 'content') else str(response_no_context)
            },
            "with_context": {
                "response": response_with_context
            }
        }
    
    def memory_strategies_comparison(self) -> Dict[str, Any]:
        """
        Compare different memory strategies using LangChain's memory classes.
        Full memory vs sliding window vs no memory.
        """
        self.logger.info("Running memory strategies comparison")
        
        # Define memory strategies
        strategies = {
            "full_memory": {
                "memory": ConversationBufferMemory(return_messages=True),
                "description": "Keep all conversation history"
            },
            "sliding_window": {
                "memory": ConversationBufferWindowMemory(k=3, return_messages=True),
                "description": "Keep last 3 exchanges"
            },
            "no_memory": {
                "memory": None,
                "description": "No conversation memory"
            }
        }
        
        # Cooking conversation (following original approach)
        conversation_topics = [
            "I want to learn how to cook Italian food.",
            "What ingredients do I need for pasta?",
            "How do I make a good tomato sauce?",
            "What about seasoning?",
            "Can you suggest a complete recipe?",
            "How long does it take to cook?",
            "What wine pairs well with this dish?"
        ]
        
        results = {}
        
        for strategy_name, strategy_config in strategies.items():
            self.logger.info(f"Testing {strategy_name} strategy")
            strategy_results = []
            
            if strategy_config["memory"]:
                # Create prompt with memory
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful cooking assistant."),
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{input}")
                ])
                
                chain = prompt | self.llm | self.parser
                
                # Initialize new message history for this strategy
                self.message_histories[strategy_name] = ChatMessageHistory()
                
                chain_with_history = RunnableWithMessageHistory(
                    chain,
                    lambda session_id: self.message_histories[session_id],
                    input_messages_key="input",
                    history_messages_key="history"
                )
                
                for i, topic in enumerate(conversation_topics, 1):
                    response = chain_with_history.invoke(
                        {"input": topic},
                        config={
                            "configurable": {"session_id": strategy_name},
                            "tags": [f"{strategy_name}_turn_{i}"]
                        }
                    )
                    
                    # For sliding window, check actual memory size
                    if strategy_name == "sliding_window":
                        # Get actual context length from memory
                        messages = self.message_histories[strategy_name].messages
                        context_length = min(len(messages) // 2, 3)  # Each exchange is 2 messages
                    elif strategy_name == "full_memory":
                        messages = self.message_histories[strategy_name].messages
                        context_length = len(messages) // 2
                    else:
                        context_length = 0
                    
                    strategy_results.append({
                        "turn": i,
                        "topic": topic,
                        "response": response,
                        "context_length": context_length
                    })
            else:
                # No memory - simple single-turn
                for i, topic in enumerate(conversation_topics, 1):
                    response = self.llm.invoke(
                        topic,
                        config={"tags": [f"no_memory_turn_{i}"]}
                    )
                    
                    strategy_results.append({
                        "turn": i,
                        "topic": topic,
                        "response": (response.content if hasattr(response, 'content') else str(response)),
                        "context_length": 0
                    })
            
            results[strategy_name] = {
                "description": strategy_config["description"],
                "conversation": strategy_results
            }
        
        return {"technique": "Memory Strategies Comparison", "strategies": results}
    
    def prompt_structure_comparison(self) -> Dict[str, Any]:
        """
        Compare how single-turn and multi-turn handle related questions.
        Following original notebook's Paris example.
        """
        self.logger.info("Running prompt structure comparison")
        
        # Questions about France/Paris
        questions = [
            "What is the capital of France?",
            "What is its population?",
            "What is the city's most famous landmark?"
        ]
        
        # Single-turn responses (no context)
        single_turn_results = []
        for question in questions:
            response = self.llm.invoke(
                question,
                config={"tags": ["single_comparison"]}
            )
            single_turn_results.append({
                "question": question,
                "response": response.content if hasattr(response, 'content') else str(response)
            })
        
        # Multi-turn responses (with context)
        multi_turn_results = []
        
        # Setup conversation with history
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        chain = prompt | self.llm | self.parser
        self.message_histories["comparison"] = ChatMessageHistory()
        
        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: self.message_histories[session_id],
            input_messages_key="input",
            history_messages_key="history"
        )
        
        for question in questions:
            response = chain_with_history.invoke(
                {"input": question},
                config={
                    "configurable": {"session_id": "comparison"},
                    "tags": ["multi_comparison"]
                }
            )
            multi_turn_results.append({
                "question": question,
                "response": response
            })
        
        return {
            "technique": "Single vs Multi-Turn Comparison",
            "single_turn": single_turn_results,
            "multi_turn": multi_turn_results
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all basic prompt structure examples."""
        self.logger.info("Starting Basic Prompt Structures demonstrations")
        
        results = {
            "technique_overview": "Basic Prompt Structures",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.single_turn_prompts(),
            self.multi_turn_conversation(),
            self.context_comparison(),
            self.memory_strategies_comparison(),
            self.prompt_structure_comparison()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("basic-prompt-structures")
    output_manager.add_header("02: BASIC PROMPT STRUCTURES - LANGCHAIN")
    
    # Initialize technique
    structures = BasicPromptStructures()
    
    try:
        # Run examples
        results = structures.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(structures.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        structures.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()