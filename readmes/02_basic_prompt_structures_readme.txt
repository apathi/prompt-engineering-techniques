=================================================================
TECHNIQUE 02: BASIC PROMPT STRUCTURES
=================================================================

1. WHAT IS THIS LESSON?
-----------------------------------------------------------------
This lesson distinguishes between single-turn (isolated) and multi-turn
(conversational) prompt architectures, revealing how context preservation
fundamentally changes AI behavior. It demonstrates that multi-turn prompts
enable reference resolution and maintain conversational coherence across
exchanges. The core insight: memory strategies—full history, sliding window,
or stateless—determine how AI interprets follow-up questions.


2. HOW THE CODE WORKS
-----------------------------------------------------------------
The implementation uses modern LangChain patterns, replacing deprecated
ConversationChain with RunnableWithMessageHistory and MessagesPlaceholder
for proper memory management.

**Single-Turn vs Multi-Turn Architecture:**
Single-turn examples demonstrate five categories:
- Factual: Direct knowledge retrieval without context
- Creative: Story/poem generation in isolation
- Analytical: Problem-solving without prior conversation
- Instructional: Task execution as standalone requests
- Conversational: Questions that naturally require context

Multi-turn examples use the same prompts but maintain conversation history,
showing how "What is its population?" becomes answerable when preceded by
"Tell me about Paris."

**Memory Strategy Comparison:**
Three approaches are tested through a cooking conversation:
- Full Buffer: Maintains complete conversation history (all 7 turns)
- Sliding Window: Keeps only recent k messages (k=3 for middle context)
- No Memory: Treats each message as isolated (stateless)

The code uses ChatMessageHistory to maintain separate message stores for
each strategy, demonstrating how context window size affects coherence.
Each conversation progresses through recipe request, ingredient questions,
substitutions, and technique clarifications—scenarios that require memory
of prior exchanges.


3. WHAT YOU SEE IN THE OUTPUT
-----------------------------------------------------------------
The output dramatically illustrates context dependency through direct
comparison. Single-turn responses to "What is its population?" return
confused clarification requests ("I'd be happy to help, but could you
specify which location you're asking about?"), while multi-turn correctly
returns Paris's 2.1 million population by referencing the previous message.

The memory strategy comparison shows diverging conversation quality:
- Full Memory: Perfect coherence across all 7 turns, with the AI correctly
  referencing "the recipe I mentioned" and "the butter substitution we
  discussed earlier"
- Sliding Window (k=3): Maintains recent context but loses early details.
  When asked about the original recipe after 5 turns, the AI can't recall
  specific ingredients from turn 1
- No Memory: Becomes repetitive and disconnected. Each response treats the
  question as brand new, asking "What recipe would you like?" multiple
  times despite ongoing conversation

Cost tracking shows 39 total requests at approximately $0.0095, with
full-memory conversations using more tokens per request due to accumulated
history.


4. WHY THIS MATTERS
-----------------------------------------------------------------
This technique is essential for building conversational AI applications
like chatbots, virtual assistants, and interactive help systems. Understanding
memory strategies directly impacts both user experience quality and API cost
management.

**Production Implications:**
- Customer Service: Full memory enables agents to reference previous issues
  without forcing customers to repeat information. "Regarding the order you
  mentioned" becomes possible.
- Educational Tutoring: Sliding window memory maintains recent teaching
  context while preventing token overflow in long study sessions.
- Interactive Troubleshooting: Multi-step debugging requires memory of
  previous diagnostic steps to avoid circular questioning.

**Cost vs. Quality Trade-offs:**
Full-memory conversations can become expensive as token counts grow
exponentially with conversation length. A 10-turn conversation with full
history might use 5,000+ tokens, while sliding window (k=3) uses only
1,500 tokens with acceptable coherence loss. For production systems,
sliding window memory (k=3 to k=5) typically balances coherence with
token efficiency.

**When to Use Each Strategy:**
- Full Memory: Short conversations, high-stakes interactions (legal advice,
  medical consultation) where perfect context is critical
- Sliding Window: Long conversations, cost-sensitive applications (customer
  support chat) where recent context matters most
- No Memory: FAQ systems, simple queries, scenarios where each question is
  truly independent

The pattern enables production features like customer service dialogues,
multi-step troubleshooting workflows, and educational tutoring systems
where conversational flow determines success or failure of the AI application.
