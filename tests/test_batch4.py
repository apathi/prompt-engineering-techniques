#!/usr/bin/env python3
"""
Batch 4 execution script - Run all specialized and advanced application techniques.
Executes techniques 16-22 (excluding T21 as requested) and demonstrates auto-save functionality.

Note: Technique 21 (Security and Safety) is intentionally excluded from automated 
testing as per user request, since it contains actual malicious prompt examples 
that should only be run manually for security testing purposes.
"""

import os
import sys
import time

# Add parent directory to path for shared_utils access
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared_utils import setup_logger

def run_technique(module_path, class_name, description):
    """Run a single technique and return success status."""
    logger = setup_logger("batch_runner")
    
    print(f"\n{'='*60}")
    print(f"🚀 RUNNING: {description}")
    print(f"{'='*60}")
    
    try:
        # Import and run the technique's main function directly
        import importlib
        
        # Clear module cache to avoid conflicts
        if module_path in sys.modules:
            del sys.modules[module_path]
        
        # Import the technique module
        technique_module = importlib.import_module(module_path)
        main_function = getattr(technique_module, "main")
        
        # Change to parent directory for proper output path
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Run the main function which includes OutputManager
        main_function()
        
        logger.info(f"✅ {description} completed successfully")
        
        # Check if output file was created in output folder
        output_file_map = {
            "06_Specialized_Applications.16_negative_prompting": "16-negative-prompting_output.txt",
            "06_Specialized_Applications.17_prompt_formatting_structure": "17-prompt-formatting-structure_output.txt",
            "06_Specialized_Applications.18_task_specific_prompts": "18-task-specific-prompts_output.txt",
            "07_Advanced_Applications.19_multilingual_prompting": "19-multilingual-prompting_output.txt",
            "07_Advanced_Applications.20_ethical_considerations": "20-ethical-considerations_output.txt",
            "07_Advanced_Applications.22_evaluating_effectiveness": "22-evaluating-effectiveness_output.txt"
        }
        
        expected_output_file = output_file_map.get(module_path)
        if expected_output_file:
            output_path = os.path.join("output", expected_output_file)
            if os.path.exists(output_path):
                logger.info(f"📁 Output saved to: {output_path}")
            else:
                logger.warning(f"⚠️  Expected output file not found: {output_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to run {description}: {str(e)}")
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_all_techniques():
    """Run all Batch 4 techniques and return success count."""
    
    # Define techniques to test - following the same pattern as other batch test scripts
    # NOTE: Technique 21 (Security and Safety) is intentionally excluded
    # as it contains malicious prompt examples for security testing only
    techniques = [
        ("06_Specialized_Applications.16_negative_prompting", "NegativePrompting", "Negative Prompting"),
        ("06_Specialized_Applications.17_prompt_formatting_structure", "PromptFormattingStructure", "Prompt Formatting Structure"),
        ("06_Specialized_Applications.18_task_specific_prompts", "TaskSpecificPrompts", "Task Specific Prompts"),
        ("07_Advanced_Applications.19_multilingual_prompting", "MultilingualPrompting", "Multilingual Prompting"),
        ("07_Advanced_Applications.20_ethical_considerations", "EthicalConsiderations", "Ethical Considerations"),
        # Technique 21 intentionally excluded - contains malicious examples for security testing
        ("07_Advanced_Applications.22_evaluating_effectiveness", "EvaluatingEffectiveness", "Evaluating Effectiveness")
    ]
    
    successful_runs = 0
    
    print("🎯 Starting Batch 4 execution - Specialized & Advanced Applications (16-22, excluding T21)")
    print("Each technique will display results and auto-save progress...")
    
    for module_path, class_name, description in techniques:
        if run_technique(module_path, class_name, description):
            successful_runs += 1
        
        # Brief pause between techniques
        time.sleep(2)
    
    return successful_runs, len(techniques)

def main():
    """Main execution function."""
    
    print("🧪 PROMPT ENGINEERING BATCH 4 TEST RUNNER")
    print("Testing Techniques 16-22 (Advanced and Specialized Applications)")
    print("="*70)
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    
    print("✅ OPENAI_API_KEY is configured")
    
    start_time = time.time()
    successful_runs, total_techniques = run_all_techniques()
    end_time = time.time()
    
    # Print summary
    print(f"\n{'='*70}")
    print("📊 BATCH 4 TEST SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Successful runs: {successful_runs}")
    print(f"❌ Failed runs: {total_techniques - successful_runs}")
    print(f"⏭️  Skipped techniques: 1 (Technique 21 - Security Testing)")
    print(f"🎯 Total techniques in batch: {total_techniques + 1}")
    print(f"⏱️  Total execution time: {end_time - start_time:.1f} seconds")
    
    print(f"\n📝 Note: Technique 21 (Security and Safety) was skipped as requested.")
    print(f"   This technique contains actual malicious prompt examples and should")
    print(f"   only be run manually for security testing purposes.")
    
    # Final status
    if successful_runs == total_techniques:
        print(f"\n🎉 All {successful_runs} tested techniques completed successfully!")
        print("📁 Output files have been generated in the 'output/' directory.")
    else:
        failed_runs = total_techniques - successful_runs
        print(f"\n⚠️  {failed_runs} technique(s) encountered errors. Check logs above.")
    
    print(f"\n🏁 Batch 4 testing completed!")

if __name__ == "__main__":
    main()