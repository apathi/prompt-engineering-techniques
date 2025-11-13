#!/usr/bin/env python3
"""
Batch 1 execution script - Run all LangChain implementations.
Executes all 5 techniques and demonstrates auto-save functionality.
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
            "01_Fundamental_Concepts.01_intro_prompt_engineering": "01-intro-prompt-engineering_output.txt",
            "01_Fundamental_Concepts.02_basic_prompt_structures": "02-basic-prompt-structures_output.txt",
            "01_Fundamental_Concepts.03_prompt_templates_variables": "03-prompt-templates-variables_output.txt",
            "02_Core_Techniques.04_zero_shot_prompting": "04-zero-shot-prompting_output.txt",
            "02_Core_Techniques.05_few_shot_learning": "05-few-shot-learning_output.txt"
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
    """Run all Batch 1 techniques in sequence."""
    techniques = [
        ("01_Fundamental_Concepts.01_intro_prompt_engineering", "IntroPromptEngineering", "Introduction to Prompt Engineering"),
        ("01_Fundamental_Concepts.02_basic_prompt_structures", "BasicPromptStructures", "Basic Prompt Structures"),
        ("01_Fundamental_Concepts.03_prompt_templates_variables", "PromptTemplatesVariables", "Prompt Templates and Variables"),
        ("02_Core_Techniques.04_zero_shot_prompting", "ZeroShotPrompting", "Zero-Shot Prompting"),
        ("02_Core_Techniques.05_few_shot_learning", "FewShotLearning", "Few-Shot Learning")
    ]
    
    start_time = time.time()
    successful_runs = 0
    
    print("🎯 Starting Batch 1 execution - All 5 LangChain techniques")
    print("Each technique will display results and auto-save progress...")
    
    for module_path, class_name, description in techniques:
        if run_technique(module_path, class_name, description):
            successful_runs += 1
        
        # Brief pause between techniques
        time.sleep(2)
    
    # Summary
    total_time = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"📊 BATCH 1 EXECUTION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful_runs}/{len(techniques)} techniques")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    
    # List created output files in output folder
    output_dir = "output"
    if os.path.exists(output_dir):
        output_files = [f for f in os.listdir(output_dir) if f.endswith('_output.txt')]
        if output_files:
            print(f"\n📁 Batch 1 output files created:")
            for file in sorted(output_files):
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path) / 1024  # KB
                print(f"   • {file_path} ({file_size:.1f} KB)")
    
    return successful_runs == len(techniques)

def main():
    """Run all Batch 1 techniques and demonstrate auto-save functionality."""
    print("=" * 60)
    print("BATCH 1 LANGCHAIN EXECUTION")
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
        print("\n🎉 All techniques completed successfully!")
        print("📁 Check the generated files in the output/ folder for clean results")
    else:
        print("\n⚠️  Some techniques may have failed - check logs above")
    
    return success

if __name__ == "__main__":
    main()