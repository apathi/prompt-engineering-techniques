# Prompt Engineering Implementations Project

## Project Overview
Implementation of all 22 prompt engineering techniques from the NirDiamant/Prompt_Engineering repository.

**Repository:** https://github.com/NirDiamant/Prompt_Engineering
**Target:** Production-ready Python implementations with OpenAI API integration

## Implementation Approach (Batch 1 Completed)

### Architecture Decision Process

#### Implementation Comparison Analysis
We evaluated three approaches before finalizing our implementation:

1. **Original GitHub Notebooks** (from NirDiamant/Prompt_Engineering)
   - Simple, educational approach
   - Direct OpenAI API calls
   - Jupyter notebook format
   - Focus on concept demonstration

2. **User's Notion Page Implementation**
   - Production-ready architecture
   - Error handling and cost tracking
   - Structured Python modules
   - Systematic testing approach

3. **Final Decision: Hybrid Approach** ✅
   - Follow original GitHub patterns for technique structure and simplicity
   - Incorporate production architectural improvements (cost tracking, error handling)
   - Use modern LangChain framework instead of direct OpenAI API
   - Maintain educational value while ensuring production robustness

### Technical Specifications Followed

#### Core Architecture
```python
# Framework Migration
- FROM: Direct OpenAI API calls
- TO: LangChain with Expression Language (LCEL)

# Key Components
from shared_utils import LangChainClient, CostTracker, OutputManager
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

# Modern Chain Syntax
chain = prompt | llm | parser  # LCEL pipe operators
```

#### Implementation Requirements Followed
- **Code Quality:** Concise, modular, clean - no unnecessary comments
- **Standards:** PEP 8 with comprehensive type hints throughout
- **Architecture:** Follow original GitHub notebook patterns with production features
- **Framework:** Modern LangChain patterns, avoiding deprecated classes
- **Testing:** Systematic approach with `run_all_examples()` method

#### Output Management Specifications
```python
# OutputManager Features Implemented
- Dual display: Console + file output
- Auto-save: After each section completion
- Progress tracking: "Progress: 2/4 sections completed"
- Clean formatting: No debug information in output files
- Status indicators: COMPLETED vs IN PROGRESS
- Timestamp headers with generation metadata
```

#### Quality Criteria Achieved
**From Original Requirements:**
- ✅ Production-ready with proper error handling
- ✅ Cost tracking per session with token usage
- ✅ Modular architecture with shared utilities
- ✅ Clean documentation (no unnecessary comments)
- ✅ Systematic testing approach

**From LangChain Migration:**
- ✅ Modern patterns (LCEL syntax with pipe operators)
- ✅ Proper memory management with RunnableWithMessageHistory
- ✅ Cost callback integration via TokenUsageCallback
- ✅ Auto-save functionality preventing data loss
- ✅ Deprecated pattern avoidance (except minor functional ones)

### Key Implementation Decisions Made

1. **Framework Choice:** LangChain over Direct OpenAI API
   - Better abstraction for prompt engineering patterns
   - Built-in support for chains, templates, and memory
   - More maintainable and extensible codebase

2. **Architecture Strategy:** Hybrid Approach
   - Original simplicity for educational value
   - Production features for robustness
   - Modern best practices for maintainability

3. **Output Strategy:** Auto-save After Each Section
   - Prevents data loss on timeouts/interruptions
   - Transparent progress indicators
   - Dual console/file output for usability

4. **Cost Integration:** Callback-based Tracking
   - Per-technique granular analysis
   - Session-based aggregation
   - Real-time cost monitoring

5. **Memory Management:** RunnableWithMessageHistory
   - Modern LangChain pattern over deprecated ConversationChain
   - Better integration with LCEL chains
   - Cleaner session management

### Testing Evolution
**test_batch1.py Development:**
1. **Phase 1:** Import and dependency checker
2. **Phase 2:** Basic execution runner
3. **Phase 3:** Full technique runner with OutputManager integration

