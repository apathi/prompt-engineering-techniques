=================================================================
TECHNIQUE 08: CONSTRAINED GENERATION
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Constrained generation demonstrates how to enforce specific formats, rules,
and structural requirements on AI outputs, making them reliably processable
by downstream systems. The technique covers format validation (JSON, bullet
lists), content constraints (length, keywords, forbidden words), and multi-
layered constraint satisfaction—essential for production systems requiring
predictable, parseable outputs.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
Two comprehensive examples with programmatic validation:

**Structured Format Generation:**
Product recommendation task with two distinct format requirements:

- **JSON Format with Validation:**
  - Task: "Recommend noise-canceling headphones under $200"
  - Required fields: product_name, price, features (array), pros (array),
    cons (array), rating (1-10)
  - ConstraintValidator utility checks:
    * All 6 fields present
    * Correct data types (price = number, features = array)
    * Valid JSON syntax (parseable by downstream systems)
  - Validation result: Pass/Fail with specific violations listed

- **Bullet List Format with Headings:**
  - Same product recommendation task
  - Required structure: Clear section headings (Product, Price, Features,
    Pros, Cons, Rating)
  - Format compliance checking:
    * Each section starts with heading
    * Items properly bulleted (-, *, or •)
    * No paragraph text mixing with bullets
  - Human-readable but still validated

**Multi-Constraint Compliance (Layered Rules):**
Client complaint email response with complex constraint combinations:

- **Constraint Set 1: Format + Length + Keywords**
  - Format: Professional email structure (greeting, body, closing)
  - Length: ≤300 characters (concise response requirement)
  - Required keywords: "apologize", "solution", "compensation"
  - Validation checks all three dimensions simultaneously

- **Constraint Set 2: Format + Content + Tone**
  - Format: Email structure maintained
  - Content constraints:
    * Required words: "acknowledge", "timeline", "follow-up"
    * Forbidden words: "excuse", "blame", "unfortunately"
    * Maximum 8 sentences
  - Tone analysis: Professional, empathetic, solution-focused
  - Validation uses ConstraintValidator to programmatically verify:
    * Keyword presence detection (regex matching)
    * Forbidden word absence checking
    * Sentence count validation
    * Email structure verification (greeting + body + signature)

**ConstraintValidator Utility:**
Specialized validation engine used across examples:
- Checks format compliance (JSON schema, bullet structure)
- Verifies content rules (keyword presence, length limits)
- Detects violations (forbidden words, missing fields)
- Returns detailed validation reports (pass/fail + specific issues)


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
Results from 4 API calls ($0.0005) show successful constraint satisfaction:

**JSON Generation Example:**
```
{
  "product_name": "Sony WH-1000XM4",
  "price": 179.99,
  "features": ["Active noise canceling", "30-hour battery", "Bluetooth 5.0"],
  "pros": ["Excellent sound quality", "Comfortable for long wear"],
  "cons": ["Bulky carrying case", "No water resistance"],
  "rating": 9
}
```
- Validation: ✓ All fields present, correct types, valid JSON
- Parseable by downstream systems (e.g., database insertion, API responses)

**Bullet List Format Example:**
```
Product: Sony WH-1000XM4
Price: $179.99
Features:
  • Active noise-canceling technology
  • 30-hour battery life
  • Touch controls
Pros:
  • Superior sound quality
  • Comfortable over-ear design
Cons:
  • Plastic build feels less premium
  • Limited color options
Rating: 9/10
```
- Validation: ✓ Clear headings, proper bullet formatting, structured layout

**Email Response (300 Character Constraint):**
"Dear Customer, We sincerely apologize for the inconvenience. We're working
on a solution and will provide compensation. Thank you for your patience.
Best regards, Support Team"
- Length: 187 characters ✓
- Contains: "apologize" ✓, "solution" ✓, "compensation" ✓
- Format: Professional email structure ✓

