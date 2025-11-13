=================================================================
TECHNIQUE 07: SELF-CONSISTENCY PROMPTING
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Self-consistency leverages the principle that correct reasoning tends to
converge while errors diverge. By generating multiple independent reasoning
paths (with higher temperature for diversity) and using voting mechanisms
to select the most consistent answer, reliability improves significantly
compared to single-path reasoning. This technique is the "wisdom of crowds"
applied to AI reasoning.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
Two sophisticated examples demonstrate consensus-based decision making:

**Multiple Reasoning Paths (Mathematical Problem):**
A percentage increase/decrease problem solved three times using different
approaches to test convergence:

Problem: "Price increased by 20%, then decreased by 20%. Final price $96.
What was original price?"

- **Path 1: Work Backwards from Final Amount**
  - Start with $96 as 80% of pre-decrease price
  - Calculate: $96 ÷ 0.8 = $120 (before 20% decrease)
  - Then: $120 ÷ 1.2 = $100 (original price)
  - Reasoning: Reverse operations in opposite order

- **Path 2: Algebraic Equation Setup**
  - Let x = original price
  - After 20% increase: x × 1.2
  - After 20% decrease: (x × 1.2) × 0.8 = 0.96x
  - Solve: 0.96x = $96, therefore x = $100
  - Reasoning: Symbolic mathematical approach

- **Path 3: Step-by-Step Percentage Calculations**
  - Assume original = $100 (verify if this works)
  - After +20%: $100 × 1.2 = $120
  - After -20%: $120 × 0.8 = $96 ✓
  - Reasoning: Forward verification of hypothesis

**Voting Mechanism:**
- Semantic similarity voting compares answers
- Confidence scores: 33.3% each if all agree (unanimous)
- If paths disagree, identifies majority answer with higher confidence
- Disagreement signals potential problem requiring investigation

**Complex Decision Making (Strategic Analysis):**
A startup funding decision analyzed from three perspectives:

Problem: "Should we accept $2M seed funding at $10M valuation, diluting
20% equity?"

- **Perspective 1: Risk Management Analysis**
  - Evaluates failure probability scenarios
  - Analyzes downside protection and mitigation strategies
  - Considers runway extension vs. equity cost
  - Recommendation: Accept (extends survival, reduces failure risk)

- **Perspective 2: Financial Optimization**
  - Calculates expected value and ROI projections
  - Models cash flow scenarios with/without funding
  - Evaluates opportunity cost of delayed growth
  - Recommendation: Accept (positive expected value, accelerates growth)

- **Perspective 3: Strategic Positioning**
  - Assesses competitive advantage timing
  - Analyzes market window and first-mover benefits
  - Evaluates investor value-add beyond capital
  - Recommendation: Accept (market timing critical, strategic partners valuable)

**Democratic Voting:**
- Three independent analyses reach same conclusion
- Consensus builds confidence in recommendation
- Synthesis combines insights from all perspectives
- Output: "Strong consensus (3/3) → Accept funding"


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
Results across 6 API calls ($0.0016) demonstrate consensus validation:

**Mathematical Problem Convergence:**
- Path 1 result: "$100" (backwards calculation)
- Path 2 result: "$100" (algebraic solution)
- Path 3 result: "$100" (forward verification)
- Voting analysis: 100% agreement, high confidence
- Demonstrates three completely different approaches reaching same answer

**When Paths Diverge (Error Detection):**
- If Path 1 calculated "$105" due to calculation error
- Voting would show: 66.7% confidence for "$100", 33.3% for "$105"
- Lower confidence signals problem needing review
- Human can investigate the outlier path to find error

**Strategic Decision Synthesis:**
- Risk perspective: Accept (runway extension outweighs dilution)
- Finance perspective: Accept (ROI projections positive)
- Strategy perspective: Accept (timing and partnerships critical)
- Final recommendation: "Strong consensus (3/3) supports accepting funding"
- Synthesis combines rationale from all three frameworks

**Confidence Metrics:**
- Unanimous agreement = High confidence (safe to proceed)
- 2/3 agreement = Medium confidence (review dissenting view)
- 1/3 agreement = Low confidence (significant disagreement, needs analysis)


4. WHY THIS MATTERS
-----------------------------------------------------------------
Self-consistency is valuable for ambiguous or high-stakes decisions where
single-path reasoning might be unreliable:

**Error Detection & Reliability:**
- Catches calculation mistakes (disagreement signals error)
- Reduces hallucination impact (false answers less likely to converge)
- Provides confidence metrics (unanimous agreement = higher trust)
- Identifies when AI is "guessing" (low consistency = uncertainty)

**Multi-Perspective Analysis:**
- Balances competing valid viewpoints (finance vs. risk vs. strategy)
- Prevents single-framework bias (e.g., overemphasizing financial returns)
- Synthesizes insights no single analysis would capture
- Mimics expert panel deliberation

**When to Use Self-Consistency:**

*High-Stakes Decisions:*
- Medical diagnoses (multiple reasoning paths reduce misdiagnosis)
- Legal strategy (diverse analytical frameworks ensure comprehensive review)
- Financial investments (balance risk, return, and strategic considerations)
- Safety-critical engineering (redundant validation catches errors)

*Ambiguous or Subjective Problems:*
- Product design decisions (user experience, technical feasibility, business value)
- Content moderation (different cultural or contextual interpretations)
- Hiring decisions (skills assessment, culture fit, growth potential)
- Strategic planning (short-term vs. long-term trade-offs)

*Mathematical or Logical Problems:*
- Complex calculations where errors are likely
- Multi-step reasoning prone to compounding mistakes
- Problems with multiple valid solution approaches
- Verification of automated analysis results

**Implementation Considerations:**

*Temperature Settings:*
- Higher temperature (0.7-0.9) for diverse reasoning paths
- Lower temperature would produce similar answers (less useful)
- Balance: Diverse enough to catch errors, consistent enough to converge

*Number of Paths:*
- 3-5 paths typically sufficient
- More paths = higher cost, diminishing returns
- Minimum 3 for meaningful voting (detect outliers)

*Voting Mechanisms:*
- Exact match: Simple but strict (text must match exactly)
- Semantic similarity: More robust (recognizes equivalent answers)
- Democratic: Each path votes equally
- Weighted: Expert paths or higher-confidence paths weighted more

**Cost-Benefit Analysis:**
- Increases API costs 3-5x (multiple completions per query)
- Significantly improves reliability on critical decisions
- Worth investment for high-stakes, irreversible, or costly-to-correct decisions
- Not necessary for low-stakes or easily reversible choices

**Comparison to Other Techniques:**
- More reliable than single Chain of Thought (catches CoT errors)
- More expensive than standard prompting (multiple API calls)
- Provides confidence metrics unlike deterministic approaches
- Ideal for production systems requiring reliability guarantees
