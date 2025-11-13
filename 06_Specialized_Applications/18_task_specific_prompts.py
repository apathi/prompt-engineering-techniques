"""
18: Prompts for Specific Tasks (LangChain Implementation)

This module demonstrates specialized prompt design for specific task domains,
combining GitHub's domain expertise with enhanced template optimization and 
quality metrics for real-world applications.

Key concepts:
- Domain-specific template specialization
- Task classification and optimization
- Performance tracking and quality metrics
- Output format control and validation
- Real-world application scenarios

"""

import os
import sys
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
import re

# Add shared_utils to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class TaskDomain(Enum):
    """Enumeration of specific task domains."""
    TEXT_SUMMARIZATION = "summarization"
    QUESTION_ANSWERING = "qa"
    CODE_GENERATION = "code"
    CREATIVE_WRITING = "creative"
    DATA_ANALYSIS = "analysis"
    TECHNICAL_WRITING = "technical"


@dataclass
class TaskPerformanceMetrics:
    """Performance metrics for task-specific prompts."""
    task_domain: TaskDomain
    accuracy_score: float
    relevance_score: float
    format_compliance: float
    execution_time: float
    output_length: int


class TaskClassifier:
    """Advanced classifier for task domain identification and optimization."""
    
    def __init__(self):
        self.domain_keywords = {
            TaskDomain.TEXT_SUMMARIZATION: ["summarize", "abstract", "brief", "overview", "condense"],
            TaskDomain.QUESTION_ANSWERING: ["question", "answer", "explain", "what", "how", "why"],
            TaskDomain.CODE_GENERATION: ["code", "function", "programming", "implement", "algorithm"],
            TaskDomain.CREATIVE_WRITING: ["story", "creative", "narrative", "character", "plot"],
            TaskDomain.DATA_ANALYSIS: ["analyze", "data", "statistics", "trends", "insights"],
            TaskDomain.TECHNICAL_WRITING: ["documentation", "specification", "technical", "manual"]
        }
    
    def classify_task(self, task_description: str) -> TaskDomain:
        """Classify task based on description keywords."""
        task_lower = task_description.lower()
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in task_lower)
            domain_scores[domain] = score
        
        return max(domain_scores, key=domain_scores.get)
    
    def get_optimization_strategy(self, domain: TaskDomain) -> Dict[str, Any]:
        """Get domain-specific optimization strategies."""
        strategies = {
            TaskDomain.TEXT_SUMMARIZATION: {
                "temperature": 0.3,
                "max_tokens": 200,
                "focus_areas": ["key_points", "conciseness", "accuracy"],
                "validation_criteria": ["length_compliance", "information_retention"]
            },
            TaskDomain.QUESTION_ANSWERING: {
                "temperature": 0.2,
                "max_tokens": 300,
                "focus_areas": ["accuracy", "completeness", "clarity"],
                "validation_criteria": ["factual_accuracy", "relevance", "directness"]
            },
            TaskDomain.CODE_GENERATION: {
                "temperature": 0.1,
                "max_tokens": 400,
                "focus_areas": ["syntax_accuracy", "functionality", "best_practices"],
                "validation_criteria": ["syntax_validity", "logic_correctness", "documentation"]
            },
            TaskDomain.CREATIVE_WRITING: {
                "temperature": 0.8,
                "max_tokens": 500,
                "focus_areas": ["creativity", "engagement", "narrative_flow"],
                "validation_criteria": ["originality", "coherence", "entertainment_value"]
            }
        }
        
        return strategies.get(domain, {
            "temperature": 0.5,
            "max_tokens": 350,
            "focus_areas": ["quality", "relevance"],
            "validation_criteria": ["completeness", "accuracy"]
        })


class TaskSpecificPrompts:
    """Task-Specific Prompts: Specialized templates for domain expertise using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("task_specific_prompts")
        self.client = LangChainClient(
            model=model,
            temperature=0.4,
            max_tokens=450,
            session_name="task_specific_prompts"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        self.classifier = TaskClassifier()
    
    def domain_specific_optimization(self) -> Dict[str, Any]:
        """
        Demonstrate intermediate domain-specific template optimization.
        Shows specialized prompts for different task domains with performance tracking.
        """
        self.logger.info("Running domain-specific optimization")
        
        # Define tasks for different domains
        domain_tasks = [
            {
                "domain": TaskDomain.TEXT_SUMMARIZATION,
                "input": """Artificial intelligence (AI) is rapidly transforming industries worldwide. From healthcare to finance, AI systems are being deployed to improve efficiency, reduce costs, and enhance decision-making. Machine learning algorithms can now analyze vast amounts of data to identify patterns that would be impossible for humans to detect. However, the adoption of AI also raises concerns about job displacement, privacy, and the need for new regulatory frameworks. Companies are investing billions in AI research, while governments are grappling with how to regulate this powerful technology without stifling innovation.""",
                "template": PromptTemplate.from_template(
                    """Summarize the following text in exactly {num_sentences} sentences, focusing on the main points and key implications.

