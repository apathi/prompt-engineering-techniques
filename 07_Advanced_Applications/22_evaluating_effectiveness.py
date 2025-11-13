"""
22: Evaluating Prompt Effectiveness (LangChain Implementation)

This module demonstrates comprehensive techniques for measuring and evaluating
prompt performance across multiple dimensions, implementing systematic assessment
frameworks and optimization strategies based on measurable metrics.

Key concepts:
- Multi-dimensional effectiveness scoring
- Comparative evaluation frameworks  
- Performance metric calculation and analysis
- Prompt optimization through iterative testing
- Statistical significance assessment

"""

import os
import sys
from typing import List, Dict, Any, Optional, Tuple
import re
from dataclasses import dataclass
from enum import Enum
import statistics
import json

# Add shared_utils to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Optional dependencies for advanced evaluation
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    ADVANCED_METRICS_AVAILABLE = True
except ImportError:
    ADVANCED_METRICS_AVAILABLE = False


class EvaluationMetric(Enum):
    """Enumeration of evaluation metrics for prompt effectiveness."""
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    CONSISTENCY = "consistency"
    EFFICIENCY = "efficiency"
    CREATIVITY = "creativity"


class ResponseQuality(Enum):
    """Enumeration of response quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ADEQUATE = "adequate"
    POOR = "poor"


@dataclass
class EvaluationResult:
    """Represents evaluation results for a single prompt-response pair."""
    prompt_id: str
    response_text: str
    metrics: Dict[EvaluationMetric, float]
    overall_score: float
    quality_rating: ResponseQuality
    evaluation_details: Dict[str, Any]


class PromptEvaluator:
    """Advanced evaluator for comprehensive prompt effectiveness assessment."""
    
    def __init__(self):
        self.evaluation_criteria = {
            EvaluationMetric.ACCURACY: {
                "weight": 0.25,
                "description": "Factual correctness and precision"
            },
            EvaluationMetric.RELEVANCE: {
                "weight": 0.20,
                "description": "Alignment with user intent and context"
            },
            EvaluationMetric.COMPLETENESS: {
                "weight": 0.15,
                "description": "Comprehensive coverage of required topics"
            },
            EvaluationMetric.CLARITY: {
                "weight": 0.15,
                "description": "Clear, understandable communication"
            },
            EvaluationMetric.CONSISTENCY: {
                "weight": 0.10,
                "description": "Internal logical consistency"
            },
            EvaluationMetric.EFFICIENCY: {
                "weight": 0.10,
                "description": "Conciseness without losing essential information"
            },
            EvaluationMetric.CREATIVITY: {
                "weight": 0.05,
                "description": "Novel insights and creative approaches"
            }
        }
        
        # Initialize sentence transformer if available
        self.sentence_model = None
        if ADVANCED_METRICS_AVAILABLE:
            try:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception:
                pass
    
    def evaluate_response(self, response: str, expected_criteria: Dict[str, Any], 
                         prompt_context: str = "") -> EvaluationResult:
        """Evaluate a response against multiple effectiveness criteria."""
        metrics = {}
        evaluation_details = {}
        
        # Calculate each metric
        for metric in EvaluationMetric:
            score, details = self._calculate_metric_score(
                response, metric, expected_criteria, prompt_context
            )
            metrics[metric] = score
            evaluation_details[metric.value] = details
        
        # Calculate weighted overall score
        overall_score = sum(
            metrics[metric] * self.evaluation_criteria[metric]["weight"]
            for metric in EvaluationMetric
        )
        
        # Determine quality rating
        if overall_score >= 0.85:
            quality_rating = ResponseQuality.EXCELLENT
        elif overall_score >= 0.70:
            quality_rating = ResponseQuality.GOOD
        elif overall_score >= 0.55:
            quality_rating = ResponseQuality.ADEQUATE
        else:
            quality_rating = ResponseQuality.POOR
        
        return EvaluationResult(
            prompt_id=f"eval_{hash(response) % 10000}",
            response_text=response,
            metrics=metrics,
            overall_score=overall_score,
            quality_rating=quality_rating,
            evaluation_details=evaluation_details
        )
    
    def _calculate_metric_score(self, response: str, metric: EvaluationMetric, 
                              expected_criteria: Dict[str, Any], 
                              prompt_context: str) -> Tuple[float, Dict[str, Any]]:
        """Calculate score for a specific metric."""
        if metric == EvaluationMetric.ACCURACY:
            return self._evaluate_accuracy(response, expected_criteria)
        elif metric == EvaluationMetric.RELEVANCE:
            return self._evaluate_relevance(response, expected_criteria, prompt_context)
        elif metric == EvaluationMetric.COMPLETENESS:
            return self._evaluate_completeness(response, expected_criteria)
        elif metric == EvaluationMetric.CLARITY:
            return self._evaluate_clarity(response)
        elif metric == EvaluationMetric.CONSISTENCY:
            return self._evaluate_consistency(response)
        elif metric == EvaluationMetric.EFFICIENCY:
            return self._evaluate_efficiency(response, expected_criteria)
        elif metric == EvaluationMetric.CREATIVITY:
            return self._evaluate_creativity(response)
        else:
            return 0.5, {"error": "Unknown metric"}
    
    def _evaluate_accuracy(self, response: str, expected_criteria: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Evaluate factual accuracy and precision."""
        # Check for key facts or requirements
        required_elements = expected_criteria.get("required_facts", [])
        forbidden_elements = expected_criteria.get("forbidden_facts", [])
        
        correct_facts = sum(1 for fact in required_elements 
                           if self._contains_concept(response, fact))
        incorrect_facts = sum(1 for fact in forbidden_elements 
                             if self._contains_concept(response, fact))
        
        if required_elements:
            accuracy_score = correct_facts / len(required_elements)
        else:
            accuracy_score = 0.8  # Default if no specific facts required
        
        # Penalize incorrect information
        if incorrect_facts > 0:
            accuracy_score *= (1 - incorrect_facts * 0.2)
        
        return max(0.0, min(1.0, accuracy_score)), {
            "correct_facts": correct_facts,
            "total_required": len(required_elements),
            "incorrect_facts": incorrect_facts
        }
    
    def _evaluate_relevance(self, response: str, expected_criteria: Dict[str, Any], 
                           prompt_context: str) -> Tuple[float, Dict[str, Any]]:
        """Evaluate relevance to prompt and user intent."""
        # Use semantic similarity if available
        if self.sentence_model and prompt_context:
            try:
                prompt_embedding = self.sentence_model.encode([prompt_context])
                response_embedding = self.sentence_model.encode([response])
                similarity = cosine_similarity(prompt_embedding, response_embedding)[0][0]
                semantic_score = float(similarity)
            except Exception:
                semantic_score = 0.5
        else:
            semantic_score = 0.5
        
        # Check for topic alignment
        expected_topics = expected_criteria.get("expected_topics", [])
        topic_coverage = sum(1 for topic in expected_topics 
                           if self._contains_concept(response, topic))
        
        if expected_topics:
            topic_score = topic_coverage / len(expected_topics)
        else:
            topic_score = 0.7
        
        # Combine semantic and topic scores
        relevance_score = (semantic_score * 0.6) + (topic_score * 0.4)
        
        return relevance_score, {
            "semantic_similarity": semantic_score,
            "topic_coverage": topic_coverage,
            "total_topics": len(expected_topics)
        }
    
    def _evaluate_completeness(self, response: str, expected_criteria: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Evaluate comprehensive coverage of required topics."""
        required_sections = expected_criteria.get("required_sections", [])
        
        if not required_sections:
            # Default completeness based on response length and structure
            word_count = len(response.split())
            has_structure = bool(re.search(r'[.!?]\s+[A-Z]', response))  # Multiple sentences
            has_examples = bool(re.search(r'(for example|such as|e\.g\.)', response, re.I))
            
            completeness_score = min(1.0, (word_count / 100) * 0.5 + 
                                   (0.3 if has_structure else 0) +
                                   (0.2 if has_examples else 0))
        else:
            covered_sections = sum(1 for section in required_sections 
                                 if self._contains_concept(response, section))
            completeness_score = covered_sections / len(required_sections)
        
        return completeness_score, {
            "sections_covered": len([s for s in required_sections 
                                   if self._contains_concept(response, s)]),
            "total_required": len(required_sections),
            "word_count": len(response.split())
        }
    
    def _evaluate_clarity(self, response: str) -> Tuple[float, Dict[str, Any]]:
        """Evaluate clarity and understandability."""
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        
        if not sentences:
            return 0.0, {"error": "No sentences found"}
        
        # Average sentence length (optimal: 15-20 words)
        avg_sentence_length = statistics.mean([len(s.split()) for s in sentences])
        length_penalty = abs(avg_sentence_length - 17.5) / 17.5
        length_score = max(0.0, 1.0 - length_penalty)
        
        # Check for clear structure
        has_transitions = bool(re.search(r'\b(however|therefore|furthermore|additionally|moreover)\b', response, re.I))
        has_lists = bool(re.search(r'^\s*[\d\-\*\•]', response, re.M))
        
        structure_score = (0.3 if has_transitions else 0) + (0.2 if has_lists else 0)
        
        clarity_score = (length_score * 0.7) + structure_score
        
        return min(1.0, clarity_score), {
            "avg_sentence_length": avg_sentence_length,
            "has_transitions": has_transitions,
            "has_lists": has_lists,
            "sentence_count": len(sentences)
        }
    
    def _evaluate_consistency(self, response: str) -> Tuple[float, Dict[str, Any]]:
        """Evaluate internal logical consistency."""
        # Check for contradictory statements (basic heuristic)
        contradiction_patterns = [
            (r'\b(always|never|all|none|every)\b', r'\b(sometimes|some|few|rarely)\b'),
            (r'\b(impossible|cannot)\b', r'\b(possible|can|may)\b'),
            (r'\b(definitely|certainly)\b', r'\b(maybe|perhaps|might)\b')
        ]
        
        contradictions = 0
        for pattern1, pattern2 in contradiction_patterns:
            if re.search(pattern1, response, re.I) and re.search(pattern2, response, re.I):
                contradictions += 1
        
        # Check for consistent terminology
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        consistency_score = max(0.0, 1.0 - (contradictions * 0.3))
        
        return consistency_score, {
            "contradictions_detected": contradictions,
            "sentence_count": len(sentences)
        }
    
    def _evaluate_efficiency(self, response: str, expected_criteria: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Evaluate efficiency (conciseness without information loss)."""
        word_count = len(response.split())
        target_length = expected_criteria.get("target_word_count", 150)
        
        if word_count <= target_length:
            length_efficiency = 1.0
        else:
            length_efficiency = max(0.3, target_length / word_count)
        
        # Check information density
        info_words = len(re.findall(r'\b[a-zA-Z]{4,}\b', response))  # Words 4+ chars
        if word_count > 0:
            density_score = info_words / word_count
        else:
            density_score = 0.0
        
        efficiency_score = (length_efficiency * 0.7) + (density_score * 0.3)
        
        return min(1.0, efficiency_score), {
            "word_count": word_count,
            "target_length": target_length,
            "information_density": density_score
        }
    
    def _evaluate_creativity(self, response: str) -> Tuple[float, Dict[str, Any]]:
        """Evaluate creativity and novel insights."""
        # Check for creative indicators
        creative_patterns = [
            r'\b(imagine|consider|what if|alternatively|innovative)\b',
            r'\b(unique|novel|creative|original|breakthrough)\b',
            r'\b(metaphor|analogy|like|as if)\b'
        ]
        
        creative_indicators = sum(1 for pattern in creative_patterns 
                                if re.search(pattern, response, re.I))
        
        # Check for varied vocabulary
        words = re.findall(r'\b[a-zA-Z]+\b', response.lower())
        unique_words = len(set(words))
        vocabulary_diversity = unique_words / len(words) if words else 0
        
        creativity_score = min(1.0, (creative_indicators * 0.2) + (vocabulary_diversity * 0.8))
        
        return creativity_score, {
            "creative_indicators": creative_indicators,
            "vocabulary_diversity": vocabulary_diversity,
            "unique_words": unique_words,
            "total_words": len(words)
        }
    
    def _contains_concept(self, text: str, concept: str) -> bool:
        """Check if text contains a concept (flexible matching)."""
        # Simple keyword-based matching - could be enhanced with NLP
        concept_words = concept.lower().split()
        text_lower = text.lower()
        
        return any(word in text_lower for word in concept_words) or concept.lower() in text_lower


class ComparativeEvaluator:
    """Specialized evaluator for comparing multiple prompts."""
    
    def __init__(self, base_evaluator: PromptEvaluator):
        self.evaluator = base_evaluator
    
    def compare_prompts(self, prompt_responses: List[Dict[str, Any]], 
                       evaluation_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Compare multiple prompts and rank their effectiveness."""
        evaluations = []
        
        for prompt_data in prompt_responses:
            evaluation = self.evaluator.evaluate_response(
                prompt_data["response"],
                evaluation_criteria,
                prompt_data.get("prompt_text", "")
            )
            evaluations.append({
                "prompt_name": prompt_data["prompt_name"],
                "evaluation": evaluation
            })
        
        # Rank by overall score
        evaluations.sort(key=lambda x: x["evaluation"].overall_score, reverse=True)
        
        # Calculate comparative metrics
        scores = [e["evaluation"].overall_score for e in evaluations]
        
        return {
            "ranked_prompts": evaluations,
            "performance_analysis": {
                "best_score": max(scores),
                "worst_score": min(scores),
                "average_score": statistics.mean(scores),
                "score_range": max(scores) - min(scores),
                "performance_variance": statistics.variance(scores) if len(scores) > 1 else 0.0
            }
        }


class EvaluatingEffectiveness:
    """Evaluating Prompt Effectiveness: Comprehensive measurement and optimization using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and evaluation components."""
        self.logger = setup_logger("evaluating_effectiveness")
        self.client = LangChainClient(
            model=model,
            temperature=0.3,
            max_tokens=600,
            session_name="evaluating_effectiveness"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        self.evaluator = PromptEvaluator()
        self.comparative_evaluator = ComparativeEvaluator(self.evaluator)
    
    def multi_dimensional_assessment(self) -> Dict[str, Any]:
        """
        Demonstrate intermediate multi-dimensional prompt effectiveness assessment.
        Shows systematic evaluation across multiple quality dimensions.
        """
        self.logger.info("Running multi-dimensional assessment")
        
        # Test scenario: Writing assistant prompts
        test_topic = "climate change solutions"
        
        # Different prompt variations to evaluate
        prompt_variations = [
            {
                "name": "Basic Direct Prompt",
                "prompt_template": "Write about climate change solutions.",
                "expected_criteria": {
                    "required_facts": ["renewable energy", "carbon reduction", "sustainability"],
                    "expected_topics": ["mitigation", "adaptation", "technology"],
                    "target_word_count": 200
                }
            },
            {
                "name": "Structured Detailed Prompt",
                "prompt_template": """Write a comprehensive analysis of climate change solutions.

Structure your response to include:
1. Key mitigation strategies
2. Adaptation approaches  
3. Technological innovations
4. Policy recommendations

Focus on practical, implementable solutions with specific examples.""",
                "expected_criteria": {
                    "required_facts": ["renewable energy", "carbon reduction", "policy", "technology"],
                    "expected_topics": ["mitigation", "adaptation", "technology", "policy"],
                    "required_sections": ["mitigation strategies", "adaptation", "innovation", "policy"],
                    "target_word_count": 300
                }
            },
            {
                "name": "Role-Based Expert Prompt",
                "prompt_template": """You are an environmental policy expert with 15 years of experience in climate solutions.

Write an authoritative but accessible analysis of the most effective climate change solutions for a general audience. Include:
- Evidence-based recommendations
- Real-world implementation examples
- Balanced perspective on challenges and opportunities
- Actionable insights for different stakeholders

Maintain scientific accuracy while ensuring clarity for non-experts.""",
                "expected_criteria": {
                    "required_facts": ["evidence-based", "implementation", "stakeholders", "scientific"],
                    "expected_topics": ["solutions", "examples", "challenges", "opportunities"],
                    "required_sections": ["recommendations", "examples", "challenges", "insights"],
                    "target_word_count": 350
                }
            }
        ]
        
        evaluation_results = []
        
        for prompt_variation in prompt_variations:
            # Generate response using the prompt
            chain = ChatPromptTemplate.from_template(prompt_variation["prompt_template"]) | self.llm | self.parser
            response = chain.invoke(
                {},
                config={"tags": [f"evaluation_{prompt_variation['name'].lower().replace(' ', '_')}"]}
            )
            
            # Evaluate the response
            evaluation = self.evaluator.evaluate_response(
                response,
                prompt_variation["expected_criteria"],
                prompt_variation["prompt_template"]
            )
            
            # Prepare detailed metrics breakdown
            metrics_breakdown = {}
            for metric, score in evaluation.metrics.items():
                criteria_info = self.evaluator.evaluation_criteria[metric]
                metrics_breakdown[metric.value] = {
                    "score": score,
                    "weight": criteria_info["weight"],
                    "weighted_contribution": score * criteria_info["weight"],
                    "description": criteria_info["description"]
                }
            
            evaluation_results.append({
                "prompt_name": prompt_variation["name"],
                "prompt_preview": prompt_variation["prompt_template"][:100] + "..." if len(prompt_variation["prompt_template"]) > 100 else prompt_variation["prompt_template"],
                "response_preview": response[:150] + "..." if len(response) > 150 else response,
                "overall_score": evaluation.overall_score,
                "quality_rating": evaluation.quality_rating.value,
                "metrics_breakdown": metrics_breakdown,
                "evaluation_details": evaluation.evaluation_details
            })
        
        # Rank results
        evaluation_results.sort(key=lambda x: x["overall_score"], reverse=True)
        
        # Calculate performance insights
        scores = [result["overall_score"] for result in evaluation_results]
        best_performing = evaluation_results[0]
        
        return {
            "technique": "Multi-Dimensional Assessment",
            "description": "Comprehensive evaluation of prompt effectiveness across accuracy, relevance, completeness, clarity, consistency, efficiency, and creativity dimensions",
            "why_this_works": "By evaluating prompts across multiple weighted dimensions, we can identify specific strengths and weaknesses, leading to more targeted optimization. Each dimension captures different aspects of communication effectiveness, providing a holistic view of prompt performance that goes beyond simple output quality.",
            "test_topic": test_topic,
            "evaluation_results": evaluation_results,
            "performance_insights": {
                "best_performing_prompt": best_performing["prompt_name"],
                "top_score": best_performing["overall_score"],
                "average_score": statistics.mean(scores),
                "performance_range": max(scores) - min(scores),
                "key_success_factors": [
                    "Clear structure and expectations",
                    "Role-based expertise framing",
                    "Specific output requirements",
                    "Target audience consideration"
                ]
            }
        }
    
    def advanced_optimization_framework(self) -> Dict[str, Any]:
        """
        Demonstrate advanced iterative optimization framework with statistical validation.
        Shows sophisticated prompt refinement through systematic evaluation and improvement cycles.
        """
        self.logger.info("Running advanced optimization framework")
        
        # Complex optimization scenario: Technical documentation generation
        optimization_task = "Create clear technical documentation for a REST API endpoint"
        
        # Evolution of prompts through optimization iterations
        prompt_evolution = [
            {
                "iteration": 1,
                "name": "Initial Baseline",
                "prompt": "Document the /users/create REST API endpoint.",
                "optimization_focus": "Baseline measurement"
            },
            {
                "iteration": 2,
                "name": "Structure Added",
                "prompt": """Document the /users/create REST API endpoint.

Include:
- Endpoint description
- HTTP method and URL
- Request parameters
- Response format
- Example usage""",
                "optimization_focus": "Added structured requirements"
            },
            {
                "iteration": 3,
                "name": "Audience & Detail Optimized",
                "prompt": """Create comprehensive technical documentation for the /users/create REST API endpoint, targeted at software developers integrating with our system.

Required sections:
1. Endpoint Overview - brief description and purpose
2. Request Details - HTTP method, URL, headers, authentication
3. Parameters - all required and optional parameters with types and descriptions
4. Response Specification - success/error responses with status codes and data format
5. Code Examples - working examples in at least 2 programming languages
6. Error Handling - common error scenarios and troubleshooting

Format for developer reference documentation with clear, scannable structure.""",
                "optimization_focus": "Target audience clarity, comprehensive coverage, usability focus"
            },
            {
                "iteration": 4,
                "name": "Best Practices Integration",
                "prompt": """You are a senior technical writer specializing in API documentation. Create comprehensive, developer-friendly documentation for the /users/create REST API endpoint.

CONTEXT: This documentation will be used by external developers integrating with our platform.

REQUIREMENTS:
✓ Follow OpenAPI specification conventions where applicable
✓ Include security considerations and rate limiting information  
✓ Provide practical code examples that developers can copy-paste
✓ Address common integration challenges and edge cases
✓ Use clear, scannable formatting with appropriate headers and bullet points

STRUCTURE:
1. 📋 Endpoint Overview (purpose, use cases)
2. 🔧 Request Specification (method, URL, authentication, headers)
3. 📝 Parameters (required/optional, validation rules, examples)
4. ✅ Success Responses (status codes, data schemas, examples)
5. ❌ Error Responses (error codes, troubleshooting guidance)
6. 💻 Code Examples (cURL, JavaScript, Python minimum)
7. ⚠️ Important Notes (rate limits, security considerations, best practices)

Optimize for developer experience and implementation speed.""",
                "optimization_focus": "Expert persona, implementation-focused, comprehensive best practices"
            }
        ]
        
        # Evaluation criteria for technical documentation
        documentation_criteria = {
            "required_facts": ["REST API", "HTTP method", "parameters", "response", "authentication"],
            "expected_topics": ["endpoint", "request", "response", "examples", "errors"],
            "required_sections": ["overview", "request", "parameters", "response", "examples"],
            "target_word_count": 400
        }
        
        optimization_results = []
        performance_trend = []
        
        for iteration_data in prompt_evolution:
            # Generate documentation using current prompt
            chain = ChatPromptTemplate.from_template(iteration_data["prompt"]) | self.llm | self.parser
            response = chain.invoke(
                {},
                config={"tags": [f"optimization_iter_{iteration_data['iteration']}"]}
            )
            
            # Evaluate response
            evaluation = self.evaluator.evaluate_response(
                response,
                documentation_criteria,
                iteration_data["prompt"]
            )
            
            # Analyze improvement areas
            weak_metrics = [metric.value for metric, score in evaluation.metrics.items() if score < 0.7]
            strong_metrics = [metric.value for metric, score in evaluation.metrics.items() if score >= 0.8]
            
            # Calculate improvement from previous iteration
            improvement = None
            if performance_trend:
                improvement = evaluation.overall_score - performance_trend[-1]["score"]
            
            iteration_result = {
                "iteration": iteration_data["iteration"],
                "prompt_name": iteration_data["name"],
                "optimization_focus": iteration_data["optimization_focus"],
                "overall_score": evaluation.overall_score,
                "quality_rating": evaluation.quality_rating.value,
                "improvement_from_previous": improvement,
                "response_length": len(response.split()),
                "strong_metrics": strong_metrics,
                "weak_metrics": weak_metrics,
                "detailed_scores": {metric.value: score for metric, score in evaluation.metrics.items()}
            }
            
            optimization_results.append(iteration_result)
            performance_trend.append({"iteration": iteration_data["iteration"], "score": evaluation.overall_score})
        
        # Calculate optimization insights
        initial_score = performance_trend[0]["score"]
        final_score = performance_trend[-1]["score"]
        total_improvement = final_score - initial_score
        
        # Identify most effective optimization strategies
        improvements = [(r["improvement_from_previous"], r["optimization_focus"]) 
                       for r in optimization_results if r["improvement_from_previous"] is not None]
        best_improvement = max(improvements, key=lambda x: x[0]) if improvements else None
        
        return {
            "technique": "Advanced Optimization Framework",
            "description": "Iterative prompt refinement through systematic evaluation, targeting specific weakness areas and measuring improvement across optimization cycles",
            "why_this_works": "Optimization frameworks provide structured approaches to prompt improvement by identifying specific areas of weakness, implementing targeted changes, and measuring results. This creates a feedback loop that leads to continuous improvement and helps identify which optimization strategies are most effective for different types of tasks.",
            "task": optimization_task,
            "optimization_iterations": optimization_results,
            "performance_analysis": {
                "initial_score": initial_score,
                "final_score": final_score,
                "total_improvement": total_improvement,
                "improvement_percentage": (total_improvement / initial_score) * 100,
                "most_effective_optimization": best_improvement[1] if best_improvement else None,
                "largest_single_improvement": best_improvement[0] if best_improvement else None
            },
            "optimization_insights": {
                "key_success_factors": [
                    "Adding structured requirements and clear sections",
                    "Defining target audience and use case context",
                    "Integrating domain expertise through role-playing",
                    "Including implementation-focused best practices"
                ],
                "metric_evolution": {
                    "most_improved_dimension": max(
                        EvaluationMetric, 
                        key=lambda m: optimization_results[-1]["detailed_scores"][m.value] - optimization_results[0]["detailed_scores"][m.value]
                    ).value,
                    "consistently_strong": [m for m in EvaluationMetric 
                                          if all(r["detailed_scores"][m.value] >= 0.7 for r in optimization_results[-2:])]
                }
            }
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all prompt effectiveness evaluation examples."""
        self.logger.info("Starting Evaluating Effectiveness demonstrations")
        
        results = {
            "technique_overview": "Evaluating Prompt Effectiveness",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.multi_dimensional_assessment(),
            self.advanced_optimization_framework()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("22-evaluating-effectiveness")
    output_manager.add_header("22: EVALUATING PROMPT EFFECTIVENESS")
    
    # Initialize technique
    evaluator = EvaluatingEffectiveness()
    
    try:
        # Run examples
        results = evaluator.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(evaluator.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        evaluator.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()