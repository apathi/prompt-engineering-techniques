#!/usr/bin/env python3
"""
Technique 11: Prompt Chaining - Advanced Multi-Step Processing

Enterprise-grade implementation demonstrating sophisticated prompt chaining patterns
including sequential chains with validation, parallel execution with synthesis,
and adaptive complexity routing with comprehensive error handling.

Features:
- Sequential chains with retry logic and validation
- Parallel chain execution with intelligent synthesis
- Adaptive complexity assessment and routing
- Performance tracking and comprehensive logging
- Production-ready error recovery mechanisms
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, OutputManager
from shared_utils.prompt_chaining_utils import (
    PromptChainManager, 
    create_adaptive_complexity_chain,
    create_content_pipeline_chain,
    validate_summary_length,
    validate_json_structure,
    validate_bullet_format
)


class PromptChaining:
    """
    Advanced prompt chaining implementation with enterprise-grade features.
    
    Demonstrates multiple chaining patterns from basic sequential processing
    to sophisticated parallel execution with adaptive routing based on complexity.
    """
    
    def __init__(self):
        self.client = LangChainClient()
        self.llm = self.client.get_llm()
        self.output_manager = OutputManager("11-prompt-chaining")
    
    def run_examples(self):
        """Execute progressive examples demonstrating different chaining approaches."""
        
        self.output_manager.add_header("TECHNIQUE 11: PROMPT CHAINING")
        self.output_manager.add_line("Advanced multi-step processing with enterprise-grade features")
        self.output_manager.add_line()
        
        results = {
            "examples": [
                self._example_1_sequential_with_validation(),
                self._example_2_parallel_with_synthesis()
            ]
        }
        
        # Display results using OutputManager
        self.output_manager.display_results(results)
        
        # Add final cost summary
        self.client.print_cost_summary()
        
        # Save final output
        self.output_manager.save_to_file()
        
        return results
    
    def _example_1_sequential_with_validation(self):
        """
        Example 1: Sequential Chain with Validation and Error Recovery
        
        Demonstrates a sophisticated multi-step analysis chain with:
        - Step-by-step document processing
        - Comprehensive validation at each step
        - Automatic retry with exponential backoff
        - Performance tracking and detailed logging
        """
        
        # Complex business document for analysis
        document = """
        Q3 Financial Performance Summary
        
        Revenue Growth: Our total revenue reached $47.2M in Q3, representing a 23% increase 
        over Q2 ($38.4M) and 45% growth year-over-year. Key drivers included:
        - Enterprise software licenses: $28.1M (+35% YoY)
        - Cloud services: $12.8M (+67% YoY)  
        - Professional services: $6.3M (+18% YoY)
        
        Market Expansion: We successfully launched in 3 new international markets (Germany, 
        Japan, Australia) with initial customer acquisition exceeding projections by 28%. 
        Total active customers now at 14,750 (+2,100 from Q2).
        
        Operational Challenges: Supply chain disruptions impacted delivery timelines for 
        15% of orders. Additionally, increased competition in the cloud services sector 
        has compressed margins by 3.2 percentage points.
        
        Strategic Initiatives: Completed acquisition of DataVision Analytics for $12.5M, 
        expanding our AI capabilities. Also invested $3.8M in R&D for next-generation 
        predictive analytics platform.
        
        Outlook: Based on current pipeline and market conditions, Q4 revenue projected 
        at $52-55M with continued focus on international expansion and product innovation.
        """
        
        # Define sequential chain with comprehensive validation
        chain_steps = [
            {
                "template": """Analyze the following business document and extract key financial metrics in a structured format:

Document: {input}

Provide a clear breakdown of:
1. Revenue figures with growth percentages
2. Customer metrics and acquisition data
3. Market expansion details
4. Key challenges identified

Financial Analysis:""",
                "validators": {
                    "contains_numbers": lambda text: any(c.isdigit() for c in text),
                    "sufficient_length": lambda text: len(text.split()) >= 50,
                    "contains_revenue": lambda text: "revenue" in text.lower() or "million" in text.lower()
                }
            },
            {
                "template": """Based on the financial analysis provided, identify the top 3 strategic opportunities and 3 critical risks:

Analysis: {input}

Format your response with clear headings for:
- Strategic Opportunities (with rationale)
- Critical Risks (with impact assessment)
- Priority Actions