**Email Response (Tone + Content Constraints):**
"Thank you for bringing this to our attention. We acknowledge the issue and
apologize for any frustration caused. Our team will investigate immediately
and provide a resolution timeline within 24 hours. We'll follow up with you
personally to ensure satisfaction."
- Required words: "acknowledge" ✓, "timeline" ✓, "follow-up" ✓
- Forbidden words: None detected ✓
- Sentences: 4 (within 8-sentence limit) ✓
- Tone: Professional, empathetic, action-oriented ✓


4. WHY THIS MATTERS
-----------------------------------------------------------------
Constrained generation is essential for production systems where AI outputs
must integrate with existing infrastructure and business processes:

**System Integration & Automation:**
- JSON outputs enable direct database insertion (no manual parsing)
- Structured formats work with APIs, webhooks, automation tools
- Predictable outputs reduce integration failures and error handling
- Enables end-to-end automation (AI → validation → downstream systems)

**Business Rule Compliance:**
- Enforce brand voice guidelines (required/forbidden terminology)
- Maintain legal compliance (required disclosures, prohibited claims)
- Ensure policy adherence (customer communication standards)
- Reduce human review burden (automated validation catches violations)

**Quality Assurance & Testing:**
- Programmatic validation enables automated testing
- Constraint violations caught before production
- Reduces manual QA time and costs
- Provides measurable quality metrics (constraint compliance percentage)

**Practical Applications:**

*API Responses (JSON Constraints):*
- Mobile apps require specific JSON schemas
- Backend services expect consistent field names and types
- API versioning maintained through schema validation
- Example: E-commerce product feeds, booking confirmations, user profiles

*Customer Communications (Tone + Content):*
- Email templates must include regulatory disclosures
- Support responses avoid liability-creating language
- Marketing messages adhere to brand voice guidelines
- Example: Complaint responses, order confirmations, policy notifications

*Content Moderation (Forbidden Words):*
- Filter offensive or inappropriate language
- Block competitor mentions in support responses
- Prevent disclosure of confidential information
- Example: Forum posts, chat responses, user-generated content

*Report Generation (Format + Length):*
- Executive summaries limited to one page
- Financial reports require specific section structure
- Compliance documents need standard formatting
- Example: Board reports, regulatory filings, audit documentation

*Data Extraction (Structured Output):*
- Extract invoice data into standardized JSON
- Parse resumes into consistent field structure
- Convert unstructured text to database records
- Example: Document processing, data entry automation, ETL pipelines

**Implementation Strategies:**

*Prompt Engineering:*
- Explicit format instructions in system prompt
- Example templates showing desired structure
- Clear constraint lists (required/forbidden elements)
- Request validation self-check before final output

*Validation Layers:*
- Format validation (JSON schema, structure checks)
- Content validation (keyword presence, length limits)
- Semantic validation (tone analysis, coherence checks)
- Business rule validation (company-specific requirements)

*Error Handling:*
- Retry logic with clarified constraints (if validation fails)
- Fallback templates (graceful degradation)
- Human review queue (for repeated violations)
- Logging and monitoring (track constraint violation patterns)

**Cost-Benefit Considerations:**
- Reduces post-processing overhead (no manual reformatting)
- Minimizes integration bugs (predictable output structure)
- Enables automation (reliable inputs for downstream systems)
- Small upfront investment (constraint definition) pays ongoing dividends

**When to Use Constrained Generation:**
- Outputs feed into automated systems (APIs, databases, workflows)
- Business rules or regulations govern content
- Consistency critical across many outputs (brand voice, legal compliance)
- Post-processing expensive or error-prone
- Integration failures costly (production systems, customer-facing apps)

**Advanced Patterns:**
- Combine with Few-Shot Learning (show constraint-compliant examples)
- Layer with Chain of Thought (explain why constraints matter)
- Add Self-Consistency (multiple attempts, validate each, pick best)
- Implement retry loops (regenerate if validation fails, up to N attempts)
