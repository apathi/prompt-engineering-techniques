=================================================================
TECHNIQUE 09: ROLE PROMPTING
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
Role prompting teaches how assigning specific professional personas (financial
advisor, tech architect, medical researcher) guides AI responses with
domain-appropriate expertise, terminology, and communication styles. The model
adopts the perspective, knowledge base, and analytical frameworks of the
assigned role.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
**Professional Role Profiles:**
- Predefined roles with expertise domains, communication styles, requirements
- Examples: Financial advisor (investment analysis, risk assessment),
  Technical architect (system design, scalability), Medical researcher
  (evidence-based analysis, clinical terminology)
- Each role has specific context requirements and analytical frameworks

**Single-Role Analysis:**
- Business scenario analyzed from one professional perspective
- Example: E-commerce strategy evaluated by financial advisor (margin focus),
  tech architect (infrastructure concerns), marketing strategist (acquisition)
- Shows how role shapes recommendations and priorities

**Multi-Role Consultation:**
- Same problem analyzed by 3+ expert roles simultaneously
- Healthcare startup decision evaluated by: Technical expert (feasibility),
  Financial analyst (ROI modeling), Medical professional (compliance)
- Synthesis combines insights from all perspectives into unified recommendation

**Implementation:**
- Uses RoleProfileManager with predefined templates
- Each role has expertise_domains, communication_style, decision_framework
- Prompts structured: "As a [role] with expertise in [domains], analyze..."


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
**Distinct Professional Perspectives:**
- Financial advisor: "Focus on margin optimization, customer lifetime value,
  and cash flow management. Recommendation: Reduce operational costs by 15%"
- Tech architect: "Infrastructure scalability concerns with current
  architecture. Recommendation: Migrate to microservices for 3x capacity"
- Marketing strategist: "Customer retention priority over acquisition.
  Recommendation: Implement loyalty program targeting 80/20 rule"

**Multi-Expert Synthesis:**
Healthcare startup analysis combines:
- Technical: Platform feasibility assessment, development timeline estimates
- Financial: Burn rate analysis, funding runway projections, ROI scenarios
- Medical: Regulatory compliance roadmap, clinical validation requirements
- Result: Unified recommendation balancing all expert viewpoints


4. WHY THIS MATTERS
-----------------------------------------------------------------
**Domain Expertise on Demand:**
- Access specialized knowledge without hiring domain experts
- Consistent professional-level analysis across business functions
- Terminology and frameworks match stakeholder expectations

**Practical Applications:**

*Strategic Decision-Making:*
- Board presentations require financial, technical, market perspectives
- Multi-role analysis ensures comprehensive risk assessment
- Reduces blind spots from single-discipline thinking

*Stakeholder Communication:*
- Technical documentation for engineers vs. executives requires different depth
- Sales pitches vary by buyer role (CFO vs. CTO vs. CMO)
- Support responses adapt to user expertise level

*Content Generation:*
- Marketing copy written by brand strategist persona
- Technical documentation from experienced engineer perspective
- Legal disclaimers reviewed through legal counsel lens

**When to Use:**
- Decisions requiring specialized domain knowledge
- Stakeholder communication needing appropriate expertise level
- Multiple perspective analysis reveals complementary insights
- Professional tone and terminology critical for credibility