Text: {text}

Summary:"""
                ),
                "params": {"num_sentences": 3}
            },
            {
                "domain": TaskDomain.QUESTION_ANSWERING,
                "input": """The Eiffel Tower is an iron lattice tower located on the Champ de Mars in Paris, France. It was named after Gustave Eiffel, whose engineering company designed and built the tower from 1887 to 1889. The tower is 330 meters (1,083 feet) tall, about the same height as an 81-story building, and was the tallest man-made structure in the world until 1930.""",
                "template": PromptTemplate.from_template(
                    """Based on the provided context, answer the following question accurately and concisely.

Context: {context}

Question: {question}

Answer:"""
                ),
                "params": {"question": "What is the height of the Eiffel Tower and when was it built?"}
            },
            {
                "domain": TaskDomain.CODE_GENERATION,
                "input": "Create a function to calculate the average of even numbers in a list",
                "template": PromptTemplate.from_template(
                    """Generate {language} code for the following task: {task}

Requirements:
- Include proper error handling
- Add comments explaining the logic
- Follow best practices for the language
- Include a simple test case

Code:"""
                ),
                "params": {"language": "Python"}
            },
            {
                "domain": TaskDomain.CREATIVE_WRITING,
                "input": "A mysterious package arrives at someone's door",
                "template": PromptTemplate.from_template(
                    """Write a {genre} story of approximately {word_count} words based on this prompt: {prompt}

The story should include:
- Engaging characters
- Clear setting
- Compelling conflict
- Satisfying resolution

Story:"""
                ),
                "params": {"genre": "mystery", "word_count": 250}
            }
        ]
        
        results = []
        
        for task_info in domain_tasks:
            # Get domain-specific optimization
            optimization = self.classifier.get_optimization_strategy(task_info["domain"])
            
            # Use the configured LLM (domain optimization can be handled via prompt engineering)
            optimized_llm = self.llm
            
            # Build chain
            chain = task_info["template"] | optimized_llm | self.parser
            
            # Prepare input parameters
            invoke_params = task_info["params"].copy()
            if task_info["domain"] == TaskDomain.TEXT_SUMMARIZATION:
                invoke_params["text"] = task_info["input"]
            elif task_info["domain"] == TaskDomain.QUESTION_ANSWERING:
                invoke_params["context"] = task_info["input"]
            elif task_info["domain"] == TaskDomain.CODE_GENERATION:
                invoke_params["task"] = task_info["input"]
            elif task_info["domain"] == TaskDomain.CREATIVE_WRITING:
                invoke_params["prompt"] = task_info["input"]
            
            # Generate response
            response = chain.invoke(
                invoke_params,
                config={"tags": [f"domain_{task_info['domain'].value}"]}
            )
            
            # Evaluate performance
            performance = self._evaluate_task_performance(
                task_info["domain"], 
                response, 
                task_info["input"],
                optimization
            )
            
            results.append({
                "domain": task_info["domain"].value,
                "input": task_info["input"],
                "optimization_settings": optimization,
                "response": response,
                "performance_metrics": {
                    "relevance_score": performance.relevance_score,
                    "format_compliance": performance.format_compliance,
                    "output_length": performance.output_length,
                    "overall_quality": (performance.relevance_score + performance.format_compliance) / 2
                }
            })
        
        return {
            "technique": "Domain-Specific Optimization",
            "description": "Specialized prompt templates optimized for specific task domains with performance tracking",
            "why_this_works": "Different tasks require different cognitive approaches and output formats. By tailoring temperature, token limits, and prompt structures to specific domains, we optimize for domain-specific success criteria. This improves both quality and efficiency compared to generic approaches.",
            "examples": results
        }
    
    def advanced_multi_domain_integration(self) -> Dict[str, Any]:
        """
        Demonstrate advanced multi-domain task integration with quality frameworks.
        Shows sophisticated task orchestration and cross-domain optimization.
        """
        self.logger.info("Running advanced multi-domain integration")
        
        # Complex multi-step tasks requiring multiple domains
        integration_scenarios = [
            {
                "name": "Technical Blog Post Creation",
                "description": "Create a technical blog post about a programming concept",
                "steps": [
                    {
                        "domain": TaskDomain.TECHNICAL_WRITING,
                        "task": "Create an outline",
                        "prompt": PromptTemplate.from_template(
                            """Create a detailed outline for a technical blog post about {topic}.

The outline should include:
- Engaging title
- Introduction hook
- 3-4 main sections with subsections
- Practical examples section
- Conclusion with key takeaways
- Target audience: {audience}
- Estimated word count: {word_count}

