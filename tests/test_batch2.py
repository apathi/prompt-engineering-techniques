#!/usr/bin/env python3
"""
Batch 2 execution script - Run all advanced LangChain implementations.
Executes techniques 6-10 and demonstrates auto-save functionality.
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
        # Map module names to expected output file names
        output_file_map = {
            "02_Core_Techniques.06_chain_of_thought": "06-chain-of-thought_output.txt",
            "03_Advanced_Strategies.07_self_consistency": "07-self-consistency_output.txt", 
            "03_Advanced_Strategies.08_constrained_generation": "08-constrained-generation_output.txt",
            "03_Advanced_Strategies.09_role_prompting": "09-role-prompting_output.txt",
            "04_Advanced_Implementations.10_task_decomposition": "10-task-decomposition_output.txt"
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
        logger.error(f"❌ {description} failed: {e}")
        print(f"Error details: {e}")
        return False
    finally:
        # Clean up
        if module_path in sys.modules:
            del sys.modules[module_path]

def run_all_techniques():
    """Run all Batch 2 techniques in sequence."""
    techniques = [
        ("02_Core_Techniques.06_chain_of_thought", "ChainOfThoughtPrompting", "Chain of Thought (CoT) Prompting"),
        ("03_Advanced_Strategies.07_self_consistency", "SelfConsistencyPrompting", "Self-Consistency Prompting"),
        ("03_Advanced_Strategies.08_constrained_generation", "ConstrainedGeneration", "Constrained Generation"),
        ("03_Advanced_Strategies.09_role_prompting", "RolePrompting", "Role Prompting"),
        ("04_Advanced_Implementations.10_task_decomposition", "TaskDecomposition", "Task Decomposition")
    ]
    
    start_time = time.time()
    successful_runs = 0
    
    print("🎯 Starting Batch 2 execution - Advanced LangChain techniques (6-10)")
    print("Each technique will display results and auto-save progress...")
    
    for module_path, class_name, description in techniques:
        if run_technique(module_path, class_name, description):
            successful_runs += 1
        
        # Brief pause between techniques
        time.sleep(2)
    
    # Summary
    total_time = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"📊 BATCH 2 EXECUTION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful_runs}/{len(techniques)} techniques")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    
    # List created output files in output folder
    output_dir = "output"
    if os.path.exists(output_dir):
        batch2_output_files = [f for f in os.listdir(output_dir) if f.endswith('_output.txt') and any(
            technique in f for technique in ['06-chain-of-thought', '07-self-consistency', '08-constrained-generation', '09-role-prompting', '10-task-decomposition']
        )]
        
        if batch2_output_files:
            print(f"\n📁 Batch 2 output files created:")
            for file in sorted(batch2_output_files):
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"   • {file_path} ({file_size:.1f} KB)")
    
    return successful_runs == len(techniques)

def main():
    """Run all Batch 2 techniques and demonstrate auto-save functionality."""
    print("=" * 60)
    print("BATCH 2 LANGCHAIN EXECUTION - ADVANCED TECHNIQUES")
    print("=" * 60)
    
    # Quick API key check
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not set - API calls will fail")
        print("   Set with: export OPENAI_API_KEY='your_key_here'")
        print("   Or add to .env file in project root")
        return False
    else:
        print("✅ OPENAI_API_KEY is configured")
    
    # Run all techniques
    success = run_all_techniques()
    
    if success:
        print("\n🎉 All Batch 2 techniques completed successfully!")
        print("📁 Check the generated files in the output/ folder for clean results")
        print("\n🎓 Advanced Techniques Completed:")
        print("   • Chain of Thought: Step-by-step reasoning patterns")
        print("   • Self-Consistency: Multiple reasoning paths with voting")
        print("   • Constrained Generation: Format and rule compliance")
        print("   • Role Prompting: Professional domain expertise")
        print("   • Task Decomposition: Complex workflow breakdown")
    else:
        print("\n⚠️  Some techniques may have failed - check logs above")
    
    return success

if __name__ == "__main__":
    main()