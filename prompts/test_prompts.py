from string import Template

TEST_PROPOSE_PROMPT = Template("""
Input: $input

Your goal is to solve this problem step-by-step.
Given the current history (if any), propose exactly $k distinct, valid next steps to continue solving this problem.

Current History:
$history

Output your response as a JSON object with this exact structure:
{
  "complete": false,
  "final_answer": "",
  "steps": [
    {
      "plan": "description of the strategy",
      "equation": "the mathematical formula or calculation"
    },
    {
      "plan": "description of another strategy",
      "equation": "another mathematical formula or calculation"
    }
  ]
}

IMPORTANT:
- If you have reached the FINAL ANSWER to the problem, set "complete": true, put the complete final answer in "final_answer", and set "steps" to an empty array [].
- If you still need more steps to solve the problem, set "complete": false, leave "final_answer" as an empty string "", and provide $k next steps in the "steps" array.

Example when NOT complete:
{
  "complete": false,
  "final_answer": "",
  "steps": [
    {
      "plan": "Find the derivative of f(x) using the power rule",
      "equation": "f'(x) = 4x^3 + 6x"
    },
    {
      "plan": "Set the derivative equal to 2 to find x-coordinate",
      "equation": "4x^3 + 6x = 2"
    }
  ]
}

Example when complete:
{
  "complete": true,
  "final_answer": "The equation of the tangent line is y = 2x + 5",
  "steps": []
}

Now provide your response as JSON:
""")

TEST_VALUE_PROMPT = Template("""Evaluate the following step in solving this problem.

Input: $input

Candidate Step:
Plan: $plan
Equation: $equation

Evaluation Criteria:
1. Is the mathematical reasoning theoretically sound?
2. Is the calculation correct (if applicable)?
3. Does this step make meaningful progress toward the final answer?

Output your evaluation as a JSON object:
{
  "score": 0.85,
  "comment": "brief explanation of the score"
}

Score guidelines:
- 1.0 = Perfect step (correct theory and calculation, makes significant progress)
- 0.7-0.9 = Good step (correct approach, minor issues or moderate progress)
- 0.4-0.6 = Partially correct (right direction but significant errors or minimal progress)
- 0.0-0.3 = Incorrect (wrong approach or major errors)

Your evaluation as JSON:
""")