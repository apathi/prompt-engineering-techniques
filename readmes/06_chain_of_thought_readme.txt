=================================================================
TECHNIQUE 06: CHAIN OF THOUGHT (CoT) PROMPTING
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Chain of Thought prompting teaches models to externalize step-by-step
reasoning, making complex problem-solving transparent and verifiable. The
technique demonstrates three levels of sophistication: standard direct
answers, basic step-by-step reasoning, and advanced systematic analysis
with validation phases—critical for tasks requiring auditable logic.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
Two advanced examples showcase progressive reasoning complexity:

**Mathematical Reasoning Progression:**
A complex delivery truck problem solved three ways to demonstrate
increasing sophistication:

Problem: "Truck travels 3 legs—First leg: 120 miles at 60 mph. Second leg:
180 miles at 45 mph. 30-minute break. Third leg: 90 miles at 50 mph. What's
total time including break?"

- **Standard Approach**: Direct answer without reasoning shown
  - Prompt: "Calculate total travel time"
  - Response: Final answer only (unclear how calculated)
  - Fast but opaque—errors undetectable

- **Basic CoT**: Explicit 4-step calculation process
  - Prompt: "Let's solve this step by step:"
  - Step 1: Calculate leg 1 time (120 ÷ 60 = 2 hours)
  - Step 2: Calculate leg 2 time (180 ÷ 45 = 4 hours)
  - Step 3: Calculate leg 3 time (90 ÷ 50 = 1.8 hours)
  - Step 4: Add break time and sum total
  - Response shows intermediate calculations

- **Advanced CoT**: 4-phase structured approach
  - Phase 1 (Analysis): Break problem into components, identify variables
  - Phase 2 (Strategy): Plan calculation sequence, note dependencies
  - Phase 3 (Calculations): Execute step-by-step with units
  - Phase 4 (Validation): Verify results, check reasonableness
  - Self-correction built into process

**Complex Logical Reasoning:**
A 5-person circular seating puzzle with 7 constraints demonstrates
systematic constraint satisfaction:

Problem: "5 people (Alice, Bob, Carol, Dave, Eve) sit in circle. Constraints:
Alice not next to Bob, Carol must be next to Dave, Eve between Alice and
Carol, etc."

- **Phase 1: Constraint Mapping**
  - Categorize by type (adjacency, separation, position)
  - Identify hard vs. soft constraints
  - Detect potential conflicts early

- **Phase 2: Systematic Scenario Generation**
  - Start with most restrictive constraint
  - Generate candidate arrangements
  - Track decision tree branches

- **Phase 3: Constraint Validation**
  - Test each candidate against all 7 constraints
  - Eliminate violations with reasoning
  - Track which constraints caused elimination

- **Phase 4: Independent Verification**
  - Re-verify winning solution from scratch
  - Check edge cases (circular boundary conditions)
  - Confirm no constraint violations missed


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
The output demonstrates increasing reasoning transparency and accuracy:

**Standard vs. Basic CoT (Mathematical):**
- Standard: "Total time is approximately 8.3 hours" (no explanation)
- Basic CoT: Shows each leg calculation explicitly:
  "Leg 1: 120 miles ÷ 60 mph = 2 hours
   Leg 2: 180 miles ÷ 45 mph = 4 hours
   Leg 3: 90 miles ÷ 50 mph = 1.8 hours
   Break: 0.5 hours
   Total: 2 + 4 + 1.8 + 0.5 = 8.3 hours"

**Advanced CoT Benefits:**
- Validation phase catches errors: "Wait, let me verify leg 3 calculation..."
- Self-correction visible: "Initial calculation missed break time, correcting..."
- Reasonableness checks: "8.3 hours for ~400 miles seems reasonable given
  average speed of ~48 mph"

**Logical Puzzle Resolution:**
- Phase 1 output: Constraint taxonomy showing 3 adjacency rules, 2 separation
  rules, 2 position rules
- Phase 2 output: Decision tree showing 8 initial candidates, progressively
  eliminated to 2 viable options
- Phase 3 output: Detailed validation showing Candidate A violates constraint
  #5, Candidate B satisfies all constraints
- Phase 4 output: Independent verification confirms Candidate B is unique
  solution


4. WHY THIS MATTERS
-----------------------------------------------------------------
Chain of Thought is critical for complex reasoning tasks requiring
transparency, accuracy, and trust:

**Auditability & Debugging:**
- Exposes reasoning process for human review
- Reveals where errors occur in multi-step logic
- Enables targeted corrections (fix specific reasoning step, not entire process)
- Critical for compliance and regulation (explain AI decisions)

**Accuracy Improvements:**
- Significantly reduces errors on math, logic, planning tasks
- Self-correction through validation phases
- Catches calculation mistakes before final answer
- Research shows 10-30% accuracy improvement on complex problems

**Trust & Transparency:**
- Builds confidence in AI decisions through visible reasoning
- Users can verify logic independently
- Detects flawed reasoning even when answer looks plausible
- Essential for high-stakes applications (medical, legal, financial)

**Practical Applications:**

*Financial Analysis:*
- Show calculation steps for investment returns
- Expose assumptions in valuation models
- Enable auditor review of automated decisions

*Medical Diagnosis:*
- Document symptom analysis and differential diagnosis
- Show reasoning for treatment recommendations
- Support second opinions and peer review

*Legal Research:*
- Trace argument construction from precedents
- Show application of legal principles step-by-step
- Document reasoning for case strategy decisions

*Engineering Design:*
- Expose calculation steps in structural analysis
- Show trade-off evaluation process
- Enable verification by senior engineers

**When to Use CoT:**
- Multi-step mathematical or logical problems
- Decisions requiring justification or explanation
- Tasks where intermediate steps matter (not just final answer)
- High-stakes scenarios where errors are costly
- Situations requiring human oversight and verification
- Complex reasoning where errors are likely without structure

**Performance Considerations:**
- Increases token usage (reasoning steps add length)
- Slower response times (more generation required)
- Higher API costs (typically 2-3x standard prompts)
- Worth the cost for accuracy-critical applications

**Best Practices:**
- Use "Let's solve this step by step" trigger phrase
- Add validation phases for self-correction
- Request explicit calculation units and intermediate values
- Ask for reasonableness checks on final answers
- Combine with self-consistency for maximum reliability