Strategic Assessment:""",
                "validators": {
                    "has_opportunities": lambda text: "opportunities" in text.lower() and "risks" in text.lower(),
                    "structured_format": lambda text: len([line for line in text.split('\n') if line.strip().startswith('-') or line.strip().startswith('1.')]) >= 3
                }
            },
            {
                "template": """Create executive recommendations based on the strategic assessment:

Assessment: {input}

Provide 5 specific, actionable recommendations with:
- Priority level (High/Medium/Low)
- Resource requirements
- Expected timeline
- Success metrics

Executive Recommendations:""",
                "validators": {
                    "has_recommendations": lambda text: "recommendation" in text.lower() or "recommend" in text.lower(),
                    "has_priorities": lambda text: "high" in text.lower() or "medium" in text.lower() or "low" in text.lower()
                }
            }
        ]
        
        # Execute sequential chain with comprehensive tracking
        manager = PromptChainManager(self.llm, enable_logging=True, max_retries=2)
        result = manager.execute_sequential_chain(chain_steps, document)
        
        # Process results for display
        if result.get("success"):
            # Extract step outputs for analysis
            step_outputs = []
            for step_result in result["results"]:
                step_outputs.append({
                    "step": f"Step {step_result['step']}",
                    "execution_time": f"{step_result['execution_time']}s",
                    "validation_status": "✅ Passed" if step_result.get('validation_results', []) else "⚠️ No validation",
                    "output_preview": step_result["output"],
                    "retry_count": step_result.get('retry_count', 0)
                })
            
            return {
                "technique": "Sequential Chain with Validation & Error Recovery",
                "examples": [
                    {
                        "approach": "Multi-step Business Document Analysis",
                        "problem": "Complex business document requiring multi-stage analysis with validation",
                        "description": "3-step chain: Financial Analysis → Strategic Assessment → Executive Recommendations",
                        "input_length": f"{len(document.split())} words",
                        "total_execution_time": f"{result['performance_metrics']['total_execution_time']}s",
                        "steps_completed": len(result["results"]),
                        "validation_checks": sum(len(step.get('validation_results', [])) for step in result["results"]),
                        "response": result["final_output"],
                        "why_this_works": "Sequential validation ensures quality at each step, while retry logic handles transient failures. Performance tracking enables optimization, and structured validation prevents chain failures from propagating.",
                        "step_breakdown": step_outputs
                    }
                ]
            }
        else:
            return {
                "technique": "Sequential Chain with Validation & Error Recovery",
                "examples": [
                    {
                        "approach": "Chain Execution Failed",
                        "problem": "Sequential chain execution encountered failure",
                        "error": result.get("error", "Unknown error"),
                        "partial_results": f"{len(result.get('partial_results', []))} steps completed",
                        "response": f"Chain failed: {result.get('error', 'Unknown error')}",
                        "why_this_works": "Error handling demonstrates robust failure recovery - even failed chains provide useful diagnostic information."
                    }
                ]
            }
    
    def _example_2_parallel_with_synthesis(self):
        """
        Example 2: Parallel Execution with Intelligent Synthesis
        
        Demonstrates advanced parallel processing with:
        - Multiple analysis perspectives executed simultaneously
        - Intelligent result synthesis and aggregation
        - Performance optimization with ThreadPoolExecutor
        - Comprehensive error handling and fallback strategies
        """
        
        # Technical product specification for multi-angle analysis
        product_spec = """
        CloudSync Pro Enterprise - Next-Generation Data Integration Platform
        
        Technical Architecture:
        - Microservices-based design with Kubernetes orchestration
        - Event-driven architecture using Apache Kafka for real-time processing
        - Multi-cloud deployment support (AWS, Azure, GCP)
        - RESTful APIs with GraphQL query layer
        - Built-in security with OAuth 2.0 and end-to-end encryption
        
        Core Features:
        - Real-time data synchronization across 150+ data sources
        - AI-powered data quality monitoring and automated cleaning
        - Visual workflow designer with drag-and-drop interface
        - Advanced analytics with machine learning model integration
        - Compliance tools for GDPR, HIPAA, SOX requirements
        
        Performance Specifications:
        - Processing capacity: 10TB+ per hour
        - Latency: <50ms for real-time operations
        - Uptime SLA: 99.99% with automated failover
        - Concurrent users: 10,000+ with horizontal scaling
        - Data retention: Configurable from 30 days to 10 years
        
        Market Positioning:
        - Target: Enterprise customers with complex data ecosystems
        - Pricing: Tier-based starting at $50K annually
        - Competition: Informatica, Talend, Microsoft Power Platform
        - Differentiator: AI-native design with self-healing capabilities
        
        Implementation Requirements:
        - Deployment time: 4-6 weeks with professional services
        - Training: 40-hour certification program for administrators
        - Integration: API-first design for seamless third-party connections
        - Support: 24/7 enterprise support with dedicated success manager
        """
        
        # Define parallel analysis perspectives
        parallel_prompts = {
            "technical_analysis": """Analyze the technical architecture and specifications of this product:

