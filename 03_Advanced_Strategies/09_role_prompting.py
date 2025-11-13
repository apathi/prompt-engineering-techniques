"""
09: Role Prompting (LangChain Implementation)

This module demonstrates role prompting techniques where AI adopts specific
professional personas, expertise domains, and contextual perspectives to
provide specialized responses without complex dynamic context switching.

Key concepts:
- Professional role assignment and persona adoption
- Domain expertise simulation
- Context-aware role behavior
- Multi-role consultation and comparison
- Role-specific communication styles

"""

import os
import sys
from typing import List, Dict, Any

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class RolePrompting:
    """Role Prompting: Professional persona adoption with LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("role_prompting")
        self.client = LangChainClient(
            model=model,
            temperature=0.4,  # Balanced creativity with professional consistency
            max_tokens=400,
            session_name="role_prompting"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
        
        # Predefined professional role profiles
        self.role_profiles = {
            "financial_advisor": {
                "persona": "You are a certified financial advisor with 15+ years of experience",
                "expertise": "Investment strategies, risk management, retirement planning, tax optimization",
                "style": "Professional, data-driven, cautious, focuses on long-term stability",
                "context": "Always consider client's risk tolerance and financial goals"
            },
            "tech_architect": {
                "persona": "You are a senior software architect with expertise in large-scale systems",
                "expertise": "System design, scalability, security, cloud architecture, performance optimization", 
                "style": "Technical, thorough, considers trade-offs, focuses on maintainability",
                "context": "Always evaluate scalability, security, and maintainability implications"
            },
            "medical_researcher": {
                "persona": "You are a medical researcher with PhD in biomedical sciences",
                "expertise": "Clinical research, evidence-based medicine, statistical analysis, peer review",
                "style": "Scientific, evidence-based, cautious about claims, cites methodology",
                "context": "Always emphasize evidence quality and statistical significance"
            },
            "marketing_strategist": {
                "persona": "You are a marketing strategist with expertise in digital campaigns",
                "expertise": "Brand positioning, consumer psychology, digital marketing, campaign ROI",
                "style": "Creative, data-driven, consumer-focused, results-oriented",
                "context": "Always consider target audience and measurable outcomes"
            }
        }
    
    def professional_domain_expertise(self) -> Dict[str, Any]:
        """
        Demonstrate professional domain expertise through role adoption.
        Shows intermediate-level specialized knowledge application.
        
        Why this works:
        Role prompting activates domain-specific knowledge patterns in the model,
        leading to more accurate, contextual, and professionally appropriate
        responses within specific fields of expertise.
        """
        self.logger.info("Running professional domain expertise demonstration")
        
        # Business scenario requiring professional expertise
        scenario = """
        A small e-commerce business (annual revenue $500K) is experiencing:
        - 40% cart abandonment rate
        - 15% monthly customer churn  
        - Rising customer acquisition costs ($45 per customer)
        - Seasonal revenue fluctuations (60% higher in Q4)
        
        They have $50K budget and 6-month timeline to address these issues.
        What strategy would you recommend?
        """
        
        # Test different professional perspectives
        roles_to_test = ["financial_advisor", "tech_architect", "marketing_strategist"]
        
        results = []
        
        for role_key in roles_to_test:
            role = self.role_profiles[role_key]
            
            # Create role-specific prompt
            role_prompt = PromptTemplate.from_template(
                """{persona}. {expertise}.

Your communication style: {style}
Context to consider: {context}

Analyze this business scenario from your professional perspective:

Scenario: {scenario}

Provide your expert recommendation:"""
            )
            
            # Generate role-specific response
            role_chain = role_prompt | self.llm | self.parser
            response = role_chain.invoke(
                {
                    "persona": role["persona"],
                    "expertise": f"Your areas of expertise include: {role['expertise']}",
                    "style": role["style"], 
                    "context": role["context"],
                    "scenario": scenario
                },
                config={"tags": [f"role_{role_key}"]}
            )
            
            results.append({
                "role": role_key.replace("_", " ").title(),
                "expertise_areas": role["expertise"],
                "communication_style": role["style"],
                "response": response
            })
        
        return {
            "technique": "Professional Domain Expertise",
            "examples": results,
            "scenario_description": scenario,
            "why_this_works": """Professional role adoption works because:
