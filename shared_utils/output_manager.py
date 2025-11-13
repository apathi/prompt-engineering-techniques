"""
Output Manager for Prompt Engineering Implementations

Provides clean, modular output handling that saves results to files
while also displaying to console without debug information.
"""

import os
from typing import Dict, Any, List
from datetime import datetime
import time


class OutputManager:
    """Manages clean output display and file saving for technique results."""
    
    def __init__(self, technique_name: str, base_dir: str = "."):
        """
        Initialize output manager for a specific technique.
        
        Args:
            technique_name: Name of the technique (e.g., "intro-prompt-engineering")
            base_dir: Base directory where output file should be saved (legacy parameter, now auto-detected)
        """
        self.technique_name = technique_name
        self.base_dir = base_dir
        
        # Always use project root output folder, regardless of execution location
        project_root = self._find_project_root()
        output_dir = os.path.join(project_root, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        self.output_file = os.path.join(output_dir, f"{technique_name}_output.txt")
        self.output_lines = []
    
    def _find_project_root(self) -> str:
        """
        Find the project root directory by looking for CLAUDE.md file.
        This ensures all output files go to the centralized output folder.
        """
        current_dir = os.path.abspath(".")
        
        # Walk up the directory tree looking for CLAUDE.md (project root marker)
        while current_dir != os.path.dirname(current_dir):  # Stop at filesystem root
            if os.path.exists(os.path.join(current_dir, "CLAUDE.md")):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        
        # Fallback to current directory if CLAUDE.md not found
        return os.path.abspath(".")
    
    def add_line(self, line: str = ""):
        """Add a line to both console output and file buffer."""
        print(line)
        self.output_lines.append(line)
    
    def add_header(self, title: str, char: str = "=", width: int = 60):
        """Add a formatted header with execution timestamp."""
        # Get local timezone abbreviation
        timezone_abbr = time.tzname[time.daylight]
        
        # Format timestamp as requested: mm/dd/yy, hh:mm:ss AM/PM TZ
        now = datetime.now()
        timestamp = now.strftime(f"%m/%d/%y, %I:%M:%S %p {timezone_abbr}")
        
        header = char * width
        self.add_line(header)
        self.add_line(title.center(width))
        self.add_line(header)
        self.add_line(f"Execution Time: {timestamp}")
        self.add_line(header)
    
    def add_section_header(self, title: str, char: str = "=", width: int = 50):
        """Add a section header."""
        self.add_line(f"\n{char * width}")
        self.add_line(f"TECHNIQUE: {title}")
        self.add_line(f"{char * width}")
    
    def add_example_header(self, example_num: int, title: str = None):
        """Add an example header."""
        if title:
            self.add_line(f"\n--- Example {example_num}: {title} ---")
        else:
            self.add_line(f"\n--- Example {example_num} ---")
    
    def add_key_value(self, key: str, value: str, max_length: int = None):
        """Add a key-value pair with optional truncation."""
        # Note: max_length parameter preserved for compatibility but truncation removed
        self.add_line(f"{key}: {value}")
    
    def add_cost_summary(self, client):
        """Add cost summary section."""
        self.add_line(f"\n{'=' * 60}")
        self.add_line("COST SUMMARY")
        self.add_line(f"{'=' * 60}")
        
        # Capture cost summary to string instead of direct print
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = cost_output = io.StringIO()
        
        try:
            client.print_cost_summary()
            cost_text = cost_output.getvalue()
            # Add each line from cost summary
            for line in cost_text.strip().split('\n'):
                self.output_lines.append(line)
                print(line, file=old_stdout)  # Still display to console
        finally:
            sys.stdout = old_stdout
    
    def save_to_file(self, is_final_save: bool = True):
        """Save all collected output to the file."""
        try:
            # Add timestamp header
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if is_final_save:
                # Final save includes completion status
                file_content = [
                    f"# {self.technique_name.replace('-', ' ').title()} - Output",
                    f"# Generated: {timestamp}",
                    f"# Status: COMPLETED",
                    f"# Clean output without debug information",
                    "",
                    *self.output_lines
                ]
                message = f"\n✅ Final output saved to: {self.output_file}"
            else:
                # Intermediate save (shouldn't normally be called directly now)
                file_content = [
                    f"# {self.technique_name.replace('-', ' ').title()} - Output",
                    f"# Generated: {timestamp}",
                    f"# Status: IN PROGRESS",
                    f"# Auto-saved to preserve partial results",
                    "",
                    *self.output_lines
                ]
                message = f"📁 Progress saved to: {self.output_file}"
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(file_content))
            
            if is_final_save:
                print(message)
            
        except Exception as e:
            print(f"Warning: Could not save output to file: {e}")
    
    def display_results(self, results: Dict[str, Any]):
        """
        Display technique results in a clean format.
        This is the main method that handles different result structures.
        Auto-saves after each section to ensure partial results are captured.
        """
        examples = results.get("examples", [])
        total_sections = len(examples)
        
        for i, example in enumerate(examples, 1):
            self.add_section_header(example.get('technique', f'Example {i}'))
            
            # Display description and rationale if available
            if example.get('description'):
                self.add_key_value("Description", example['description'])
            if example.get('why_this_works'):
                self.add_key_value("Why This Works", example['why_this_works'])
            
            # Handle different result structures
            if "examples" in example:
                self._display_standard_examples(example["examples"])
            elif "conversation" in example:
                self._display_conversation(example["conversation"])
            elif "strategies" in example:
                self._display_strategies(example["strategies"])
            elif "without_context" in example and "with_context" in example:
                self._display_context_comparison(example)
            elif "single_turn" in example and "multi_turn" in example:
                self._display_structure_comparison(example)
            elif "task" in example and "test_input" in example:
                self._display_comparative_analysis(example)
            elif "test_scenarios" in example:
                self._display_test_scenarios(example)
            elif "evaluation_results" in example:
                self._display_evaluation_results(example)
            elif "optimization_iterations" in example:
                self._display_optimization_results(example)
            
            # Auto-save after each section to ensure partial results are captured
            self._auto_save_progress(i, total_sections)
    
    def _auto_save_progress(self, current_section: int, total_sections: int):
        """
        Auto-save progress after each section.
        Ensures partial results are always captured even if process is interrupted.
        """
        try:
            # Add progress note
            progress_note = f"\n[Progress: {current_section}/{total_sections} sections completed]"
            self.output_lines.append(progress_note)
            
            # Save current progress
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_content = [
                f"# {self.technique_name.replace('-', ' ').title()} - Output",
                f"# Generated: {timestamp}",
                f"# Progress: {current_section}/{total_sections} sections completed",
                f"# Auto-saved after each section to preserve partial results",
                "",
                *self.output_lines
            ]
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(file_content))
            
            # Only show save message for intermediate saves if user needs to see progress
            if current_section < total_sections:
                print(f"📁 Progress auto-saved ({current_section}/{total_sections} sections)")
            
        except Exception as e:
            # Don't interrupt the main process for save failures
            pass
    
    def _display_standard_examples(self, examples: List[Dict[str, Any]]):
        """Display standard examples format."""
        for i, ex in enumerate(examples, 1):
            # Determine title based on example content
            title = (ex.get('category') or 
                    ex.get('template_type') or 
                    ex.get('pattern') or 
                    ex.get('approach') or 
                    ex.get('type') or 
                    'Unknown')
            
            self.add_example_header(i, title)
            
            # Display based on example structure
            if "clarity_level" in ex:
                self.add_key_value("Clarity Level", ex['clarity_level'])
                self.add_key_value("Prompt", ex['prompt'])
                self.add_key_value("Description", ex.get('description', 'N/A'))
            elif "template_type" in ex:
                self.add_key_value("Template Type", ex['template_type'])
                self.add_key_value("Structure", ex['structure'])
            elif "pattern" in ex:
                self.add_key_value("Pattern", ex['pattern'])
                self.add_key_value("Statement", ex['statement'])
            elif "approach" in ex:
                self.add_key_value("Approach", ex['approach'])
                self.add_key_value("Problem", ex['problem'])
            elif "condition" in ex:
                self.add_key_value("Condition", ex['condition'])
                self.add_key_value("Input", str(ex['input']))
            elif "case" in ex:
                self.add_line(f"Case {ex['case']}:")
                self.add_key_value("  Task", ex['task'])
                self.add_key_value("  Context", ex['context'], 50)
                self.add_key_value("  Constraints", ex['constraints'], 50)
            elif "template_parts" in ex:
                self.add_key_value("Composed from", ', '.join(ex['template_parts']))
                self.add_key_value("Project", ex['project_data']['project_name'])
            elif "items" in ex:
                if isinstance(ex['items'], str):
                    self.add_key_value("Items", ex['items'], 100)
                else:
                    self.add_key_value("Items", ', '.join(ex['items']))
            elif "input" in ex and "prediction" in ex:
                self.add_key_value("Input", ex['input'])
                self.add_key_value("Prediction", ex['prediction'])
            elif "text" in ex and "task" in ex:
                self.add_key_value("Text", ex['text'])
                self.add_key_value("Task", ex['task'])
                self.add_key_value("Result", ex['result'])
            elif "input" in ex and "output" in ex:
                self.add_key_value("Input", ex['input'])
                self.add_key_value("Output", ex['output'])
            elif "strategy" in ex:
                self.add_key_value("Strategy", ex['strategy'])
                self.add_key_value("Description", ex['description'])
                self.add_key_value("Test Input", ex['test_input'])
                self.add_key_value("Prediction", ex['prediction'])
                self.add_key_value("Examples Used", f"{len(ex['examples_used'])} examples")
            elif "product" in ex:
                self.add_key_value("Product", ex['product'])
                self.add_key_value("Zero-shot", ex['zero_shot'])
                self.add_key_value("Few-shot", ex['few_shot'])
            elif "num_examples" in ex:
                self.add_key_value("Number of Examples", str(ex['num_examples']))
                self.add_key_value("Test Input", ex['test_input'])
                self.add_key_value("Prediction", ex['prediction'])
            elif "prompt_style" in ex:
                self.add_key_value("Prompt Style", ex['prompt_style'])
            elif "format" in ex:
                self.add_key_value("Format", ex['format'])
                if ex.get('input', 'N/A') != "N/A":
                    self.add_key_value("Input", ex['input'])
            
            # Always show full response if available
            response = ex.get('response', 'No response')
            self.add_key_value("Response", response)
    
    def _display_conversation(self, conversation: List[Dict[str, Any]]):
        """Display conversation format."""
        self.add_line("\nConversation Flow:")
        for turn in conversation:
            self.add_line(f"\nTurn {turn['turn']}:")
            user_input = turn.get('user_input', turn.get('topic', 'N/A'))
            self.add_key_value("User", user_input)
            
            response = turn['response']
            if isinstance(response, str):
                self.add_key_value("Assistant", response)
            else:
                self.add_key_value("Assistant", str(response))
            
            if "context_length" in turn:
                self.add_key_value("Context Length", f"{turn['context_length']} exchanges")
    
    def _display_strategies(self, strategies: Dict[str, Any]):
        """Display memory strategies format."""
        for strategy_name, strategy_data in strategies.items():
            self.add_line(f"\n--- {strategy_name.replace('_', ' ').title()} ---")
            self.add_key_value("Description", strategy_data['description'])
            self.add_line("Sample responses:")
            for turn in strategy_data['conversation'][:3]:  # Show first 3
                self.add_line(f"  Turn {turn['turn']}: {turn['response']}")
    
    def _display_context_comparison(self, example: Dict[str, Any]):
        """Display context comparison format."""
        self.add_key_value("Initial Context", example['initial_context'], 100)
        self.add_key_value("Follow-up Question", example['follow_up_question'])
        self.add_line("\n--- Without Context ---")
        self.add_key_value("Response", example['without_context']['response'], 200)
        self.add_line("\n--- With Context ---")
        self.add_key_value("Response", example['with_context']['response'], 200)
    
    def _display_structure_comparison(self, example: Dict[str, Any]):
        """Display structure comparison format."""
        self.add_line("\n--- Single-Turn Responses ---")
        for item in example["single_turn"]:
            self.add_key_value("Q", item['question'])
            self.add_key_value("A", item['response'], 150)
        
        self.add_line("\n--- Multi-Turn Responses ---")
        for item in example["multi_turn"]:
            self.add_key_value("Q", item['question'])
            self.add_key_value("A", item['response'], 150)
    
    def _display_comparative_analysis(self, example: Dict[str, Any]):
        """Display comparative analysis format."""
        self.add_key_value("Task", example['task'])
        self.add_key_value("Test Input", example['test_input'], 100)
        self.add_line("\nComparison of prompt styles:")
        for ex in example.get("examples", []):
            self.add_line(f"\n{ex['prompt_style']} Style:")
            self.add_line(f"  {ex['response']}")
    
    def _display_test_scenarios(self, example: Dict[str, Any]):
        """Display test scenarios format for security and evaluation techniques."""
        test_scenarios = example.get("test_scenarios", [])
        if example.get("task"):
            self.add_key_value("Task", example["task"])
        
        self.add_line(f"\nTest Scenarios ({len(test_scenarios)} total):")
        for i, scenario in enumerate(test_scenarios, 1):
            self.add_line(f"\n--- Test Scenario {i} ---")
            
            # Handle different scenario structures
            if "test_category" in scenario:
                self.add_key_value("Category", scenario["test_category"])
                if "input_sample" in scenario:
                    self.add_key_value("Input Sample", scenario["input_sample"])
                if "threat_analysis" in scenario:
                    analysis = scenario["threat_analysis"]
                    self.add_key_value("Threat Type", analysis.get("detected_type", "N/A"))
                    self.add_key_value("Threat Level", analysis.get("threat_level", "N/A"))
                    self.add_key_value("Confidence", f"{analysis.get('confidence', 0):.2f}")
                if "security_response" in scenario:
                    response = scenario["security_response"]
                    self.add_key_value("Was Blocked", str(response.get("was_blocked", False)))
                    self.add_key_value("Response Preview", response.get("response_preview", "N/A"))
            elif "prompt_name" in scenario:
                self.add_key_value("Prompt Name", scenario["prompt_name"])
                self.add_key_value("Overall Score", f"{scenario.get('overall_score', 0):.3f}")
                self.add_key_value("Quality Rating", scenario.get("quality_rating", "N/A"))
    
    def _display_evaluation_results(self, example: Dict[str, Any]):
        """Display evaluation results format."""
        evaluation_results = example.get("evaluation_results", [])
        if example.get("test_topic"):
            self.add_key_value("Test Topic", example["test_topic"])
        
        self.add_line(f"\nEvaluation Results ({len(evaluation_results)} prompts tested):")
        for i, result in enumerate(evaluation_results, 1):
            self.add_line(f"\n--- Evaluation {i}: {result.get('prompt_name', 'Unknown')} ---")
            self.add_key_value("Prompt Preview", result.get("prompt_preview", "N/A"))
            self.add_key_value("Overall Score", f"{result.get('overall_score', 0):.3f}")
            self.add_key_value("Quality Rating", result.get("quality_rating", "N/A"))
            
            # Display metrics breakdown
            metrics = result.get("metrics_breakdown", {})
            if metrics:
                self.add_line("\nMetrics Breakdown:")
                for metric_name, metric_data in metrics.items():
                    if isinstance(metric_data, dict):
                        score = metric_data.get("score", 0)
                        self.add_line(f"  {metric_name}: {score:.3f}")
                    else:
                        self.add_line(f"  {metric_name}: {metric_data}")
    
    def _display_optimization_results(self, example: Dict[str, Any]):
        """Display optimization iterations format."""
        optimization_iterations = example.get("optimization_iterations", [])
        if example.get("task"):
            self.add_key_value("Optimization Task", example["task"])
        
        self.add_line(f"\nOptimization Iterations ({len(optimization_iterations)} iterations):")
        for iteration in optimization_iterations:
            iter_num = iteration.get("iteration", "Unknown")
            self.add_line(f"\n--- Iteration {iter_num}: {iteration.get('prompt_name', 'Unknown')} ---")
            self.add_key_value("Optimization Focus", iteration.get("optimization_focus", "N/A"))
            self.add_key_value("Overall Score", f"{iteration.get('overall_score', 0):.3f}")
            
            improvement = iteration.get("improvement_from_previous")
            if improvement is not None:
                self.add_key_value("Improvement from Previous", f"{improvement:+.3f}")
            
            # Show strong and weak areas
            strong_metrics = iteration.get("strong_metrics", [])
            weak_metrics = iteration.get("weak_metrics", [])
            if strong_metrics:
                self.add_key_value("Strong Areas", ", ".join(strong_metrics))
            if weak_metrics:
                self.add_key_value("Areas for Improvement", ", ".join(weak_metrics))