**Final Pattern:**
```bash
source .venv/bin/activate
python test_batch1.py  # Runs all 5 techniques, creates output files
```

### Success Metrics Achieved
- ✅ All 5 techniques implemented and functional
- ✅ Cost tracking operational (~$0.01 for full batch execution)
- ✅ Output files generated automatically with clean formatting
- ✅ Modular, maintainable code structure established
- ✅ Original educational patterns preserved with modern implementation
- ✅ Production-ready error handling and robustness
- ✅ Systematic testing approach with unified runner

### Established Code Pattern Template (Updated for Category Structure)
```python
#!/usr/bin/env python3
"""
Technique XX: Technique Name - Brief Description

Demonstrates [technique concepts] with [implementation approach].
"""

import os
import sys
# CRITICAL: Updated path for category structure (2 levels deep)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, OutputManager
from typing import Dict, List, Any
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class TechniqueName:
    """Technique description with category-based implementation."""
    
    def __init__(self):
        self.client = LangChainClient()
        self.llm = self.client.get_llm()
        self.output_manager = OutputManager("XX-technique-name")  # Hyphenated for output files
    
    def run_examples(self):
        """Execute progressive examples demonstrating the technique."""
        
        self.output_manager.add_header("TECHNIQUE XX: TECHNIQUE NAME")
        self.output_manager.add_line("Brief description of technique purpose")
        self.output_manager.add_line()
        
        results = {
            "examples": [
                self._example_1_basic_implementation(),
                self._example_2_advanced_implementation()
            ]
        }
        
        self.output_manager.display_results(results)
        
        # CRITICAL: Add cost summary for all techniques
        self.client.print_cost_summary()
        
        self.output_manager.save_to_file()
        return results
    
    def _example_1_basic_implementation(self):
        """Example 1: Basic technique demonstration."""
        
        prompt = PromptTemplate.from_template("Template here...")
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({"input": "value"}, config={"tags": ["technique_xx"]})
        
        return {
            "technique": "Basic Implementation",
            "examples": [{"response": response, "why_this_works": "Explanation..."}]
        }


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("TECHNIQUE XX: TECHNIQUE NAME")
    print("="*60)
    
    technique = TechniqueName()
    results = technique.run_examples()
    return results


if __name__ == "__main__":
    main()
```

#### Key Changes for Category Structure:
1. **Import Path**: `sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` (2 levels up)
2. **File Location**: `XX_Category_Name/XX_technique_name.py` (underscores for Python modules)
3. **Output Naming**: `OutputManager("XX-technique-name")` (hyphens preserved for output files)
4. **Cost Tracking**: Always include `self.client.print_cost_summary()`

## Technical Specifications

### Core Requirements
- **OpenAI API:** Version ≥1.0.0
- **LangChain:** Latest version with LCEL support
- **Default Model:** GPT-4o-mini (configurable)
- **Python Standards:** PEP 8 with type hints
- **API Key:** Environment variable `OPENAI_API_KEY`
- **Dependencies:** Single requirements.txt at root level
- **Logging:** INFO level by default
- **Cost Tracking:** Per-session tracking with account balance monitoring
- **Output:** Auto-save functionality with dual console/file output

