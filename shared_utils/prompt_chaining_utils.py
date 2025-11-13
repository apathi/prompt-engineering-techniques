"""
Prompt Chaining Utilities

Provides enterprise-grade chaining capabilities for complex multi-step prompt workflows
with comprehensive error handling, validation, performance tracking, and execution management.

Features:
- Sequential and parallel chain execution
- Dynamic conditional routing based on complexity
- Comprehensive error recovery and validation
- Performance metrics and monitoring
- Result synthesis and intelligent aggregation
- Production-ready logging and debugging
"""

import asyncio
import time
import json
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional, Callable, Union
from datetime import datetime
import logging

class ChainPerformanceMetrics:
    """Performance tracking for chain execution."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.step_timings = []
        self.total_tokens = 0
        self.step_count = 0
    
    def start_execution(self):
        """Start timing the chain execution."""
        self.start_time = time.time()
    
    def end_execution(self):
        """End timing the chain execution."""
        self.end_time = time.time()
    
    def record_step_timing(self, step: int, duration: float):
        """Record timing for a specific step."""
        self.step_timings.append({"step": step, "duration": duration})
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        total_time = (self.end_time - self.start_time) if self.end_time and self.start_time else 0
        avg_step_time = sum(t["duration"] for t in self.step_timings) / len(self.step_timings) if self.step_timings else 0
        
        return {
            "total_execution_time": round(total_time, 3),
            "average_step_time": round(avg_step_time, 3),
            "total_steps": len(self.step_timings),
            "step_timings": self.step_timings,
            "total_tokens_estimated": self.total_tokens
        }

class PromptChainManager:
    """Enterprise-grade prompt chain manager with comprehensive features."""
    
    def __init__(self, llm, enable_logging: bool = True, max_retries: int = 3):
        """
        Initialize chain manager with advanced configuration.
        
        Args:
            llm: Language model instance
            enable_logging: Enable detailed logging
            max_retries: Maximum retry attempts for failed steps
        """
        self.llm = llm
        self.enable_logging = enable_logging
        self.max_retries = max_retries
        self.chain_history = []
        self.execution_log = []
        self.performance_metrics = ChainPerformanceMetrics()
        
        # Setup logging
        if enable_logging:
            self.logger = logging.getLogger(f"PromptChainManager_{id(self)}")
            self.logger.setLevel(logging.INFO)
    
    def execute_sequential_chain(self, chain_steps: List[Dict[str, Any]], initial_input: str) -> Dict[str, Any]:
        """
        Execute a sequential chain of prompts with comprehensive features.
        
        Args:
            chain_steps: List of step configurations with templates, validators, and retry options
            initial_input: Initial input to start the chain
            
        Returns:
            Dictionary with success status, results, performance metrics, and execution history
        """
        # Start performance tracking
        self.performance_metrics.start_execution()
        current_input = initial_input
        results = []
        
        if self.enable_logging:
            self.logger.info(f"Starting sequential chain with {len(chain_steps)} steps")
        
        for i, step in enumerate(chain_steps):
            step_start_time = time.time()
            retry_count = 0
            step_successful = False
            
            while retry_count <= self.max_retries and not step_successful:
                try:
                    # Enhanced step logging
                    step_log = {
                        "step": i + 1,
                        "template": step["template"],
                        "input_preview": current_input,
                        "timestamp": datetime.now().isoformat(),
                        "retry_attempt": retry_count
                    }
                    self.chain_history.append(step_log)
                    
                    if self.enable_logging:
                        self.logger.info(f"Executing step {i + 1} (attempt {retry_count + 1})")
                    
                    # Create and execute chain
                    from langchain_core.prompts import PromptTemplate
                    from langchain_core.output_parsers import StrOutputParser
                    
                    prompt = PromptTemplate.from_template(step["template"])
                    chain = prompt | self.llm | StrOutputParser()
                    result = chain.invoke({"input": current_input})
                    
                    # Advanced validation with multiple validators
                    validation_results = []
                    if "validators" in step:
                        for validator_name, validator_func in step["validators"].items():
                            is_valid = validator_func(result)
                            validation_results.append({"validator": validator_name, "passed": is_valid})
                            if not is_valid:
                                raise ValueError(f"Step {i + 1} failed {validator_name} validation")
                    elif "validator" in step and step["validator"]:
                        is_valid = step["validator"](result)
                        validation_results.append({"validator": "default", "passed": is_valid})
                        if not is_valid:
                            raise ValueError(f"Step {i + 1} validation failed")
                    
                    # Successful step completion
                    step_duration = time.time() - step_start_time
                    self.performance_metrics.record_step_timing(i + 1, step_duration)
                    
                    step_result = {
                        "step": i + 1,
                        "output": result,
                        "validation_results": validation_results,
                        "execution_time": round(step_duration, 3),
                        "retry_count": retry_count,
                        "output_length": len(result)
                    }
                    results.append(step_result)
                    
                    # Update input for next step
                    current_input = result
                    step_successful = True
                    
                    if self.enable_logging:
                        self.logger.info(f"Step {i + 1} completed successfully in {step_duration:.3f}s")
                
                except Exception as e:
                    retry_count += 1
                    error_msg = str(e)
                    
                    if self.enable_logging:
                        self.logger.warning(f"Step {i + 1} failed (attempt {retry_count}): {error_msg}")
                    
                    if retry_count > self.max_retries:
                        # Final failure after all retries
                        self.performance_metrics.end_execution()
                        
                        error_result = {
                            "success": False,
                            "error": f"Chain failed at step {i + 1} after {self.max_retries + 1} attempts: {error_msg}",
                            "partial_results": results,
                            "execution_history": self.chain_history,
                            "performance_metrics": self.performance_metrics.get_summary()
                        }
                        
                        self.execution_log.append({
                            "timestamp": datetime.now().isoformat(),
                            "status": "failed",
                            "error": error_msg,
                            "step": i + 1,
                            "total_retries": retry_count - 1
                        })
                        
                        return error_result
                    
                    # Wait before retry (exponential backoff)
                    if retry_count <= self.max_retries:
                        wait_time = 0.5 * (2 ** (retry_count - 1))  # 0.5s, 1s, 2s...
                        time.sleep(wait_time)
        
        # Successful completion
        self.performance_metrics.end_execution()
        
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "steps_completed": len(chain_steps),
            "total_execution_time": self.performance_metrics.get_summary()["total_execution_time"]
        })
        
        if self.enable_logging:
            self.logger.info(f"Chain completed successfully in {self.performance_metrics.get_summary()['total_execution_time']}s")
        
        return {
            "success": True,
            "results": results,
            "final_output": current_input,
            "execution_history": self.chain_history,
            "performance_metrics": self.performance_metrics.get_summary(),
            "execution_log": self.execution_log
        }
    
    def execute_parallel_chains(self, prompt_templates: Dict[str, str], document: str, 
                              synthesis_template: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute multiple prompts in parallel with comprehensive result synthesis.
        
        Args:
            prompt_templates: Dictionary of prompt names to template strings
            document: Input document to analyze
            synthesis_template: Optional template for combining results
            
        Returns:
            Dictionary with parallel results, synthesis, and performance metrics
        """
        start_time = time.time()
        
        def run_single_prompt(prompt_name: str, template: str) -> Dict[str, Any]:
            """Execute a single prompt with enhanced error handling and timing."""
            step_start = time.time()
            try:
                if self.enable_logging:
                    self.logger.info(f"Starting parallel execution: {prompt_name}")
                
                from langchain_core.prompts import PromptTemplate
                from langchain_core.output_parsers import StrOutputParser
                
                prompt = PromptTemplate.from_template(template)
                chain = prompt | self.llm | StrOutputParser()
                result = chain.invoke({"document": document})
                
                execution_time = time.time() - step_start
                
                if self.enable_logging:
                    self.logger.info(f"Completed {prompt_name} in {execution_time:.3f}s")
                
                return {
                    "name": prompt_name,
                    "result": result,
                    "success": True,
                    "execution_time": round(execution_time, 3),
                    "output_length": len(result)
                }
            except Exception as e:
                execution_time = time.time() - step_start
                error_msg = str(e)
                
                if self.enable_logging:
                    self.logger.error(f"Failed {prompt_name} in {execution_time:.3f}s: {error_msg}")
                
                return {
                    "name": prompt_name,
                    "result": f"Error: {error_msg}",
                    "success": False,
                    "execution_time": round(execution_time, 3),
                    "error": error_msg
                }
        
        # Execute all prompts in parallel with enhanced monitoring
        max_workers = min(len(prompt_templates), 4)  # Optimal worker count
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(run_single_prompt, name, template)
                for name, template in prompt_templates.items()
            ]
            parallel_results = [future.result() for future in futures]
        
        # Organize results
        results_dict = {r["name"]: r["result"] for r in parallel_results}
        successful_results = {r["name"]: r["result"] for r in parallel_results if r["success"]}
        
        # Advanced result synthesis
        synthesis_result = None
        if synthesis_template and successful_results:
            try:
                from langchain_core.prompts import PromptTemplate
                from langchain_core.output_parsers import StrOutputParser
                
                synthesis_prompt = PromptTemplate.from_template(synthesis_template)
                synthesis_chain = synthesis_prompt | self.llm | StrOutputParser()
                
                # Create synthesis input from all successful results
                synthesis_input = "\n\n".join([
                    f"{name.upper()}:\n{result}" 
                    for name, result in successful_results.items()
                ])
                
                synthesis_result = synthesis_chain.invoke({
                    "analysis_results": synthesis_input,
                    "original_document": document
                })
                
                if self.enable_logging:
                    self.logger.info("Synthesis completed successfully")
                    
            except Exception as e:
                synthesis_result = f"Synthesis failed: {str(e)}"
                if self.enable_logging:
                    self.logger.error(f"Synthesis failed: {str(e)}")
        
        total_execution_time = time.time() - start_time
        
        # Comprehensive result package
        return {
            "success": True,
            "parallel_results": results_dict,
            "successful_count": len(successful_results),
            "failed_count": len(parallel_results) - len(successful_results),
            "synthesis": synthesis_result,
            "execution_details": parallel_results,
            "performance_metrics": {
                "total_execution_time": round(total_execution_time, 3),
                "max_workers_used": max_workers,
                "average_execution_time": round(
                    sum(r["execution_time"] for r in parallel_results) / len(parallel_results), 3
                ),
                "fastest_execution": min(r["execution_time"] for r in parallel_results),
                "slowest_execution": max(r["execution_time"] for r in parallel_results)
            }
        }

