from string import Template

SUMMARIZER_PROMPT = Template("""
You are summarizing a mathematical reasoning history for a finite field geometry problem.

Your job:
- Extract ONLY the essential mathematical state.
- Keep all derived formulas, bounds, constraints, and computed values.
- Remove step-by-step plans, JSON structure, and irrelevant narration.
- Produce a SHORT, COMPACT summary that captures the CURRENT STATE needed for further computation.

Output format (plain text, no JSON):
- Key derived quantities
- Current bounds or constraints
- Current working formulas
- Any partially computed invariants
- The current goal (if clear)

Here is the full history to summarize:
$history

Now provide the compressed summary, no longer than 10–15 lines:
""")