### Project Structure (Category-Based Organization)
```
prompt-engineering-implementations/
├── output/                          # All output files (auto-created)
│   ├── 01-intro-prompt-engineering_output.txt
│   ├── 02-basic-prompt-structures_output.txt  
│   ├── 03-prompt-templates-variables_output.txt
│   ├── 04-zero-shot-prompting_output.txt
│   ├── 05-few-shot-learning_output.txt
│   ├── 06-chain-of-thought_output.txt
│   ├── 07-self-consistency_output.txt
│   ├── 08-constrained-generation_output.txt
│   ├── 09-role-prompting_output.txt
│   ├── 10-task-decomposition_output.txt
│   ├── 11-prompt-chaining_output.txt
│   ├── 12-instruction-engineering_output.txt
│   ├── 13-prompt-optimization_output.txt
│   ├── 14-handling-ambiguity_output.txt
│   └── 15-length-management_output.txt
├── shared_utils/                    # Shared utilities (unchanged)
│   ├── __init__.py
│   ├── langchain_client.py         # LangChain wrapper with cost tracking
│   ├── output_manager.py           # Clean output handling with auto-save
│   ├── cost_tracker.py            # Token usage & cost estimation + balance
│   ├── logger.py                  # Simple logging setup
│   ├── voting_utils.py            # Voting mechanisms for self-consistency
│   ├── constraint_validator.py    # Format and constraint validation
│   ├── task_decomposer.py         # Task breakdown and dependency management
│   └── prompt_chaining_utils.py   # Advanced chaining utilities
├── 01_Fundamental_Concepts/         # Category: Basic concepts and foundations
│   ├── __init__.py
│   ├── 01_intro_prompt_engineering.py
│   ├── 02_basic_prompt_structures.py
│   └── 03_prompt_templates_variables.py
├── 02_Core_Techniques/             # Category: Essential prompt techniques  
│   ├── __init__.py
│   ├── 04_zero_shot_prompting.py
│   ├── 05_few_shot_learning.py
│   └── 06_chain_of_thought.py
├── 03_Advanced_Strategies/         # Category: Sophisticated approaches
│   ├── __init__.py
│   ├── 07_self_consistency.py
│   ├── 08_constrained_generation.py
│   └── 09_role_prompting.py
├── 04_Advanced_Implementations/    # Category: Complex implementations
│   ├── __init__.py
│   ├── 10_task_decomposition.py
│   ├── 11_prompt_chaining.py
│   └── 12_instruction_engineering.py
├── 05_Optimization_and_Refinement/ # Category: Enhancement techniques
│   ├── __init__.py
│   ├── 13_prompt_optimization.py
│   ├── 14_handling_ambiguity.py
│   └── 15_length_management.py
├── 06_Specialized_Applications/    # Category: Domain-specific applications
│   ├── __init__.py
│   ├── 16_negative_prompting.py    # (Planned)
│   ├── 17_prompt_formatting.py    # (Planned)
│   └── 18_task_specific_prompts.py # (Planned)
├── 07_Advanced_Applications/       # Category: Advanced use cases
│   ├── __init__.py
│   ├── 19_multilingual_prompting.py    # (Planned)
│   ├── 20_ethical_considerations.py    # (Planned)
│   ├── 21_prompt_security.py          # (Planned)
│   └── 22_evaluating_effectiveness.py # (Planned)
├── tests/                          # Test batch runners
│   ├── test_batch1.py             # Runner for techniques 1-5
│   ├── test_batch2.py             # Runner for techniques 6-10
│   └── test_batch3.py             # Runner for techniques 11-15
├── requirements.txt
└── CLAUDE.md
```

## 22 Prompt Engineering Techniques

| # | Category | Technique | Implementation Status |
|---|----------|-----------|----------------------|
| 1 | Fundamental | Introduction to Prompt Engineering | ✅ Completed |
| 2 | Fundamental | Basic Prompt Structures | ✅ Completed |
| 3 | Fundamental | Prompt Templates and Variables | ✅ Completed |
| 4 | Core | Zero-Shot Prompting | ✅ Completed |
| 5 | Core | Few-Shot Learning | ✅ Completed |
| 6 | Core | Chain of Thought (CoT) | ✅ Completed |
| 7 | Advanced | Self-Consistency | ✅ Completed |
| 8 | Advanced | Constrained Generation | ✅ Completed |
| 9 | Advanced | Role Prompting | ✅ Completed |
| 10 | Advanced | Task Decomposition | ✅ Completed |
| 11 | Advanced | Prompt Chaining | Planned |
| 12 | Advanced | Instruction Engineering | Planned |
| 13 | Optimization | Prompt Optimization | Planned |
| 14 | Optimization | Handling Ambiguity | Planned |
| 15 | Optimization | Length Management | Planned |
| 16 | Specialized | Negative Prompting | Planned |
| 17 | Specialized | Prompt Formatting | Planned |
| 18 | Specialized | Task-Specific Prompts | Planned |
| 19 | Advanced | Multilingual Prompting | Planned |
| 20 | Advanced | Ethical Considerations | Planned |
| 21 | Advanced | Prompt Security | Planned |
| 22 | Advanced | Evaluating Effectiveness | Planned |

