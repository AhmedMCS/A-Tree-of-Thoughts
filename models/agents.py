import json
from models.gpt import client, models, track_usage
from prompts.math_problem import PROPOSE_PROMPT, VALUE_PROMPT
from prompts.test_prompts import TEST_PROPOSE_PROMPT, TEST_VALUE_PROMPT
from prompts.summarizer import SUMMARIZER_PROMPT

MAX_HISTORY_CHARS = 2000

def compress_history(history, MAX_HISTORY_CHARS=MAX_HISTORY_CHARS):
    # No need to summarize small histories
    if len(history) <= MAX_HISTORY_CHARS:
        return history
    
    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "system", "content": "You summarize reasoning histories compactly and accurately."},
            {"role": "user", "content": SUMMARIZER_PROMPT.substitute(history=history)}
        ]
    )

    compressed = response.choices[0].message.content.strip()

    if not compressed:
        return history  

    return compressed




def propose_step(input: str, history: str, k: int = 2) -> dict:
    prompt = PROPOSE_PROMPT.substitute(input=input, history=history, k=k)
    
    messages = [
        {"role": "system", "content": "Return ONLY valid JSON as instructed."},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=models["thinker"],
        messages=messages,
        temperature=0.0,
        max_completion_tokens=5000,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "proposed_steps",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "plan": {"type": "string"},
                                    "equation": {"type": "string"},
                                },
                                "required": ["plan", "equation"]
                            }
                        }
                    },
                    "required": ["steps"]
                }
            }
        }
    )

    track_usage(response)
    
    content = response.choices[0].message.content
    
    if content is None or content.strip() == "":
        print(f"Empty response from API. Response object: {response}")
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from API response. Content: {content[:200]}... Error: {e}")

def f_score_step(input: str, history: str, plan: str, equation: str) -> dict:
    prompt = VALUE_PROMPT.substitute(input=input, history=history, plan=plan, equation=equation)
    
    messages = [
        {"role": "system", "content": "Return ONLY valid JSON"},
        {"role": "user", "content": prompt},
    ]
    
    response = client.chat.completions.create(
        model=models["evaluator"],
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "step_evaluation",
                "schema": {
                    "type": "object",
                    "properties": {
                        "score": {"type": "number"},
                        "heuristic_score": {"type": "number"},
                        "comment": {"type": "string"},
                    },
                    "required": ["score", "heuristic_score", "comment"]
                }
            }
        }
    )

    track_usage(response)

    content = response.choices[0].message.content
    
    if content is None or content.strip() == "":
        raise ValueError(f"Empty response from API. Response object: {response}")
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from API response. Content: {content[:200]}... Error: {e}")

def score_step(input: str, plan: str, equation: str) -> dict:
    prompt = VALUE_PROMPT.substitute(input=input, plan=plan, equation=equation)
    
    messages = [
        {"role": "system", "content": "Return ONLY valid JSON"},
        {"role": "user", "content": prompt},
    ]
    
    response = client.chat.completions.create(
        model=models["evaluator"],
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "step_evaluation",
                "schema": {
                    "type": "object",
                    "properties": {
                        "score": {"type": "number"},
                        "comment": {"type": "string"},
                    },
                    "required": ["score", "comment"]
                }
            }
        }
    )

    track_usage(response)

    content = response.choices[0].message.content
    
    if content is None or content.strip() == "":
        raise ValueError(f"Empty response from API. Response object: {response}")
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from API response. Content: {content[:200]}... Error: {e}")


def test_propose_step(input: str, history: str, k: int = 2) -> dict:
    prompt = TEST_PROPOSE_PROMPT.substitute(input=input, history=history or "None", k=k)
    
    messages = [
        {"role": "system", "content": "Return ONLY valid JSON as instructed."},
        {"role": "user", "content": prompt},
    ]
    
    response = client.chat.completions.create(
        model=models["thinker-test"],
        messages=messages,
        temperature=0.0,
        max_completion_tokens=1000,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "proposed_steps",
                "schema": {
                    "type": "object",
                    "properties": {
                        "complete": {"type": "boolean"},
                        "final_answer": {"type": "string"},
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "plan": {"type": "string"},
                                    "equation": {"type": "string"},
                                },
                                "required": ["plan", "equation"]
                            }
                        }
                    },
                    "required": ["complete", "final_answer", "steps"]
                }
            }
        }
    )

    track_usage(response)

    content = response.choices[0].message.content
    
    if content is None or content.strip() == "":
        raise ValueError(f"Empty response from API. Response object: {response}")
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from API response. Content: {content[:200]}... Error: {e}")

def test_score_step(input: str, plan: str, equation: str) -> dict:
    prompt = TEST_VALUE_PROMPT.substitute(input=input, plan=plan, equation=equation)
    
    messages = [
        {"role": "system", "content": "Return ONLY valid JSON"},
        {"role": "user", "content": prompt},
    ]
    
    response = client.chat.completions.create(
        model=models["evaluator-test"],
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "step_evaluation",
                "schema": {
                    "type": "object",
                    "properties": {
                        "score": {"type": "number"},
                        "comment": {"type": "string"},
                    },
                    "required": ["score", "comment"]
                }
            }
        }
    )

    track_usage(response)

    content = response.choices[0].message.content
    
    if content is None or content.strip() == "":
        raise ValueError(f"Empty response from API. Response object: {response}")
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from API response. Content: {content[:200]}... Error: {e}")