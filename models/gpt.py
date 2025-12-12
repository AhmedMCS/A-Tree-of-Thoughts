import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    raise ValueError("OPENAI_API_KEY is not set")


models = {
    "thinker": "gpt-5.1",
    "evaluator": "gpt-5.1",
    "compressor": "gpt-5.1",
    "thinker-test": "gpt-4.1",
    "evaluator-test": "gpt-4.1",
}

TOKEN_USAGE = {
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0,
    "calls": 0,
}


def track_usage(response):
    """
    Extract token usage from an OpenAI response object
    and update global counters.
    """
    usage = response.usage  # Responses API returns a usage object

    # Some models return null usage for streaming or malformed responses:
    if usage is None:
        return

    input_tokens = getattr(usage, "input_tokens", 0)
    output_tokens = getattr(usage, "output_tokens", 0)
    total_tokens = getattr(usage, "total_tokens", input_tokens + output_tokens)

    TOKEN_USAGE["input_tokens"] += input_tokens
    TOKEN_USAGE["output_tokens"] += output_tokens
    TOKEN_USAGE["total_tokens"] += total_tokens
    TOKEN_USAGE["calls"] += 1


def print_usage():
    """Convenience function to show usage stats."""
    print("\n=== Token Usage Summary ===")
    print(f"Total Calls:       {TOKEN_USAGE['calls']}")
    print(f"Input Tokens:      {TOKEN_USAGE['input_tokens']}")
    print(f"Output Tokens:     {TOKEN_USAGE['output_tokens']}")
    print(f"Total Tokens:      {TOKEN_USAGE['total_tokens']}")
    print("===========================\n")