"""
17: Prompt Formatting and Structure (LangChain Implementation)

This module demonstrates comprehensive prompt formatting techniques and structural 
elements, exploring how different formats impact AI model responses and
optimizing for specific communication patterns.

Key concepts:
- Format taxonomy (Q&A, dialogue, instruction, completion)
- Structural element analysis (headings, lists, sections)
- Visual organization and whitespace management
- Template design patterns for reusability
- Format impact assessment and optimization

"""

import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Add shared_utils to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class PromptFormat(Enum):
    """Enumeration of different prompt format types."""
    QA_FORMAT = "qa"
    DIALOGUE_FORMAT = "dialogue"
    INSTRUCTION_FORMAT = "instruction"
    COMPLETION_FORMAT = "completion"
    STRUCTURED_FORMAT = "structured"


@dataclass
class FormatAnalysis:
    """Analysis results for a specific format type."""
    format_type: PromptFormat
    response_length: int
    clarity_score: float
    engagement_score: float
    structure_score: float
    response_text: str


class FormatAnalyzer:
    """Advanced analyzer for prompt format effectiveness."""
    
    def __init__(self):
        self.format_patterns = {
            "clarity_indicators": ["clear", "understand", "specific", "detailed"],
            "engagement_indicators": ["interesting", "engaging", "compelling", "captivating"],
            "structure_indicators": ["organized", "systematic", "structured", "coherent"]
        }
    
    def analyze_response(self, response: str, format_type: PromptFormat) -> FormatAnalysis:
        """Analyze response quality across multiple dimensions."""
        # Calculate basic metrics
        response_length = len(response.split())
        
        # Score clarity (presence of clear explanatory language)
        clarity_score = self._calculate_indicator_score(response, "clarity_indicators")
        
        # Score engagement (conversational and interesting language)
        engagement_score = self._calculate_indicator_score(response, "engagement_indicators")
        
        # Score structure (organized presentation)
        structure_score = self._calculate_structure_score(response)
        
        return FormatAnalysis(
            format_type=format_type,
            response_length=response_length,
            clarity_score=clarity_score,
            engagement_score=engagement_score,
            structure_score=structure_score,
            response_text=response
        )
    
    def _calculate_indicator_score(self, response: str, indicator_type: str) -> float:
        """Calculate score based on presence of indicator words."""
        indicators = self.format_patterns[indicator_type]
        response_lower = response.lower()
        
        matches = sum(1 for indicator in indicators if indicator in response_lower)
        return min(1.0, matches / len(indicators))
    
    def _calculate_structure_score(self, response: str) -> float:
        """Calculate structure score based on formatting elements."""
        score = 0.0
        
        # Check for paragraph breaks
        if '\n\n' in response:
            score += 0.3
        
        # Check for lists or bullet points
        if any(marker in response for marker in ['•', '-', '*', '1.', '2.', '3.']):
            score += 0.3
        
        # Check for headings or sections
        if any(marker in response for marker in ['#', '**', '__']):
            score += 0.2
        
        # Check for logical flow indicators
        flow_words = ['first', 'second', 'then', 'next', 'finally', 'therefore']
        if any(word in response.lower() for word in flow_words):
            score += 0.2
        
        return min(1.0, score)


class PromptFormattingStructure:
    """Prompt Formatting and Structure: Optimizing communication patterns using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("prompt_formatting_structure")
        self.client = LangChainClient(
            model=model,
            temperature=0.4,
            max_tokens=400,
            session_name="prompt_formatting_structure"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        self.analyzer = FormatAnalyzer()
    
    def format_comparison_analysis(self) -> Dict[str, Any]:
        """
        Demonstrate intermediate format comparison across different prompt structures.
        Shows systematic format impact assessment.
        """
        self.logger.info("Running format comparison analysis")
        
        # Topic for consistent comparison
        topic = "machine learning algorithms"
        
        # Define different format approaches
        format_prompts = {
            PromptFormat.QA_FORMAT: ChatPromptTemplate.from_template(
                """Q: What are machine learning algorithms and how do they work?
A: """
            ),
            
            PromptFormat.DIALOGUE_FORMAT: ChatPromptTemplate.from_template(
                """Student: I'm confused about machine learning algorithms. Can you help me understand them?
Teacher: Of course! Let me explain machine learning algorithms in a way that makes sense.
Student: That would be great. How do they actually work?
Teacher: """
            ),
            
            PromptFormat.INSTRUCTION_FORMAT: ChatPromptTemplate.from_template(
                """Provide a clear, educational explanation of machine learning algorithms.