## Implementation Batches

### Batch 1: Foundational (Techniques 1-5)
**Status:** ✅ COMPLETED

#### Implementation Details
- **Approach:** Hybrid LangChain implementation
- **Pattern:** Each technique has 4-6 example methods demonstrating concepts
- **Structure:** Consistent main() → OutputManager → file output pattern
- **Testing:** Unified test_batch1.py runner for all techniques

#### Key Features Implemented
1. **01-intro-prompt-engineering**
   - Basic prompt structure progression
   - Template structure comparison
   - Fact-checking patterns
   - Problem-solving approaches

2. **02-basic-prompt-structures**
   - Clear vs vague comparisons
   - Structural components analysis
   - Context provision patterns
   - Constraint specification

3. **03-prompt-templates-variables**
   - Dynamic variable substitution
   - Conditional prompt generation
   - Template composition
   - Iterative refinement

4. **04-zero-shot-prompting**
   - Direct task specification
   - Role-based prompting
   - Format specification
   - Multi-step reasoning

5. **05-few-shot-learning**
   - Basic classification with examples
   - Multi-task learning
   - In-context custom tasks
   - Example selection strategies
   - Adaptive few-shot learning

### Batch 2: Advanced Techniques (Techniques 6-10)
**Status:** ✅ COMPLETED

#### Implementation Details
- **Approach:** Advanced LangChain implementation with specialized utilities
- **Pattern:** 2 progressively complex examples per technique with "why this works" explanations  
- **Features:** Voting mechanisms, constraint validation, task decomposition, role profiles
- **Testing:** Unified test_batch2.py runner for all techniques

#### Key Features Implemented
1. **06-chain-of-thought**
   - Mathematical reasoning progression (standard → CoT → advanced CoT)
   - Complex logical reasoning with systematic constraint analysis
   - Step-by-step problem decomposition and validation

2. **07-self-consistency**
   - Multiple reasoning paths with voting mechanisms
   - Complex decision-making with multi-perspective analysis
   - Democratic voting and semantic similarity voting

3. **08-constrained-generation**
   - Structured format generation with validation (JSON, bullet lists)
   - Multi-constraint compliance (format + content + tone rules)
   - Advanced constraint layering and violation detection

4. **09-role-prompting**
   - Professional domain expertise adoption (financial, technical, medical, marketing)
   - Multi-role consultation analysis with synthesis
   - Predefined role profiles with expertise domains

5. **10-task-decomposition**
   - Systematic project breakdown with dependency tracking
   - Complex workflow orchestration with parallel execution
   - Risk analysis and contingency planning

### Batch 3: Advanced Strategies (Techniques 11-15)
- Prompt Chaining
- Instruction Engineering
- Prompt Optimization
- Handling Ambiguity
- Length Management

### Batch 4: Specialized Applications (Techniques 16-22)
- Negative Prompting
- Prompt Formatting
- Task-Specific Prompts
- Multilingual Prompting
- Ethical Considerations
- Prompt Security
- Evaluating Effectiveness

## Cost Estimates

**GPT-4o-mini Pricing:**
- Input: ~$0.15/1M tokens
- Output: ~$0.60/1M tokens

**Per Technique Examples:**
- Simple examples (100-300 tokens): ~$0.0001-0.0003
- Complex examples (500-1000 tokens): ~$0.0005-0.001
- Full technique demonstration: ~$0.002-0.005