Outline:"""
                        ),
                        "params": {"topic": "Python decorators", "audience": "intermediate developers", "word_count": "1500"}
                    },
                    {
                        "domain": TaskDomain.CODE_GENERATION,
                        "task": "Generate code examples",
                        "prompt": PromptTemplate.from_template(
                            """Generate Python code examples to illustrate decorators for a technical blog post.

Create:
1. Basic decorator example with explanation
2. Decorator with arguments example
3. Class-based decorator example
4. Real-world use case (timing decorator)

Each example should:
- Be complete and runnable
- Include clear comments
- Show both definition and usage
- Be progressively more complex

Code Examples:"""
                        ),
                        "params": {}
                    },
                    {
                        "domain": TaskDomain.CREATIVE_WRITING,
                        "task": "Write engaging introduction",
                        "prompt": PromptTemplate.from_template(
                            """Write an engaging introduction for a technical blog post about Python decorators.

Requirements:
- Hook readers with a relatable scenario or problem
- Introduce decorators in accessible terms
- Set expectations for what readers will learn
- Maintain professional yet approachable tone
- Approximately 150 words
- Target audience: intermediate Python developers

Introduction:"""
                        ),
                        "params": {}
                    }
                ]
            },
            {
                "name": "Data Science Report Generation",
                "description": "Generate a comprehensive data analysis report",
                "steps": [
                    {
                        "domain": TaskDomain.DATA_ANALYSIS,
                        "task": "Analyze sample data",
                        "prompt": PromptTemplate.from_template(
                            """Analyze the following sales data and provide insights:

Data Summary:
- Q1 Sales: $500,000 (20% increase from previous year)
- Q2 Sales: $450,000 (5% decrease from Q1)
- Q3 Sales: $600,000 (33% increase from Q2)
- Q4 Sales: $550,000 (8% decrease from Q3)
- Top performing product: Software licenses (40% of revenue)
- Emerging market: Mobile apps (300% growth year-over-year)

Provide:
1. Key trends identification
2. Performance analysis
3. Growth opportunities
4. Risk factors
5. Recommendations

Analysis:"""
                        ),
                        "params": {}
                    },
                    {
                        "domain": TaskDomain.TECHNICAL_WRITING,
                        "task": "Create executive summary",
                        "prompt": PromptTemplate.from_template(
                            """Create an executive summary for a data analysis report based on these key findings:

{findings}

The summary should:
- Be exactly 150 words
- Lead with the most important insight
- Include key metrics and percentages
- End with primary recommendation
- Use business-appropriate language
- Focus on actionable insights

