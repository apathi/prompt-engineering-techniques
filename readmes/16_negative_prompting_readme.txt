=================================================================
TECHNIQUE 16: NEGATIVE PROMPTING
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Negative prompting guides AI outputs by explicitly specifying what to exclude
through multi-layer constraint validation. The technique demonstrates how to
create boundaries that prevent undesired content while maintaining helpful,
informative responses.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
**ConstraintValidator Utility:**
Pattern-based violation detection with severity scoring:
- Forbidden words: Regex matching with case-insensitive detection
- Forbidden phrases: Multi-word pattern recognition
- Style constraints: Tone and formality violations
- Content constraints: Topic boundaries and scope limits
- Severity levels: Low (0.1), Medium (0.3), High (0.6) penalty weights

**Basic Negative Constraints (Example 1):**
Three topics with explicit exclusion rules:

AI Topic:
- No technical jargon or complex terminology
- No historical background or dates
- No comparisons to other technologies
- Keep under 150 words
- Focus only on current practical applications

Climate Change Topic:
- No political opinions or blame assignment
- No catastrophic language or fear-mongering
- No specific country examples
- Keep scientific and objective
- Focus on actionable solutions

Cryptocurrency Topic:
- No investment advice or financial recommendations
- No price predictions or market speculation
- No promotion of specific coins or platforms
- Explain concepts only, not opportunities
- Keep neutral and educational

**Advanced Multi-Dimensional Constraints (Example 2):**
Layered constraint categories with granular validation:

Business Email (Declining Proposal):
- Tone: No rudeness, dismissiveness, unprofessionalism, casual language
- Content: No detailed rejection reasons, competitor mentions
- Structure: ≤100 words, no attachments/links
- Legal: No binding commitments, discriminatory language

Medical Information (Allergy Summary):
- Medical: No specific advice, medication suggestions
- Liability: No replacement for professional consultation, definitive diagnoses
- Content: No rare complications, medical jargon
- Scope: Only seasonal allergies, no food allergies

Each category independently validated with compliance scoring.


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
**Constraint Compliance (5 Requests, $0.0007):**

AI Explanation (150 words, constraints satisfied):
- No technical terms ("neural networks", "algorithms" avoided)
- No historical context (no mention of AI history or pioneers)
- No comparisons (doesn't reference competing technologies)
- Practical focus: Virtual assistants, recommendation systems, healthcare

Climate Change Explanation (actionable solutions):
- Avoids political blame ("governments failed" not mentioned)
- No catastrophic language ("doom", "disaster" avoided)
- No country specifics (general global approach)
- Scientific objectivity maintained
- Solutions: Energy efficiency, renewable transition, reforestation

Business Email (87 words):
"Thank you for your proposal. After careful consideration, we've decided not
to move forward at this time. We appreciate your effort and hope to keep
communication open for future opportunities. Best regards."
- Professional tone maintained
- No specific rejection reasons given
- No competitor mentions
- Under 100-word limit

**Compliance Scoring:**
- Violation detection: 0 violations across all examples
- Compliance score: 1.0 (100% adherence to constraints)
- Category-specific validation: All dimensions passed


4. WHY THIS MATTERS
-----------------------------------------------------------------
**Content Moderation & Brand Safety:**
- Prevents offensive, inappropriate, or harmful content
- Maintains brand voice by excluding specific language
- Critical for customer-facing applications

**Legal & Compliance:**
- Healthcare: Avoid medical advice, liability, unauthorized diagnoses
- Finance: Prevent investment advice, price predictions, guarantees
- Legal: No legal advice, binding commitments, regulated claims
- Reduces organizational risk and regulatory violations

**Practical Applications:**

*Customer Communications:*
- Support emails exclude blame, excuses, competitor mentions
- Product descriptions avoid unsubstantiated claims, superlatives
- Marketing content prevents prohibited comparisons, guarantees

*Educational Content:*
- Medical information avoids specific advice, medication recommendations
- Financial education excludes investment tips, price targets
- Legal content prevents unauthorized legal advice

*Content Generation at Scale:*
- Blog posts avoid competitor mentions, controversial topics
- Product reviews exclude profanity, personal attacks
- Forum moderation filters offensive language, spam patterns

*Multi-Market Localization:*
- Cultural sensitivity by excluding inappropriate references
- Regional compliance by avoiding restricted topics
- Age-appropriate content by filtering mature themes

**Implementation Strategies:**

*Constraint Definition:*
- Explicit word/phrase blacklists with regex patterns
- Category-based organization (tone, content, legal, scope)
- Severity weighting for prioritized enforcement

*Validation Layers:*
- Pre-generation: Constraints embedded in system prompt
- Post-generation: Automated validation before delivery
- Iterative refinement: Regenerate if violations detected (max 3 attempts)

*Monitoring & Improvement:*
- Track violation patterns to refine constraint lists
- A/B test constraint phrasing for better compliance
- User feedback loop identifies missed violation types

**When to Use:**
- Regulated industries (healthcare, finance, legal, pharma)
- Brand-sensitive content requiring voice consistency
- Multi-audience platforms needing age/region appropriateness
- High-risk applications where violations cause legal/reputation damage
- Content moderation systems requiring automated filtering
