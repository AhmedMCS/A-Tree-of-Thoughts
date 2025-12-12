import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.agents import propose_step, score_step
from models.gpt import print_usage
from problem_statements.problems import algebraic_geometry_problem

# greedy depth first search on the tree

def greedy():
    input = algebraic_geometry_problem
    history = ""
    max_iterations = 30 # max depth of the tree
    
    for i in range(max_iterations):
        proposed_steps = propose_step(input, history)
        
        # Check if LLM says problem is complete
        if proposed_steps.get("complete", False):
            print(f"\n{'='*50}")
            print(f"✓ SOLUTION COMPLETE at step {i+1}!")
            print(f"{'='*50}")
            print(f"\nFinal Answer: {proposed_steps.get('final_answer', '')}")
            print(f"\n{'='*50}")
            print("Solution Path:")
            print(f"{'='*50}")
            print(history)
            print_usage()
            return
        
        # Reset each iteration
        best_score = -1
        best_step = None
        
        # Evaluate each proposed step
        for step in proposed_steps.get("steps", []):
            score_result = score_step(input, step["plan"], step["equation"])
            #print(f"Step {i+1}: {step['plan']} (score: {score_result.get('score', 0)})")
            
            if score_result.get("score", 0) > best_score:
                best_score = score_result["score"]
                best_step = step
        
        # Add best step to history
        if best_step:
            history += f"Plan: {best_step['plan']}\nEquation: {best_step['equation']}\n\n"
            print(f"Step {i+1}: {best_step['plan']} (score: {best_score})")
        else:
            print("No valid steps found, stopping.")
            break
    

    print_usage()
    print("\n" + "="*50)
    print("Max iterations reached without completion")
    print("="*50)
    print(history)

if __name__ == "__main__":
    greedy()