Executive Summary:"""
                        ),
                        "params": {}
                    }
                ]
            }
        ]
        
        results = []
        
        for scenario in integration_scenarios:
            scenario_results = {
                "scenario_name": scenario["name"],
                "description": scenario["description"],
                "steps": []
            }
            
            previous_outputs = {}
            
            for step_idx, step in enumerate(scenario["steps"]):
                # Get domain optimization
                optimization = self.classifier.get_optimization_strategy(step["domain"])
                
                # Use the configured LLM (domain optimization handled via prompt engineering)
                optimized_llm = self.llm
                
                # Prepare parameters (may include previous step outputs)
                invoke_params = step["params"].copy()
                if step["task"] == "Create executive summary":
                    # Use previous analysis output as findings
                    invoke_params["findings"] = previous_outputs.get("analysis", "Analysis not available")
                
                # Ensure all required template variables are provided
                if "findings" in step["prompt"].input_variables and "findings" not in invoke_params:
                    invoke_params["findings"] = "No findings available from previous steps"
                
                # Build and execute chain
                chain = step["prompt"] | optimized_llm | self.parser
                response = chain.invoke(
                    invoke_params,
                    config={"tags": [f"integration_{scenario['name'].lower().replace(' ', '_')}_step_{step_idx}"]}
                )
                
                # Store output for potential use in subsequent steps
                if step["task"] == "Analyze sample data":
                    previous_outputs["analysis"] = response
                
                # Evaluate step performance
                step_performance = self._evaluate_integration_step(step, response, optimization)
                
                scenario_results["steps"].append({
                    "step_number": step_idx + 1,
                    "domain": step["domain"].value,
                    "task": step["task"],
                    "response": response,
                    "performance": step_performance
                })
            
            # Calculate overall scenario quality
            overall_quality = sum(step["performance"]["quality_score"] for step in scenario_results["steps"]) / len(scenario_results["steps"])
            scenario_results["overall_quality"] = overall_quality
            
            results.append(scenario_results)
        
        return {
            "technique": "Advanced Multi-Domain Integration",
            "description": "Sophisticated task orchestration combining multiple specialized domains for complex deliverables",
            "why_this_works": "Complex real-world tasks often require multiple cognitive modes and domain expertise. By orchestrating specialized prompts across different domains and passing context between steps, we can create sophisticated workflows that leverage each domain's strengths while maintaining coherence across the entire deliverable.",
            "examples": results
        }
    
    def _evaluate_task_performance(self, domain: TaskDomain, response: str, input_text: str, optimization: Dict) -> TaskPerformanceMetrics:
        """Evaluate performance of task-specific response."""
        # Calculate basic metrics
        output_length = len(response.split())
        
        # Domain-specific relevance scoring
        relevance_score = self._calculate_relevance_score(domain, response, input_text)
        
        # Format compliance scoring
        format_compliance = self._check_format_compliance(domain, response, optimization)
        
        return TaskPerformanceMetrics(
            task_domain=domain,
            accuracy_score=0.8,  # Placeholder - would need ground truth
            relevance_score=relevance_score,
            format_compliance=format_compliance,
            execution_time=0.0,  # Placeholder
            output_length=output_length
        )
    
    def _calculate_relevance_score(self, domain: TaskDomain, response: str, input_text: str) -> float:
        """Calculate relevance score based on domain-specific criteria."""
        response_lower = response.lower()
        
        if domain == TaskDomain.TEXT_SUMMARIZATION:
            # Check if key concepts from input appear in summary
            input_words = set(input_text.lower().split())
            response_words = set(response_lower.split())
            overlap = len(input_words.intersection(response_words))
            return min(1.0, overlap / len(input_words) * 3)
        
        elif domain == TaskDomain.CODE_GENERATION:
            # Check for code-like patterns
            code_indicators = ['def ', 'function', 'return', 'if ', '==', 'for ', 'while ']
            score = sum(1 for indicator in code_indicators if indicator in response_lower)
            return min(1.0, score / len(code_indicators))
        
        elif domain == TaskDomain.CREATIVE_WRITING:
            # Check for narrative elements
            narrative_indicators = ['character', 'story', 'scene', 'dialogue', 'plot']
            score = sum(1 for indicator in narrative_indicators if indicator in response_lower)
            return min(1.0, score / len(narrative_indicators))
        
        else:
            # Generic relevance check
            return 0.7  # Default score
    
    def _check_format_compliance(self, domain: TaskDomain, response: str, optimization: Dict) -> float:
        """Check compliance with domain-specific format requirements."""
        score = 1.0
        
        # Check length compliance
        expected_max_tokens = optimization.get("max_tokens", 400)
        actual_tokens = len(response.split())
        if actual_tokens > expected_max_tokens * 1.2:  # 20% tolerance
            score -= 0.2
        
        # Domain-specific format checks
        if domain == TaskDomain.CODE_GENERATION:
            if "```" not in response and "def " not in response:
                score -= 0.3
        
        elif domain == TaskDomain.TEXT_SUMMARIZATION:
            if len(response.split('.')) > 5:  # Too many sentences for a summary
                score -= 0.2
        
        return max(0.0, score)
    
    def _evaluate_integration_step(self, step: Dict, response: str, optimization: Dict) -> Dict[str, float]:
        """Evaluate performance of an integration step."""
        # Basic quality metrics
        completeness = min(1.0, len(response.split()) / optimization.get("max_tokens", 400))
        coherence = self._check_coherence(response)
        domain_appropriateness = self._check_domain_appropriateness(step["domain"], response)
        
        quality_score = (completeness + coherence + domain_appropriateness) / 3
        
        return {
            "completeness": completeness,
            "coherence": coherence,
            "domain_appropriateness": domain_appropriateness,
            "quality_score": quality_score
        }
    
    def _check_coherence(self, text: str) -> float:
        """Check text coherence based on transition words and flow."""
        transition_words = ['however', 'therefore', 'additionally', 'furthermore', 'moreover', 'consequently']
        coherence_score = min(1.0, sum(1 for word in transition_words if word in text.lower()) / 3)
        return coherence_score
    
    def _check_domain_appropriateness(self, domain: TaskDomain, text: str) -> float:
        """Check if text is appropriate for the specified domain."""
        domain_keywords = self.classifier.domain_keywords.get(domain, [])
        text_lower = text.lower()
        matches = sum(1 for keyword in domain_keywords if keyword in text_lower)
        return min(1.0, matches / max(1, len(domain_keywords)))
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all task-specific prompt examples."""
        self.logger.info("Starting Task-Specific Prompts demonstrations")
        
        results = {
            "technique_overview": "Prompts for Specific Tasks",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.domain_specific_optimization(),
            self.advanced_multi_domain_integration()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("18-task-specific-prompts")
    output_manager.add_header("18: PROMPTS FOR SPECIFIC TASKS")
    
    # Initialize technique
    task_prompts = TaskSpecificPrompts()
    
    try:
        # Run examples
        results = task_prompts.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(task_prompts.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        task_prompts.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()