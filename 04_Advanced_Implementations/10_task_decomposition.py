"""
10: Task Decomposition (LangChain Implementation)

This module demonstrates task decomposition techniques where complex tasks
are broken down into manageable subtasks with dependency tracking and
sequential execution, using simplified workflow management.

Key concepts:
- Systematic task breakdown strategies
- Dependency identification and management
- Sequential task execution workflows
- Result integration and synthesis
- Progress tracking and validation

"""

import os
import sys
from typing import List, Dict, Any

# Add shared_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared_utils import LangChainClient, setup_logger, OutputManager
from shared_utils.task_decomposer import TaskDecomposer, create_simple_decomposition, analyze_task_complexity
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class TaskDecomposition:
    """Task Decomposition: Breaking complex tasks into manageable workflows using LangChain."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize with LangChain client and components."""
        self.logger = setup_logger("task_decomposition")
        self.client = LangChainClient(
            model=model,
            temperature=0.3,  # Balanced creativity with systematic thinking
            max_tokens=400,
            session_name="task_decomposition"
        )
        self.llm = self.client.get_llm()
        self.parser = StrOutputParser()
    
    def systematic_project_breakdown(self) -> Dict[str, Any]:
        """
        Demonstrate systematic project breakdown with dependency tracking.
        Shows intermediate-level task decomposition for project management.
        
        Why this works:
        Complex projects become manageable when broken into sequential,
        well-defined subtasks. This approach reduces cognitive load and
        enables systematic progress tracking and validation.
        """
        self.logger.info("Running systematic project breakdown")
        
        # Complex project requiring systematic breakdown
        project_description = """
        Launch a new mobile app for local restaurant discovery:
        
        Requirements:
        - iOS and Android apps with location-based restaurant search
        - User reviews and ratings system
        - Restaurant owner dashboard for menu/info management
        - Payment integration for in-app orders
        - 6-month timeline with limited budget
        - Team: 2 developers, 1 designer, 1 PM
        - Must comply with app store guidelines and local regulations
        
        Create a comprehensive project plan with clear deliverables and timeline.
        """
        
        # Task decomposition prompt
        decomposition_prompt = PromptTemplate.from_template(
            """Analyze this complex project and break it down into manageable tasks.

Project: {project}

Create a systematic breakdown following this structure:

PHASE 1 - PROJECT ANALYSIS:
- Identify core components and requirements
- Assess complexity and resource needs
- Determine critical path dependencies

PHASE 2 - TASK DECOMPOSITION:
- Break down into 6-8 major tasks/phases
- Define clear deliverables for each task
- Estimate timeline and resource allocation
- Identify dependencies between tasks

PHASE 3 - EXECUTION SEQUENCE:
- Determine optimal task ordering
- Identify which tasks can be parallel
- Plan milestone checkpoints
- Define success criteria for each phase

Structured Breakdown:"""
        )
        
        # Generate decomposition
        decomposition_chain = decomposition_prompt | self.llm | self.parser
        breakdown_analysis = decomposition_chain.invoke(
            {"project": project_description},
            config={"tags": ["task_decomp_project_analysis"]}
        )
        
        # Create task decomposer for dependency tracking
        decomposer = create_simple_decomposition(
            "Mobile App Launch",
            [
                "Requirements analysis and technical specification",
                "UI/UX design and user flow creation", 
                "Backend API development and database setup",
                "Mobile app development (iOS/Android)",
                "Payment integration and testing",
                "Restaurant dashboard development",
                "Testing, debugging, and performance optimization",
                "App store submission and launch preparation"
            ]
        )
        
        # Get execution order and summary
        execution_order = decomposer.get_execution_order()
        task_summary = decomposer.get_task_summary()
        
        # Validation and refinement prompt
        validation_prompt = PromptTemplate.from_template(
            """Review this project breakdown for completeness and feasibility:

Original Project: {project}

Proposed Breakdown: {breakdown}

Task Execution Order: {order}

Validation Analysis:
1. Are all critical requirements covered?
2. Are task dependencies logical and realistic?
3. Is the timeline feasible with given resources?
4. Are there missing tasks or overlooked requirements?
5. What are the highest-risk elements?

Provide improvement recommendations:"""
        )
        
        validation_chain = validation_prompt | self.llm | self.parser
        validation_analysis = validation_chain.invoke(
            {
                "project": project_description,
                "breakdown": breakdown_analysis,
                "order": [f"{i+1}. {decomposer.tasks[task_id].description}" for i, task_id in enumerate(execution_order)]
            },
            config={"tags": ["task_decomp_validation"]}
        )
        
        results = [
            {
                "stage": "Initial Breakdown Analysis",
                "description": "Systematic decomposition with dependency identification",
                "response": breakdown_analysis
            },
            {
                "stage": "Execution Planning",
                "description": f"Sequential task ordering with {len(execution_order)} identified tasks",
                "response": f"Task Execution Order:\n" + "\n".join([f"{i+1}. {decomposer.tasks[task_id].title}: {decomposer.tasks[task_id].description}" for i, task_id in enumerate(execution_order)])
            },
            {
                "stage": "Validation and Refinement", 
                "description": "Critical analysis of proposed breakdown for feasibility",
                "response": validation_analysis
            }
        ]
        
        return {
            "technique": "Systematic Project Breakdown",
            "examples": results,
            "project_description": project_description,
            "execution_metrics": {
                "total_tasks": len(execution_order),
                "estimated_phases": 3,
                "dependency_complexity": "Sequential with some parallel opportunities"
            },
            "why_this_works": """Systematic project breakdown works because:
1. Large projects become manageable through structured decomposition
2. Dependency identification prevents bottlenecks and resource conflicts
3. Clear deliverables enable progress tracking and quality control
4. Sequential ordering optimizes resource utilization and timeline
5. Validation phases catch overlooked requirements and risks early"""
        }
    
    def complex_workflow_orchestration(self) -> Dict[str, Any]:
        """
        Demonstrate complex workflow orchestration with parallel execution.
        Shows advanced workflow management with multiple coordination points.
        
        Why this works:
        Complex workflows require coordination between parallel work streams.
        Proper orchestration maximizes efficiency while maintaining quality
        and ensuring all components integrate successfully.
        """
        self.logger.info("Running complex workflow orchestration")
        
        # Complex multi-stream workflow scenario
        workflow_scenario = """
        Organize a hybrid corporate conference for 500 attendees:
        
        Event Requirements:
        - 2-day conference with keynotes, breakout sessions, networking
        - Hybrid format: 300 in-person, 200 virtual attendees
        - 20 speakers (mix of internal executives and external experts)
        - Exhibition area with 15 sponsor booths
        - Catering for dietary restrictions and cultural preferences
        - Live streaming and recording capabilities
        - Post-event content distribution and follow-up
        
        Constraints:
        - 3-month planning timeline
        - $200K budget allocation
        - Venue already booked
        - Must comply with accessibility and safety regulations
        - International speakers requiring visa/travel coordination
        
        Create a comprehensive workflow that maximizes parallel execution.
        """
        
        # Workflow orchestration analysis
        orchestration_prompt = PromptTemplate.from_template(
            """Design a complex workflow for this multi-faceted event:

Event Challenge: {scenario}

Create an advanced workflow orchestration plan:

WORKFLOW DESIGN:
1. Identify all major work streams that can run in parallel
2. Map critical integration points where streams must synchronize
3. Design coordination mechanisms between parallel teams
4. Plan resource sharing and conflict resolution
5. Define quality gates and validation checkpoints

PARALLEL EXECUTION STRATEGY:
- Content & Speaker Track: Program design, speaker coordination, content preparation
- Technology Track: A/V setup, streaming platform, registration system
- Logistics Track: Venue setup, catering, accommodation, transportation  
- Marketing Track: Promotion, registration, sponsor coordination
- Compliance Track: Permits, accessibility, safety protocols

INTEGRATION CHOREOGRAPHY:
Map how these parallel streams coordinate and integrate at key milestones.

Orchestration Plan:"""
        )
        
        orchestration_chain = orchestration_prompt | self.llm | self.parser
        workflow_design = orchestration_chain.invoke(
            {"scenario": workflow_scenario},
            config={"tags": ["workflow_orchestration"]}
        )
        
        # Risk and contingency analysis
        contingency_prompt = PromptTemplate.from_template(
            """Analyze this workflow for risks and create contingency plans:

Workflow: {workflow}

RISK ANALYSIS:
1. Identify critical path bottlenecks
2. Assess coordination failure points
3. Evaluate resource constraint risks  
4. Consider external dependency vulnerabilities
5. Plan for scope creep and timeline pressure

CONTINGENCY PLANNING:
- What are the "must-have" vs "nice-to-have" elements?
- How can parallel streams adapt if one falls behind?
- What are fallback options for critical dependencies?
- How to maintain quality under timeline pressure?

Risk Mitigation Strategy:"""
        )
        
        contingency_chain = contingency_prompt | self.llm | self.parser
        risk_analysis = contingency_chain.invoke(
            {"workflow": workflow_design},
            config={"tags": ["workflow_risk_analysis"]}
        )
        
        # Implementation complexity assessment
        complexity_analysis = analyze_task_complexity(workflow_scenario)
        
        results = [
            {
                "component": "Parallel Workflow Design",
                "description": "Multi-stream orchestration with coordination points",
                "response": workflow_design
            },
            {
                "component": "Risk and Contingency Planning",
                "description": "Critical path analysis with fallback strategies",
                "response": risk_analysis
            },
            {
                "component": "Complexity Assessment",
                "description": f"Automated analysis: {complexity_analysis['complexity']} complexity, {complexity_analysis['decomposition_type']} workflow",
                "response": f"Analysis Results:\n- Complexity Level: {complexity_analysis['complexity']}\n- Workflow Type: {complexity_analysis['decomposition_type']}\n- Estimated Subtasks: {complexity_analysis['estimated_subtasks']}\n- Recommendation: {complexity_analysis['suggestion']}"
            }
        ]
        
        return {
            "technique": "Complex Workflow Orchestration",
            "examples": results,
            "workflow_scenario": workflow_scenario,
            "orchestration_metrics": {
                "parallel_streams": 5,
                "integration_points": "Multiple synchronization milestones",
                "complexity_level": complexity_analysis['complexity']
            },
            "why_this_works": """Complex workflow orchestration works because:
1. Parallel execution maximizes resource utilization and reduces timeline
2. Clear integration points prevent coordination failures
3. Risk analysis identifies critical dependencies before they become problems
4. Contingency planning provides adaptability under changing conditions
5. Structured orchestration scales coordination across multiple teams effectively"""
        }
    
    def run_all_examples(self) -> Dict[str, Any]:
        """Run all task decomposition examples."""
        self.logger.info("Starting Task Decomposition demonstrations")
        
        results = {
            "technique_overview": "Task Decomposition",
            "examples": []
        }
        
        # Run example methods
        examples = [
            self.systematic_project_breakdown(),
            self.complex_workflow_orchestration()
        ]
        
        results["examples"] = examples
        
        # Print cost summary
        self.client.print_cost_summary()
        
        return results


def main():
    """Main execution function."""
    # Initialize output manager with folder name format
    output_manager = OutputManager("10-task-decomposition")
    output_manager.add_header("10: TASK DECOMPOSITION - LANGCHAIN")
    
    # Initialize technique
    task_decomp = TaskDecomposition()
    
    try:
        # Run examples
        results = task_decomp.run_all_examples()
        
        # Display results using OutputManager
        output_manager.display_results(results)
        
        # Add cost summary
        output_manager.add_cost_summary(task_decomp.client)
        
        # Save to file
        output_manager.save_to_file()
        
    except KeyboardInterrupt:
        output_manager.add_line("\n\nExecution interrupted by user")
        output_manager.save_to_file()
    except Exception as e:
        output_manager.add_line(f"Error: {e}")
        task_decomp.logger.error(f"Execution failed: {e}")
        output_manager.save_to_file()


if __name__ == "__main__":
    main()