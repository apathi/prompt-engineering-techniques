=================================================================
TECHNIQUE 03: PROMPT TEMPLATES AND VARIABLES
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
This lesson teaches dynamic prompt construction through variable substitution
and template reusability. The core concept: templates with placeholders
({variable}) enable scaling prompt engineering across multiple contexts
without rewriting logic. It demonstrates progression from simple single-
variable templates to complex multi-variable scenarios with conditional
logic, list processing, and compositional patterns.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
The implementation uses LangChain's PromptTemplate.from_template() with
curly-brace variable syntax for dynamic content injection.

**Simple Templates (Single Variable):**
Basic templates contain one placeholder:
- "Explain {topic} in simple terms"
- Variables are injected at runtime: {topic: "photosynthesis"}
- Enables reusable explanation templates across any subject

**Complex Templates (Multiple Variables):**
Multi-variable templates combine context, audience, and constraints:
- "Explain {concept} in {field} to a {audience} audience using {style}"
- Example injection: {concept: "neural networks", field: "AI",
  audience: "beginners", style: "analogies"}
- Single template generates content for any domain/audience combination

**Conditional Templates:**
Dynamic template selection based on runtime conditions:
- Function checks user profile (has_profession: bool)
- Selects employment-specific vs. general template
- Injects profession-relevant examples when available
- Demonstrates branching logic in template systems

**List Processing Templates:**
Handles variable-length data structures:
- Accepts lists of items: ["apple", "banana", "hammer", "Moby Dick"]
- Formats as bullet points or comma-separated strings
- Template categorizes items by type and provides analysis
- Shows how templates handle dynamic data quantities

**Template Composition:**
Combines multiple template components:
- Header template: Project metadata (name, budget, timeline)
- Body template: Progress and deliverables breakdown
- Footer template: Risk summary and next steps
- Unified composition creates structured executive summaries
- Demonstrates modular template architecture for complex documents


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
The output demonstrates template flexibility across diverse scenarios.
Simple templates generate focused explanations (photosynthesis: "process
where plants convert sunlight into energy through chlorophyll"). Multi-
variable templates produce audience-tailored content—neural networks
explained to beginners uses everyday analogies, while the same template
with {audience: "engineers"} would include technical architecture details.

Conditional templates show personalization in action. Users with professions
receive career advice incorporating their field ("As a software engineer,
consider cloud architecture certifications"), while general users get
broader guidance. The template logic adapts output structure based on
input data.

List processing categorizes mixed items into logical groups: fruits (apple,
banana), tools (hammer, screwdriver), literature (Moby Dick, 1984). The
template recognizes patterns and provides contextual analysis beyond simple
enumeration.

Template composition produces structured executive summaries from project
data. The header/body/footer combination creates professional reports with
consistent formatting, showing how complex documents can be generated from
reusable components. Total cost: approximately $0.0017 for 10 requests.


4. WHY THIS MATTERS
-----------------------------------------------------------------
This technique is critical for production systems requiring dynamic content
generation at scale. Instead of hardcoding hundreds of specific prompts,
teams maintain a library of composable templates with variable injection.

**Production Applications:**
- Email Personalization: Single template generates thousands of personalized
  messages by injecting {customer_name}, {product}, {purchase_date}. Changes
  to email structure require updating one template, not thousands of records.

- Report Generation: Financial reports, status updates, and analytics
  summaries use template composition. Header (metadata) + body (data tables)
  + footer (recommendations) creates consistent document structure across
  departments.

- API Documentation: Developer documentation templates inject {endpoint},
  {method}, {parameters}, {response_format} to generate consistent API
  references from specification data. One template maintains documentation
  for hundreds of endpoints.

- User Onboarding: Conditional templates adapt onboarding flows based on
  user type {is_enterprise}, {has_technical_background}, {industry}. New
  users see relevant guidance without manual content creation.

**Maintenance & Iteration:**
Template-based approaches reduce maintenance burden exponentially. When
prompt engineering best practices evolve, updating the master template
propagates improvements across all use cases. A/B testing becomes trivial—
swap template versions without touching business logic. Non-technical
users can leverage AI through forms that populate template variables,
democratizing prompt engineering beyond the engineering team.

**Scalability Pattern:**
The pattern enables rapid iteration: Template library → Variable injection →
Quality testing → Production deployment. Organizations build template
repositories categorized by use case (customer support, content generation,
data analysis), allowing teams to leverage proven patterns rather than
starting from scratch. This architectural approach transforms prompt
engineering from ad-hoc scripting to systematic, maintainable infrastructure.
