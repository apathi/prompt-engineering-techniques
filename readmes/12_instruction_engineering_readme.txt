=================================================================
TECHNIQUE 12: INSTRUCTION ENGINEERING
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Instruction engineering teaches how to craft clear, precise instructions with
specific constraints to eliminate ambiguity and ensure consistent outputs.
The technique demonstrates systematic refinement from vague instructions to
multi-constraint specifications with measurable quality scoring.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
**Instruction Quality Scoring (8-Point Scale):**
Evaluates instruction completeness across dimensions:
1. Has specific task description (not vague "write something")
2. Includes length constraint (word count, character limit)
3. Defines structure requirements (sections, format, headers)
4. Specifies target audience (executives, customers, technical users)
5. Sets tone/style guidelines (professional, casual, technical)
6. Provides context/background (why this task matters)
7. Includes constraints (what to include/exclude)
8. Defines success criteria (how to measure quality)

**Progressive Refinement Examples:**

*Poor Instruction (Score: 0/8):*
"Write something about planning"
- No length, structure, audience, tone, context, constraints, or criteria

*Refined Instruction (Score: 8/8):*
"Write a 300-word professional business memo for executives explaining
quarterly planning process. Structure: Introduction (purpose), 3 key phases
(research, goal-setting, execution), and conclusion. Use bullet points for
phases. Include specific timeline references. Avoid jargon. Success: Clear
understanding of planning cycle within 5 minutes."

**Multi-Constraint Validation:**
Customer feedback analysis task with 5 simultaneous constraints:
- Format: Valid JSON structure
- Content: 3 insights maximum, each under 50 words
- Field requirements: category, insight, priority (High/Medium/Low),
  confidence (percentage)
- Word count: Overall response under 150 words
- Quality: Actionable insights with specific recommendations

**Implementation:**
Uses InstructionOptimizer utility to programmatically validate compliance
across all constraint dimensions


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
**Quality Score Comparison:**
- Poor: "Write something about planning" → Score 0/8
  * Missing all 8 quality dimensions
  * Output unpredictable and likely irrelevant

- Refined: Detailed business memo instruction → Score 8/8
  * All dimensions specified
  * Output matches exact requirements: 300 words, 3 phases with bullets,
    executive-appropriate tone, 5-minute read time

**Multi-Constraint Success:**
Customer feedback analysis produced valid JSON:
```
{
  "insights": [
    {"category": "Product", "insight": "Users want mobile app",
     "priority": "High", "confidence": "85%"},
    {"category": "Support", "insight": "Response time too slow",
     "priority": "Medium", "confidence": "70%"},
    {"category": "Pricing", "insight": "Enterprise tier needed",
     "priority": "High", "confidence": "90%"}
  ]
}
```
- Validation: 5/5 constraints satisfied (JSON format ✓, 3 insights ✓,
  word limits ✓, required fields ✓, actionable content ✓)


4. WHY THIS MATTERS
-----------------------------------------------------------------
**Eliminates Trial-and-Error:**
- Clear instructions produce predictable outputs on first attempt
- Reduces iteration cycles from 5+ attempts to 1-2
- Saves API costs (fewer retries) and development time

**Measurable Quality Standards:**
- 8-point scoring provides objective instruction assessment
- Teams can benchmark instruction quality across projects
- Systematic refinement process (identify missing dimensions, add them)

**Production Reliability:**
- Multi-constraint validation ensures outputs integrate with systems
- Business rules enforced programmatically (format, length, content)
- Reduces manual review and post-processing overhead

**Practical Applications:**

*Report Generation:*
- Executive summaries: Length, structure, audience, tone all specified
- Financial reports: Format (JSON/PDF), sections, compliance requirements
- Status updates: Template with required fields, word limits, priorities

*Content Creation:*
- Marketing copy: Brand voice, character limits, call-to-action requirements
- Technical docs: Audience level, code example constraints, structure
- Customer communications: Tone guidelines, required disclosures, length

*Data Processing:*
- Extraction tasks: Output schema (JSON), field requirements, validation rules
- Analysis reports: Insight count, confidence thresholds, priority labels
- Summaries: Length constraints, key points required, format specification

*API Integrations:*
- Structured outputs (JSON schema) for database insertion
- Field validation (required fields, data types, value ranges)
- Format compliance for downstream system compatibility

**When to Use:**
- Output unpredictability causes production issues
- Multiple stakeholders need consistent quality
- Integration with automated systems requires reliability
- Manual post-processing expensive or error-prone
- Quality standards must be objective and measurable