**Total Project Estimate:** ~$0.10-0.25 for all examples

## Safety & Budget Controls
- Max tokens: 1000 per example
- Temperature: 0.2 (predictable outputs)
- Rate limiting with exponential backoff
- Input sanitization and validation
- No sensitive data in examples

## Code Standards
- Production-ready with proper error handling
- Comprehensive docstrings and inline comments
- PEP 8 style guidelines
- Type hints throughout
- Modular, clean architecture
- Concise documentation
- **CRITICAL: NO OUTPUT TRUNCATION** - Always preserve complete LLM responses in output files and user displays. Users paid for full responses and should see them entirely. Any `response[:N] + "..."` patterns are forbidden.

### **CRITICAL OUTPUT FILE STANDARDS** 🎯
These standards MUST be followed for all implementations:

1. **File Naming Convention:** 
   - ALWAYS use chapter number prefix format: `XX-technique-name_output.txt`
   - Examples: `01-intro-prompt-engineering_output.txt`, `06-chain-of-thought_output.txt`
   - Use folder name format in OutputManager: `OutputManager("01-intro-prompt-engineering")`

2. **Output Directory Structure:**
   - ALL output files MUST be saved to `output/` folder
   - OutputManager automatically creates `output/` folder if needed
   - Never save output files to project root directory
   - Final structure: `output/01-intro-prompt-engineering_output.txt`

## Documentation Template
Each technique includes:
- **Overview:** Brief technique description
- **Setup:** Prerequisites and installation
- **Usage:** Step-by-step execution guide  
- **Examples:** 3+ working demonstrations
- **Cost Analysis:** Token usage and pricing
- **Troubleshooting:** Common issues and solutions
- **References:** Links to original notebook

## Implementation Progress
- [x] Repository access confirmed
- [x] Implementation plan created  
- [x] .claude file documentation
- [x] Shared utilities module (LangChain version)
- [x] Batch 1 implementation (Techniques 1-5)
- [x] Batch 2 implementation (Techniques 6-10)
- [x] Batch 3 implementation (Techniques 11-15)
- [x] Project restructuring with category-based organization
- [x] Response truncation removal (37 instances across 13 files)
- [x] Test runner migration to tests/ folder
- [x] Python module naming compliance (underscores)
- [ ] Batch 4 implementation (Techniques 16-22)

## Category-Based Structure Implementation (2025-09-03)

### Major Restructuring Completed
**Problem Solved:** The original nested folder structure (`XX-technique-name/main.py`) created import complexity and navigation challenges as the project scaled.