def create_adaptive_complexity_chain(llm):
    """Create a chain that adapts based on input complexity assessment."""
    
    def assess_and_route(user_query: str, complexity_threshold: int = 5) -> str:
        """Assess query complexity and route to appropriate processing chain."""
        
        # Step 1: Assess complexity
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        complexity_prompt = PromptTemplate.from_template(
            """Rate the complexity of this query from 1-10 and explain briefly why:
            
            Query: {query}
            
            Complexity rating (start with number):"""
        )
        
        complexity_chain = complexity_prompt | llm | StrOutputParser()
        complexity_assessment = complexity_chain.invoke({"query": user_query})
        
        try:
            # Extract complexity score
            complexity_score = int(complexity_assessment.split()[0])
        except (ValueError, IndexError):
            complexity_score = 5  # Default to medium complexity
        
        if complexity_score <= complexity_threshold:
            # Simple chain for low complexity
            simple_prompt = PromptTemplate.from_template(
                "Provide a direct, comprehensive answer to: {query}"
            )
            simple_chain = simple_prompt | llm | StrOutputParser()
            return simple_chain.invoke({"query": user_query})
        
        else:
            # Complex multi-step chain
            manager = PromptChainManager(llm)
            
            complex_steps = [
                {
                    "template": """Break down this complex query into 3-4 specific sub-questions:
                    
                    Query: {input}
                    
                    Sub-questions:"""
                },
                {
                    "template": """Answer each of the following sub-questions thoroughly:
                    
                    Questions: {input}
                    
                    Detailed answers:"""
                },
                {
                    "template": """Synthesize these detailed answers into a cohesive response to the original query:
                    
                    Original query: """ + user_query + """
                    
                    Detailed answers: {input}
                    
                    Synthesized response:"""
                }
            ]
            
            result = manager.execute_sequential_chain(complex_steps, user_query)
            return result.get("final_output", "Processing failed")
    
    return assess_and_route