Include:
- What they are
- How they work
- Why they're important
- Give 1-2 examples

Explanation:"""
            ),
            
            PromptFormat.COMPLETION_FORMAT: ChatPromptTemplate.from_template(
                """Machine learning algorithms are computational methods that """
            ),
            
            PromptFormat.STRUCTURED_FORMAT: ChatPromptTemplate.from_template(
                """# Machine Learning Algorithms: Complete Guide

## Definition
[Provide definition here]

## How They Work
[Explain the process]

## Key Examples
[List 2 examples with brief descriptions]

## Why They Matter
[Explain importance]

Please complete each section:"""
            )
        }
        
        results = []
        
        for format_type, prompt in format_prompts.items():
            chain = prompt | self.llm | self.parser
            response = chain.invoke(
                {},
                config={"tags": [f"format_comparison_{format_type.value}"]}
            )
            
            # Analyze the response
            analysis = self.analyzer.analyze_response(response, format_type)
            
            results.append({
                "format_type": format_type.value,
                "response": response,
                "analysis": {
                    "length_words": analysis.response_length,
                    "clarity_score": analysis.clarity_score,
                    "engagement_score": analysis.engagement_score,
                    "structure_score": analysis.structure_score,
                    "overall_score": (analysis.clarity_score + analysis.engagement_score + analysis.structure_score) / 3
                }
            })
        
        # Find best performing format
        best_format = max(results, key=lambda x: x["analysis"]["overall_score"])
        
        return {
            "technique": "Format Comparison Analysis",
            "description": "Systematic comparison of different prompt formats to assess impact on response quality",
            "why_this_works": "Different formats trigger different response patterns in language models. Q&A formats tend to be concise, dialogue formats more engaging, instruction formats more comprehensive, and structured formats more organized. By analyzing these patterns, we can choose optimal formats for specific use cases.",
            "topic": topic,
            "examples": results,
            "best_performing_format": {
                "type": best_format["format_type"],
                "score": best_format["analysis"]["overall_score"]
            }
        }
    
    def advanced_structural_optimization(self) -> Dict[str, Any]:
        """
        Demonstrate advanced structural element optimization and template design.
        Shows sophisticated formatting strategies with impact measurement.
        """
        self.logger.info("Running advanced structural optimization")
        
        # Complex task requiring structured response
        task = "Create a comprehensive project plan for implementing a new software feature"
        
        # Test different structural approaches
        structural_variations = [
            {
                "name": "Minimal Structure",
                "prompt": ChatPromptTemplate.from_template(
                    """Create a project plan for implementing a new software feature: user authentication system.

Project Plan:"""
                )
            },
            {
                "name": "Moderate Structure",
                "prompt": ChatPromptTemplate.from_template(
                    """Create a project plan for implementing a new software feature: user authentication system.

Please organize your response with clear sections and use bullet points for lists.

Project Plan:"""
                )
            },
            {
                "name": "Advanced Structure",
                "prompt": ChatPromptTemplate.from_template(
                    """Create a comprehensive project plan for implementing a user authentication system.

# PROJECT STRUCTURE TEMPLATE:

## 🎯 Project Overview
[Brief description and objectives]

## 📋 Requirements Analysis
• Functional requirements
• Technical requirements  
• Security requirements

## 🗓️ Timeline & Phases
1. Phase 1: [Name] - [Duration]
2. Phase 2: [Name] - [Duration]
3. Phase 3: [Name] - [Duration]

## 👥 Resource Allocation
• Team members needed
• Skills required
• External dependencies

## 🔍 Risk Assessment
• High-priority risks
• Mitigation strategies

## 📊 Success Metrics
• Key performance indicators
• Acceptance criteria

Please complete each section with specific details:"""
                )
            },
            {
                "name": "Interactive Structure",
                "prompt": ChatPromptTemplate.from_template(
                    """You are a senior project manager creating a detailed plan for implementing a user authentication system.

CONTEXT: You're presenting this to both technical and non-technical stakeholders.

REQUIREMENTS:
✓ Use clear headings with emojis for visual appeal
✓ Include specific timelines and deliverables
✓ Address both technical and business concerns
✓ Use numbered lists for sequential items
✓ Use bullet points for parallel items
✓ Include risk mitigation strategies
✓ Keep sections concise but comprehensive

FORMAT EXAMPLE:
## 🚀 Phase 1: Discovery (Week 1-2)
### Deliverables:
1. Requirements document
2. Technical specification
• Security audit checklist
• API design patterns

