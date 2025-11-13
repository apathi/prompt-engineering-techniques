#!/usr/bin/env python3
"""
Batch 3 execution script - Run all advanced strategies techniques.
Executes techniques 11-15 and demonstrates auto-save functionality.
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
            "04_Advanced_Implementations.11_prompt_chaining": "11-prompt-chaining_output.txt",
            "04_Advanced_Implementations.12_instruction_engineering": "12-instruction-engineering_output.txt",
            "05_Optimization_and_Refinement.13_prompt_optimization": "13-prompt-optimization_output.txt", 
            "05_Optimization_and_Refinement.14_handling_ambiguity": "14-handling-ambiguity_output.txt"
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
    """Run all Batch 3 techniques in sequence."""
    techniques = [
        ("04_Advanced_Implementations.11_prompt_chaining", "PromptChaining", "Prompt Chaining"),
        ("04_Advanced_Implementations.12_instruction_engineering", "InstructionEngineering", "Instruction Engineering"),
        ("05_Optimization_and_Refinement.13_prompt_optimization", "PromptOptimization", "Prompt Optimization"),
        ("05_Optimization_and_Refinement.14_handling_ambiguity", "HandlingAmbiguity", "Handling Ambiguity")
    ]
    
    start_time = time.time()
    successful_runs = 0
    
    print("🎯 Starting Batch 3 execution - Advanced Strategies (11-14)")
    print("Each technique will display results and auto-save progress...")
    
    for module_path, class_name, description in techniques:
        if run_technique(module_path, class_name, description):
            successful_runs += 1
        
        # Brief pause between techniques
        time.sleep(2)
    
    # Summary
    total_time = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"📊 BATCH 3 EXECUTION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful_runs}/{len(techniques)} techniques")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    
    # List created output files in output folder
    output_dir = "output"
    if os.path.exists(output_dir):
        batch3_output_files = [f for f in os.listdir(output_dir) if f.endswith('_output.txt') and any(
            technique in f for technique in ['11-prompt-chaining', '12-instruction-engineering', '13-prompt-optimization', '14-handling-ambiguity']
        )]
        
        if batch3_output_files:
            print(f"\n📁 Batch 3 output files created:")
            for file in sorted(batch3_output_files):
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"   • {file_path} ({file_size:.1f} KB)")
    
    return successful_runs == len(techniques)

def main():
    """Run all Batch 3 techniques and demonstrate auto-save functionality."""
    print("=" * 60)
    print("BATCH 3 LANGCHAIN EXECUTION - ADVANCED STRATEGIES")
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
        print("\n🎉 All Batch 3 techniques completed successfully!")
        print("📁 Check the generated files in the output/ folder for clean results")
        print("\n🎓 Advanced Strategy Techniques Completed:")
        print("   • Prompt Chaining: Enterprise-grade multi-step processing")
        print("   • Instruction Engineering: Clear, precise communication")
        print("   • Prompt Optimization: A/B testing and systematic improvement")
        print("   • Handling Ambiguity: Context-aware resolution strategies")
        print("\n💡 Note: Cost tracking available in techniques using LangChainClient")
    else:
        print("\n⚠️  Some techniques may have failed - check logs above")
    
    return success

if __name__ == "__main__":
    main()