def create_content_pipeline_chain(llm):
    """Create an advanced content creation pipeline with refinement."""
    
    def content_pipeline(topic: str, target_audience: str, content_type: str) -> Dict[str, str]:
        """Execute multi-stage content creation workflow."""
        
        manager = PromptChainManager(llm)
        
        pipeline_steps = [
            {
                "template": """Research {topic} for {audience}. Create an outline with:
                1. Key concepts to cover  
                2. 5 main sections
                3. Supporting details for each section
                
                Topic: {topic}
                Audience: {audience}
                
                Outline:""".replace("{topic}", topic).replace("{audience}", target_audience)
            },
            {
                "template": """Using the following outline, write detailed content for a {content_type}.
                Make each section comprehensive but accessible:
                
                Outline: {input}
                
                Detailed content:""".replace("{content_type}", content_type)
            },
            {
                "template": """Review the following content for {audience}. Improve:
                1. Clarity and readability
                2. Flow between sections  
                3. Engagement level
                
                Original content: {input}
                
                Refined content:""".replace("{audience}", target_audience)
            }
        ]
        
        result = manager.execute_sequential_chain(pipeline_steps, f"Topic: {topic}")
        
        if result.get("success"):
            return {
                "outline": result["results"][0]["output"] if len(result["results"]) > 0 else "",
                "detailed_content": result["results"][1]["output"] if len(result["results"]) > 1 else "",
                "final_content": result["final_output"],
                "execution_history": result["history"]
            }
        else:
            return {"error": result.get("error", "Pipeline execution failed")}
    
    return content_pipeline

# Validation functions for common use cases
def validate_summary_length(text: str, max_words: int = 100) -> bool:
    """Validate that summary doesn't exceed word limit."""
    return len(text.split()) <= max_words

def validate_json_structure(text: str) -> bool:
    """Validate that output contains valid JSON structure."""
    import json
    try:
        json.loads(text.strip())
        return True
    except (json.JSONDecodeError, ValueError):
        return False

def validate_bullet_format(text: str) -> bool:
    """Validate that output is formatted as bullet points."""
    lines = text.strip().split('\n')
    bullet_chars = ['•', '-', '*', '1.', '2.', '3.']
    return any(any(line.strip().startswith(char) for char in bullet_chars) for line in lines)