{document}

Focus on:
- Architecture strengths and potential weaknesses
- Scalability and performance capabilities
- Technology stack evaluation
- Integration complexity assessment

Technical Analysis:""",
            
            "market_analysis": """Evaluate the market positioning and competitive landscape for this product:

{document}

Analyze:
- Target market fit and opportunity size
- Competitive advantages and disadvantages
- Pricing strategy effectiveness
- Market entry barriers and challenges

Market Analysis:""",
            
            "risk_analysis": """Identify potential risks and mitigation strategies for this product:

{document}

Evaluate:
- Technical implementation risks
- Market and competitive risks
- Operational and support risks
- Compliance and security considerations

Risk Analysis:""",
            
            "implementation_analysis": """Assess the implementation and adoption challenges for this product:

{document}

Consider:
- Deployment complexity and timeline
- User training and adoption requirements
- Change management considerations
- Success measurement criteria

Implementation Analysis:"""
        }
        
        # Synthesis template for combining all perspectives
        synthesis_template = """Based on the comprehensive analysis from multiple perspectives, create an executive summary with strategic recommendations:

Analysis Results:
{analysis_results}

Original Product:
{original_document}

Provide a synthesized assessment covering:
1. Overall Product Viability (1-10 scale with rationale)
2. Top 3 Strategic Strengths
3. Top 3 Critical Concerns
4. Implementation Priority (High/Medium/Low) with justification
5. Next Steps and Key Decision Points

Executive Summary:"""
        
        # Execute parallel analysis with synthesis
        manager = PromptChainManager(self.llm, enable_logging=True)
        result = manager.execute_parallel_chains(
            parallel_prompts, 
            product_spec, 
            synthesis_template
        )
        
        # Process results for display
        if result.get("success"):
            # Extract individual analysis results
            analysis_results = []
            for analysis_detail in result["execution_details"]:
                analysis_results.append({
                    "analysis_type": analysis_detail["name"].replace('_', ' ').title(),
                    "execution_time": f"{analysis_detail['execution_time']}s",
                    "success": "✅ Success" if analysis_detail["success"] else "❌ Failed",
                    "output_length": analysis_detail.get("output_length", 0),
                    "preview": analysis_detail["result"]
                })
            
            return {
                "technique": "Parallel Execution with Intelligent Synthesis",
                "examples": [
                    {
                        "approach": "Multi-Perspective Product Analysis",
                        "problem": "Complex product specification requiring multi-angle analysis",
                        "description": "4 parallel analyses (Technical, Market, Risk, Implementation) with intelligent synthesis",
                        "parallel_tasks": len(parallel_prompts),
                        "successful_analyses": result["successful_count"],
                        "failed_analyses": result["failed_count"],
                        "total_execution_time": f"{result['performance_metrics']['total_execution_time']}s",
                        "fastest_analysis": f"{result['performance_metrics']['fastest_execution']}s",
                        "slowest_analysis": f"{result['performance_metrics']['slowest_execution']}s",
                        "response": result.get("synthesis", "Synthesis not available"),
                        "why_this_works": "Parallel execution dramatically reduces total processing time while multiple perspectives provide comprehensive coverage. Intelligent synthesis combines insights that no single analysis could achieve, and ThreadPoolExecutor optimization ensures optimal resource utilization.",
                        "analysis_breakdown": analysis_results
                    }
                ]
            }
        else:
            return {
                "technique": "Parallel Execution with Intelligent Synthesis",
                "examples": [
                    {
                        "approach": "Parallel Execution Failed",
                        "problem": "Parallel chain execution encountered failure",
                        "error": "Parallel execution encountered errors",
                        "response": "Parallel execution failed - see error handling capabilities",
                        "why_this_works": "Even failed parallel execution demonstrates robust error handling and provides partial results where possible."
                    }
                ]
            }


def main():
    """Main execution function following established pattern."""
    
    # Clear display
    print("\n" + "="*60)
    print("TECHNIQUE 11: PROMPT CHAINING")
    print("="*60)
    
    # Initialize and run
    chaining = PromptChaining()
    results = chaining.run_examples()
    
    return results


if __name__ == "__main__":
    main()