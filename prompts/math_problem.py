from string import Template

PROPOSE_PROMPT = Template("""
You are generating the next $k computational steps for solving a problem. 
Your output MUST be valid JSON. Begin with '{' and end with '}'.

Return ONLY:
{
  "complete": boolean,
  "final_answer": string,
  "steps": [
    { "plan": string, "equation": string },
    ...
  ]
}

RULES:
- If the final numerical answer is obtained → check your work and set complete=true, include it in final_answer, steps=[].
- Otherwise → complete=false, final_answer="", and provide EXACTLY $k steps.
- Steps MUST be concrete, computational, and make real mathematical progress.
- NO literature references, NO vague meta-actions, NO repeating past steps.
- If a value can be derived from given information, compute it directly.
- Steps must reflect NEW strategies relative to the history.

Input:
$input

History:
$history

Examples:

Example (not complete):
{
  "complete": false,
  "final_answer": "",
  "steps": [
    {
      "plan": "Apply (insert strategy here)",
      "equation": "(insert equation here)"
    },
    {
      "plan": "Compute (insert equation here)",
      "equation": "(insert equation here)"
    }
  ]
}

Example (complete):
{
  "complete": true,
  "final_answer": "The answer is (insert answer here)",
  "steps": []
}

Now output the JSON object:
""")


VALUE_PROMPT = Template("""
Evaluate the candidate step for correctness and usefulness given the history of steps and the input problem. 
Return ONLY valid JSON starting with '{' and ending with '}'.

Structure:
{
  "score": number,
  "proximity": number,
  "comment": string
}

Criteria:
- score: mathematical correctness (0.0 to 1.0)
- proximity: whether the step narrows the search space or makes clear forward progress (0.0 to 1.0)
- comment: brief explanation

Input:
$input

History:
$history

Candidate Step:
Plan: $plan
Equation: $equation

Return the JSON now:
""")