### Risks & Mitigation:
⚠️ Risk: Unclear requirements
🛡️ Mitigation: Stakeholder interviews

Create the complete project plan following this format:"""
                )
            }
        ]
        
        results = []
        
        for variation in structural_variations:
            chain = variation["prompt"] | self.llm | self.parser
            response = chain.invoke(
                {},
                config={"tags": [f"structural_{variation['name'].lower().replace(' ', '_')}"]}
            )
            
            # Advanced structural analysis
            structural_metrics = self._analyze_structural_elements(response)
            readability_score = self._calculate_readability_score(response)
            completeness_score = self._assess_completeness(response, task)
            
            results.append({
                "structure_type": variation["name"],
                "response": response,
                "metrics": {
                    "structural_elements": structural_metrics,
                    "readability_score": readability_score,
                    "completeness_score": completeness_score,
                    "overall_effectiveness": (
                        structural_metrics["structure_density"] + 
                        readability_score + 
                        completeness_score
                    ) / 3
                },
                "word_count": len(response.split())
            })
        
        # Identify most effective structure
        best_structure = max(results, key=lambda x: x["metrics"]["overall_effectiveness"])
        
        return {
            "technique": "Advanced Structural Optimization",
            "description": "Sophisticated analysis of structural elements and their impact on communication effectiveness",
            "why_this_works": "Well-structured prompts create cognitive scaffolding that guides both the model's generation process and the reader's comprehension. By using hierarchical organization, visual elements, and clear formatting conventions, we improve information processing, reduce cognitive load, and increase task completion rates.",
            "task": task,
            "examples": results,
            "optimization_insights": {
                "most_effective_structure": best_structure["structure_type"],
                "effectiveness_score": best_structure["metrics"]["overall_effectiveness"],
                "key_factors": "Clear hierarchy, visual elements, logical flow, comprehensive coverage"
            }
        }
    
    def _analyze_structural_elements(self, text: str) -> Dict[str, Any]:
        """Analyze presence and quality of structural elements."""
        elements = {
            "headings": len([line for line in text.split('\n') if line.startswith('#') or line.startswith('##')]),
            "bullet_points": text.count('•') + text.count('*') + text.count('-'),
            "numbered_lists": len([line for line in text.split('\n') if line.strip().startswith(tuple('123456789'))]),
            "sections": text.count('\n\n'),
            "visual_elements": text.count('✓') + text.count('⚠️') + text.count('🚀') + text.count('📋'),
            "total_lines": len(text.split('\n'))
        }
        
        # Calculate structure density
        total_structural_elements = sum(elements.values()) - elements["total_lines"]
        structure_density = min(1.0, total_structural_elements / max(1, elements["total_lines"]) * 5)
        
        elements["structure_density"] = structure_density
        return elements
    
    def _calculate_readability_score(self, text: str) -> float:
        """Calculate readability score based on sentence length and complexity."""
        sentences = text.split('.')
        if not sentences:
            return 0.0
        
        # Average sentence length
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Penalize very long or very short sentences
        optimal_length = 15  # words per sentence
        length_score = 1.0 - min(1.0, abs(avg_sentence_length - optimal_length) / optimal_length)
        
        # Check for transition words (improves flow)
        transitions = ['however', 'therefore', 'additionally', 'furthermore', 'consequently']
        transition_score = min(1.0, sum(1 for t in transitions if t in text.lower()) / len(transitions))
        
        return (length_score + transition_score) / 2
    
    def _assess_completeness(self, text: str, task: str) -> float:
        """Assess how completely the response addresses the given task."""
        # For project planning task, check for key components
        required_components = [
            "timeline", "phase", "requirement", "resource", "risk", "team", 
            "deliverable", "milestone", "scope", "objective"
        ]
        
        text_lower = text.lower()
        components_present = sum(1 for comp in required_components if comp in text_lower)
        
        return components_present / len(required_components)
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all prompt formatting and structure examples."""
        self.logger.info("Starting Prompt Formatting and Structure demonstrations")
        
        results = {
            "technique_overview": "Prompt Formatting and Structure",
            "examples": []
        }
        
        # Run all example methods
        examples = [
            self.format_comparison_analysis(),
            self.advanced_structural_optimization()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager
    output_manager = OutputManager("17-prompt-formatting-structure")
    output_manager.add_header("17: PROMPT FORMATTING AND STRUCTURE")
    
    # Initialize technique
    formatting = PromptFormattingStructure()
    
    try:
        # Run examples
        results = formatting.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(formatting.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        formatting.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()