**Solution:** Reorganized all techniques into logical category folders with flat file structure:
- **01_Fundamental_Concepts/**: Basic concepts (Techniques 1-3)
- **02_Core_Techniques/**: Essential techniques (Techniques 4-6) 
- **03_Advanced_Strategies/**: Sophisticated approaches (Techniques 7-9)
- **04_Advanced_Implementations/**: Complex implementations (Techniques 10-12)
- **05_Optimization_and_Refinement/**: Enhancement techniques (Techniques 13-15)
- **06_Specialized_Applications/**: Domain-specific applications (Techniques 16-18)
- **07_Advanced_Applications/**: Advanced use cases (Techniques 19-22)

### Implementation Guidelines for Future Techniques

#### File Naming Convention
```python
# CORRECT: Python files use underscores for modules
06_Specialized_Applications/16_negative_prompting.py

# INCORRECT: Hyphens break Python imports  
06_Specialized_Applications/16-negative-prompting.py
```

#### Output File Naming (Unchanged)
```python
# OutputManager calls maintain existing convention
OutputManager("16-negative-prompting")  # Creates: 16-negative-prompting_output.txt
```

#### Import Pattern (Updated)
```python
# Standard import pattern for new structure
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared_utils import LangChainClient, OutputManager
# Techniques are now 2 levels deep: category_folder/ -> root/
```

#### Test Runner Pattern
```python
# New test file location: tests/test_batch4.py
techniques = [
    ("06_Specialized_Applications.16_negative_prompting", "NegativePrompting", "Negative Prompting"),
    ("06_Specialized_Applications.17_prompt_formatting", "PromptFormatting", "Prompt Formatting"),
    # ... etc
]
```

### Benefits Achieved
- ✅ **Clean Organization**: Techniques grouped by logical categories
- ✅ **Scalable Structure**: Ready for remaining 7 techniques (16-22)
- ✅ **Zero Breaking Changes**: All existing functionality preserved
- ✅ **Python Compliance**: Proper module naming with underscores
- ✅ **Simplified Navigation**: Flat file structure within categories
- ✅ **Maintained Compatibility**: Output files unchanged, import paths consistent

## Next Steps
1. ~~Create shared utilities (langchain_client, output_manager, cost_tracker, logger)~~ ✅
2. ~~Implement Batch 1 (Foundational techniques 1-5)~~ ✅
3. ~~Implement Batch 2 (Advanced techniques 6-10)~~ ✅
4. ~~Implement Batch 3 (Advanced strategies 11-15)~~ ✅
5. ~~Restructure project with category-based organization~~ ✅
6. ~~Remove response truncation and add cost tracking to all techniques~~ ✅
7. Implement Batch 4 (Specialized applications 16-22):
   - 16. Negative Prompting → `06_Specialized_Applications/16_negative_prompting.py`
   - 17. Prompt Formatting → `06_Specialized_Applications/17_prompt_formatting.py`  
   - 18. Task-Specific Prompts → `06_Specialized_Applications/18_task_specific_prompts.py`
   - 19. Multilingual Prompting → `07_Advanced_Applications/19_multilingual_prompting.py`
   - 20. Ethical Considerations → `07_Advanced_Applications/20_ethical_considerations.py`
   - 21. Prompt Security → `07_Advanced_Applications/21_prompt_security.py`
   - 22. Evaluating Effectiveness → `07_Advanced_Applications/22_evaluating_effectiveness.py`

---

# 🎯 CRITICAL IMPLEMENTATION GUIDELINES

## Category-Based Structure Rules (2025-09-03 Update)
**When implementing new techniques (16-22), ALWAYS follow these guidelines:**

### ✅ CORRECT File Structure:
```python
06_Specialized_Applications/16_negative_prompting.py  # Python module: underscores
OutputManager("16-negative-prompting")              # Output file: hyphens preserved
```

### ❌ INCORRECT File Structure:
```python
16-negative-prompting/main.py                       # Old nested structure - DON'T USE
06_Specialized_Applications/16-negative-prompting.py # Hyphens break Python imports
```

### 🔧 Required Import Pattern:
```python
# ALWAYS use this exact pattern for category-based structure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### 📁 Test Runner Location:
```python
# New techniques must be added to: tests/test_batch4.py  
techniques = [
    ("06_Specialized_Applications.16_negative_prompting", "NegativePrompting", "Negative Prompting"),
    # Format: ("Category.module_name", "ClassName", "Display Name")
]
```

### 💰 Cost Tracking Requirements:
```python
# EVERY technique MUST include cost tracking
self.client = LangChainClient()  # NOT get_llm()
self.client.print_cost_summary() # REQUIRED in run_examples()
```

---

# 🚫 CRITICAL PROJECT RULE

## NO OUTPUT TRUNCATION EVER
**When working on this project, NEVER implement response truncation patterns like:**
- `response[:N] + "..."`
- `if len(response) > N: response = response[:N] + "..."`
- Any character limits on LLM responses in output files

**Rationale:** Users pay for complete API responses and deserve to see the full content they paid for. Truncation was removed project-wide in 2025-09-03 across 37 instances in 13 files.

**Always preserve complete responses in output files and user displays.**