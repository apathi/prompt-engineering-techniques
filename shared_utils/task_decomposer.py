"""
Task decomposition utilities for prompt engineering.

Simple utilities for breaking down complex tasks into manageable subtasks,
tracking dependencies, and managing task execution workflows.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Status of a task in the decomposition workflow."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class Task:
    """Represents a single task in a decomposition workflow."""
    id: str
    title: str
    description: str
    dependencies: List[str] = None  # List of task IDs this depends on
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class TaskDecomposer:
    """Simple task decomposition and management utility."""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.execution_order: List[str] = []
    
    def add_task(self, task_id: str, title: str, description: str, 
                 dependencies: Optional[List[str]] = None) -> Task:
        """
        Add a task to the decomposition.
        
        Args:
            task_id: Unique identifier for the task
            title: Short title for the task
            description: Detailed description of what needs to be done
            dependencies: List of task IDs this task depends on
            
        Returns:
            Created Task object
        """
        task = Task(
            id=task_id,
            title=title,
            description=description,
            dependencies=dependencies or []
        )
        self.tasks[task_id] = task
        return task
    
    def get_ready_tasks(self) -> List[Task]:
        """
        Get tasks that are ready to be executed (no pending dependencies).
        
        Returns:
            List of tasks ready for execution
        """
        ready_tasks = []
        
        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
                
            # Check if all dependencies are completed
            dependencies_met = all(
                self.tasks.get(dep_id, Task("", "", "")).status == TaskStatus.COMPLETED
                for dep_id in task.dependencies
            )
            
            if dependencies_met:
                ready_tasks.append(task)
        
        return ready_tasks
    
    def mark_task_completed(self, task_id: str, result: Optional[str] = None):
        """Mark a task as completed with optional result."""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETED
            self.tasks[task_id].result = result
    
    def mark_task_failed(self, task_id: str, error: str):
        """Mark a task as failed with error message."""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.FAILED
            self.tasks[task_id].error = error
    
    def mark_task_in_progress(self, task_id: str):
        """Mark a task as in progress."""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.IN_PROGRESS
    
    def get_execution_order(self) -> List[str]:
        """
        Calculate the optimal execution order based on dependencies.
        Uses topological sorting.
        
        Returns:
            List of task IDs in execution order
        """
        # Simple topological sort implementation
        visited = set()
        temp_visited = set()
        order = []
        
        def visit(task_id: str):
            if task_id in temp_visited:
                raise ValueError(f"Circular dependency detected involving task {task_id}")
            if task_id in visited:
                return
            
            temp_visited.add(task_id)
            
            # Visit dependencies first
            task = self.tasks.get(task_id)
            if task:
                for dep_id in task.dependencies:
                    if dep_id in self.tasks:
                        visit(dep_id)
            
            temp_visited.remove(task_id)
            visited.add(task_id)
            order.append(task_id)
        
        # Visit all tasks
        for task_id in self.tasks.keys():
            visit(task_id)
        
        self.execution_order = order
        return order
    
    def get_task_summary(self) -> Dict[str, Any]:
        """
        Get summary of all tasks and their statuses.
        
        Returns:
            Dictionary with task summary information
        """
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = 0
        
        for task in self.tasks.values():
            status_counts[task.status.value] += 1
        
        completed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
        failed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
        
        return {
            "total_tasks": len(self.tasks),
            "status_counts": status_counts,
            "completion_rate": len(completed_tasks) / len(self.tasks) if self.tasks else 0.0,
            "completed_tasks": [{"id": t.id, "title": t.title} for t in completed_tasks],
            "failed_tasks": [{"id": t.id, "title": t.title, "error": t.error} for t in failed_tasks],
            "ready_tasks": [{"id": t.id, "title": t.title} for t in self.get_ready_tasks()]
        }
    
    def validate_dependencies(self) -> Dict[str, Any]:
        """
        Validate that all task dependencies are valid.
        
        Returns:
            Validation result with any issues found
        """
        issues = []
        
        for task_id, task in self.tasks.items():
            for dep_id in task.dependencies:
                if dep_id not in self.tasks:
                    issues.append(f"Task '{task_id}' depends on non-existent task '{dep_id}'")
        
        # Check for circular dependencies
        try:
            self.get_execution_order()
        except ValueError as e:
            issues.append(str(e))
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues
        }


def create_simple_decomposition(main_task: str, subtask_descriptions: List[str]) -> TaskDecomposer:
    """
    Create a simple sequential task decomposition.
    
    Args:
        main_task: Description of the main task
        subtask_descriptions: List of subtask descriptions
        
    Returns:
        TaskDecomposer with sequential tasks
    """
    decomposer = TaskDecomposer()
    
    # Add tasks sequentially with each depending on the previous
    for i, description in enumerate(subtask_descriptions):
        task_id = f"task_{i+1}"
        title = f"Step {i+1}"
        dependencies = [f"task_{i}"] if i > 0 else []
        
        decomposer.add_task(task_id, title, description, dependencies)
    
    return decomposer


def create_parallel_decomposition(main_task: str, parallel_tasks: List[str], 
                                 final_task: Optional[str] = None) -> TaskDecomposer:
    """
    Create a parallel task decomposition with optional final consolidation task.
    
    Args:
        main_task: Description of the main task
        parallel_tasks: List of tasks that can be done in parallel
        final_task: Optional final task that depends on all parallel tasks
        
    Returns:
        TaskDecomposer with parallel task structure
    """
    decomposer = TaskDecomposer()
    
    # Add parallel tasks
    parallel_ids = []
    for i, description in enumerate(parallel_tasks):
        task_id = f"parallel_task_{i+1}"
        title = f"Parallel Step {i+1}"
        decomposer.add_task(task_id, title, description)
        parallel_ids.append(task_id)
    
    # Add final consolidation task if specified
    if final_task:
        decomposer.add_task("final_task", "Final Integration", final_task, parallel_ids)
    
    return decomposer


def analyze_task_complexity(task_description: str) -> Dict[str, Any]:
    """
    Analyze a task description to suggest decomposition approach.
    
    Args:
        task_description: Description of the task to analyze
        
    Returns:
        Analysis suggesting decomposition strategy
    """
    description_lower = task_description.lower()
    
    # Simple heuristics for complexity analysis
    complexity_indicators = {
        "high": ["analyze", "research", "compare", "evaluate", "design", "plan", "strategy"],
        "medium": ["create", "write", "implement", "develop", "build"],
        "low": ["list", "summarize", "explain", "describe", "define"]
    }
    
    sequential_indicators = ["first", "then", "next", "after", "finally", "step"]
    parallel_indicators = ["simultaneously", "parallel", "concurrent", "meanwhile"]
    
    # Determine complexity level
    complexity = "low"
    for level, indicators in complexity_indicators.items():
        if any(indicator in description_lower for indicator in indicators):
            complexity = level
            break
    
    # Suggest decomposition type
    has_sequential = any(indicator in description_lower for indicator in sequential_indicators)
    has_parallel = any(indicator in description_lower for indicator in parallel_indicators)
    
    if has_sequential and has_parallel:
        decomposition_type = "mixed"
    elif has_sequential:
        decomposition_type = "sequential"
    elif has_parallel:
        decomposition_type = "parallel"
    else:
        decomposition_type = "simple"
    
    # Estimate subtask count
    word_count = len(task_description.split())
    estimated_subtasks = min(max(2, word_count // 20), 8)  # 2-8 subtasks based on length
    
    return {
        "complexity": complexity,
        "decomposition_type": decomposition_type,
        "estimated_subtasks": estimated_subtasks,
        "has_sequential_indicators": has_sequential,
        "has_parallel_indicators": has_parallel,
        "word_count": word_count,
        "suggestion": f"Recommend {decomposition_type} decomposition with ~{estimated_subtasks} subtasks"
    }