1. Activates domain-specific knowledge patterns in the model
2. Provides contextual framework for specialized reasoning
3. Ensures responses match professional communication styles
4. Leverages expertise hierarchies and decision-making patterns
5. Creates consistent, reliable expert-level outputs"""
        }
    
    def multi_role_consultation_analysis(self) -> Dict[str, Any]:
        """
        Demonstrate multi-role consultation for complex decisions.
        Shows advanced collaborative analysis with role integration.
        
        Why this works:
        Complex problems benefit from multiple professional perspectives.
        Multi-role consultation provides comprehensive analysis covering
        different aspects that single-role analysis might miss.
        """
        self.logger.info("Running multi-role consultation analysis")
        
        # Complex decision requiring multiple expertise areas
        decision_scenario = """
        A healthcare startup wants to launch an AI-powered diagnostic tool:
        
        Product Details:
        - AI system for early detection of skin cancer from photos
        - Target market: Dermatology clinics and primary care
        - Development cost: $2M, 18-month timeline
        - Regulatory approval required (FDA Class II medical device)
        - Competition: 3 established players, 2 emerging startups
        
        Key Concerns:
        - Clinical validation requirements
        - Data privacy and security compliance
        - Market penetration strategy
        - Funding requirements ($5M Series A)
        - Risk management and liability
        
        Should they proceed with development?
        """
        
        # Multi-role consultation process
        consultation_roles = [
            {
                "role": "medical_researcher",
                "focus": "Clinical validation, regulatory requirements, medical efficacy"
            },
            {
                "role": "tech_architect", 
                "focus": "Technical feasibility, security, scalability, development risks"
            },
            {
                "role": "financial_advisor",
                "focus": "Financial viability, funding strategy, ROI analysis, risk assessment"
            }
        ]
        
        # Synthesis prompt for integration
        synthesis_prompt = PromptTemplate.from_template(
            """You are a senior business consultant synthesizing expert opinions for executive decision-making.

Original Decision: {scenario}

Expert Consultations:
{expert_opinions}

Provide an integrated analysis that:
1. Synthesizes key insights from all experts
2. Identifies areas of consensus and disagreement
3. Weighs the different perspectives appropriately
4. Makes a clear go/no-go recommendation
5. Outlines critical success factors and risk mitigation

Executive Summary:"""
        )
        
        results = []
        expert_opinions = []
        
        # Get each expert's opinion
        for consultation in consultation_roles:
            role_key = consultation["role"]
            role = self.role_profiles[role_key]
            
            expert_prompt = PromptTemplate.from_template(
                """{persona}. Focus your analysis on: {focus_areas}

Decision Scenario: {scenario}

Provide your expert assessment covering:
- Key opportunities and risks from your perspective  
- Critical success factors in your domain
- Specific recommendations for your area of expertise
- Overall recommendation (proceed/pause/abandon) with rationale

Expert Analysis:"""
            )
            
            expert_chain = expert_prompt | self.llm | self.parser
            expert_response = expert_chain.invoke(
                {
                    "persona": role["persona"],
                    "focus_areas": consultation["focus"],
                    "scenario": decision_scenario
                },
                config={"tags": [f"consultation_{role_key}"]}
            )
            
            expert_opinions.append(f"{role_key.replace('_', ' ').title()}: {expert_response}")
            
            results.append({
                "expert_role": role_key.replace("_", " ").title(),
                "focus_areas": consultation["focus"],
                "recommendation": expert_response
            })
        
        # Synthesize all expert opinions
        synthesis_chain = synthesis_prompt | self.llm | self.parser
        integrated_analysis = synthesis_chain.invoke(
            {
                "scenario": decision_scenario,
                "expert_opinions": "\n\n".join(expert_opinions)
            },
            config={"tags": ["multi_role_synthesis"]}
        )
        
        # Add synthesis to results
        results.append({
            "expert_role": "Executive Integration",
            "focus_areas": "Synthesis of all expert perspectives",
            "recommendation": integrated_analysis
        })
        
        return {
            "technique": "Multi-Role Consultation Analysis", 
            "examples": results,
            "decision_scenario": decision_scenario,
            "why_this_works": """Multi-role consultation works because:
1. Different professional perspectives reveal distinct aspects of complex problems
2. Expert domain knowledge provides specialized risk and opportunity assessment
3. Integration of multiple viewpoints creates more robust decision-making
4. Role-specific communication styles ensure appropriate depth in each area
5. Synthesis process balances competing priorities and constraints effectively"""
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all role prompting examples."""
        self.logger.info("Starting Role Prompting demonstrations")
        
        results = {
            "technique_overview": "Role Prompting",
            "examples": []
        }
        
        # Run example methods
        examples = [
            self.professional_domain_expertise(),
            self.multi_role_consultation_analysis()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager with folder name format
    output_manager = OutputManager("09-role-prompting")
    output_manager.add_header("09: ROLE PROMPTING - LANGCHAIN")
    
    # Initialize technique
    role_prompting = RolePrompting()
    
    try:
        # Run examples
        results = role_prompting.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(role_prompting.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        role_prompting.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()