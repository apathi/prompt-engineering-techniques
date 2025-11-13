=================================================================
TECHNIQUE 05: FEW-SHOT LEARNING
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Few-shot learning demonstrates how providing 2-5 examples dramatically
improves AI performance on pattern-recognition tasks. This technique
covers example selection strategies, multi-task learning, in-context
learning for novel tasks, and adaptive learning with varying example
counts—enabling custom behavior without model retraining.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
Six progressively complex implementations showcase few-shot capabilities:

**Basic Classification (3 Examples):**
- Sentiment analysis with balanced examples: positive, negative, neutral
- Format: "Text: [example] → Sentiment: [label]"
- Demonstrates pattern learning from minimal data
- Tests edge case: "Not good, not bad, just average" (ambiguous input)

**Multi-Task Learning (5 Examples):**
- Single prompt handles both sentiment analysis AND language detection
- Examples show dual-label format: "Text → Sentiment | Language"
- Proves few-shot can learn multiple simultaneous tasks
- Input: "Hola, ¿cómo estás?" → Expected: Positive | Spanish

**Custom Task Learning (3 Examples):**
- Teaches novel task: Pig Latin conversion
- No prior model training on this specific transformation
- Examples: "hello → ellohay", "world → orldway", "python → ythonpay"
- Tests pure pattern inference from examples alone

**Example Selection Strategies (3 Variations):**
- Same task, different example sets test quality impact
- Balanced: Mix of easy/hard examples
- Extreme: Only very obvious cases
- Subtle: Nuanced, difficult-to-classify examples
- Reveals how example difficulty affects performance

**Few-Shot vs. Zero-Shot Comparison (Side-by-Side):**
- Product categorization task run both ways
- Input: "Wireless Bluetooth Headphones", "Green Tea Bags", "USB-C Cable"
- Zero-shot: Granular categories ("Smartphones", "Beverages/Tea")
- Few-shot: Consistent categories ("Electronics", "Food & Beverages")
- Shows improved terminology consistency

**Adaptive Learning (1, 2, 3, 6 Examples):**
- Tests performance scaling with example count
- Task: Product categorization
- Measures accuracy and consistency as examples increase
- Identifies diminishing returns point (often 3-5 examples)


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
Results across 33 API calls ($0.0004 cost) show consistent improvements
over zero-shot approaches:

**Classification Accuracy:**
- Edge case "Not good, not bad, just average" → Correctly labeled "Neutral"
- Ambiguous inputs handled more reliably than zero-shot
- Consistent label vocabulary (examples define valid categories)

**Multi-Task Success:**
- "Hola, ¿cómo estás?" → Positive | Spanish (both tasks correct)
- "Pretty good overall" → Positive | English (handles casual language)
- Dual-task learning doesn't sacrifice single-task accuracy

**Custom Task Performance:**
- Pig Latin conversion learned from 3 examples only
- Novel inputs correctly transformed: "programming" → "rogrammingpay"
- Demonstrates pure pattern inference without prior training

**Comparison Results:**
- Zero-shot: Inconsistent categories, very specific labels
  ("Smartphones", "Beverages / Tea", "Electronics Accessories")
- Few-shot: Consistent high-level categories
  ("Electronics", "Food & Beverages", "Electronics")
- Terminology standardization is key improvement


4. WHY THIS MATTERS
-----------------------------------------------------------------
Few-shot learning bridges the gap between zero-shot flexibility and
fine-tuning accuracy, offering significant advantages:

**Minimal Data Requirements:**
- 2-5 examples vs. thousands required for fine-tuning
- Rapid deployment without dataset collection overhead
- Cost-effective for specialized tasks with limited data availability

**Custom Task Support:**
- Enable domain-specific classifications (medical codes, legal categories)
- Teach novel formats (custom JSON schemas, proprietary notations)
- Adapt to organization-specific terminology and conventions

**Consistency Improvements:**
- Examples define valid output vocabulary (prevents hallucinated categories)
- Standardizes formatting (JSON structure, field names, date formats)
- Reduces post-processing variance (outputs match expected patterns)

**API Cost Optimization:**
- More concise than verbose zero-shot instructions
- Examples communicate requirements more efficiently than lengthy descriptions
- Smaller prompts = lower token costs at scale

**Practical Applications:**

*Content Moderation:*
- Train on company-specific policy examples
- Handle nuanced cases (sarcasm, context-dependent content)
- Adapt to evolving guidelines by updating examples

*Customer Support Classification:*
- Categorize tickets using your support taxonomy
- Learn from high-quality agent responses
- Maintain consistent routing and prioritization

*Data Extraction:*
- Extract fields from unstructured text (invoices, receipts, emails)
- Handle format variations through diverse examples
- Standardize outputs for database insertion

*Code Generation:*
- Show examples in your codebase style
- Enforce naming conventions and patterns
- Generate boilerplate matching team standards

**When to Use Few-Shot:**
- Task requires specific output format or terminology
- Zero-shot produces inconsistent results
- You have access to 2-10 quality examples
- Fine-tuning is too expensive or time-consuming
- Need rapid iteration on task definitions

**Optimal Example Count:**
- 3-5 examples typically sufficient for most tasks
- More examples improve accuracy but increase token costs
- Balance: Enough diversity to show pattern, not so many to waste tokens
