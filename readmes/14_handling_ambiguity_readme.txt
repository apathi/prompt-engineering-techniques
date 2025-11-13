=================================================================
TECHNIQUE 14: HANDLING AMBIGUITY
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Handling ambiguity teaches systematic detection and resolution of unclear or
vague prompts through context injection and multi-step clarification frameworks.
The technique prevents misinterpretation by transforming ambiguous requests
into specific, actionable requirements.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
**Ambiguity Detection:**
- `_detect_ambiguity()` function identifies vague terms using keyword dictionaries
- Flags: "it", "some", "better", "good", "stuff", "thing", "improve", "optimize"
- Clarity scoring measures specificity of requests
- Automated detection triggers clarification workflows

**Context-Based Disambiguation:**
Same ambiguous prompt tested with different contexts to show interpretation
variations:

Prompt: "Tell me about the bank"
- Context: Financial → Banking institutions, services, accounts
- Context: Geographic → River banks, erosion, ecosystems
- Context: Data → Data banks, storage systems, databases

Demonstrates how context shapes interpretation of ambiguous terms.

**Multi-Step Clarification Pipeline:**
Transforms vague requests into detailed specifications:

Stage 1: Identify ambiguous elements ("Make it better and add some good stuff")
- Flags: "better" (subjective), "good stuff" (undefined), "it" (unclear referent)

Stage 2: Request clarifications
- What does "better" mean? (Performance? UX? Features?)
- What is "good stuff"? (Features? Content? Functionality?)
- What is "it"? (Website? App? Product?)

Stage 3: Generate structured requirements
- Specific goals with measurable criteria
- Timeline and resource estimates
- Success metrics and validation checkpoints


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
**Context-Driven Interpretation:**
"Bank" with financial context → Discusses checking accounts, loans, investments
"Bank" with geographic context → Explains riverbanks, erosion, wildlife habitats
"Bank" with data context → Describes database storage, data repositories

**Clarification Transformation:**
Vague: "Make it better and add some good stuff"
Clarified: "Improve website load time from 5s to 2s (performance), add user
dashboard with analytics (feature), implement dark mode (UX). Timeline: 6 weeks.
Success metrics: <2s page load, 80% user satisfaction, 50% dark mode adoption."

**Clarity Scoring:**
- Original vague prompt: 2/10 clarity score (highly ambiguous)
- After clarification: 9/10 clarity score (specific and actionable)


4. WHY THIS MATTERS
-----------------------------------------------------------------
**Prevents Costly Misinterpretation:**
- Ambiguous requirements lead to wrong implementations
- Clarification upfront saves rework and wasted resources
- Critical for customer-facing AI where misunderstanding damages trust

**Production Applications:**

*Customer Service Chatbots:*
- User: "I need help with my account"
- Bot detects ambiguity, asks: "Which account? (Email, billing, user profile?)"
- Prevents incorrect responses and customer frustration

*Project Management AI:*
- Stakeholder: "Improve the dashboard"
- System clarifies: "Which metrics? Which users? What improvements?"
- Generates specific requirements with acceptance criteria

*Voice Assistants:*
- User: "Book a table"
- Assistant disambiguates: "Restaurant reservation or database table setup?"
- Context (time, location, recent activity) guides interpretation

**When to Use:**
- User inputs naturally vague or underspecified
- Domain has multiple valid interpretations for same term
- Misinterpretation costs high (production systems, customer service)
- Context available to guide disambiguation
- Multi-step workflows benefit from upfront clarification

**Implementation Strategies:**
- Context injection: Prepend relevant domain context to prompts
- Clarification questions: Ask users to specify before proceeding
- Default interpretations: Use most common meaning with confidence scores
- Disambiguation templates: Predefined clarification workflows by domain
