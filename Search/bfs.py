import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from models.agents import propose_step, score_step, compress_history
from models.gpt import print_usage
from problem_statements.problems import algebraic_geometry_problem
from Node import Node
import numpy as np



def beam_search():
    input = algebraic_geometry_problem
    root = Node("", [], depth=0)
    max_iterations = 30
    beam_width = 2
    k = 2  # thoughts per node
    
    beam = [root]  # Current beam 
    
    for i in range(max_iterations):
        print(f"\n{'='*60}")
        print(f"Iteration {i+1} - Exploring {len(beam)} paths")
        print(f"{'='*60}")
        
        all_candidates = []
        
        for node in beam:
            print(f"\nExpanding node (depth {node.depth}, score: {node.get_total_score():.2f})")
            
            # Propose steps
            proposed_steps = propose_step(input, node.history, k=k)
            
            # Check if complete
            if proposed_steps.get("complete", False):
                print(f"\n✓ SOLUTION FOUND!")
                print(f"Final Answer: {proposed_steps.get('final_answer', '')}")
                print(f"\n{'='*60}")
                print("Solution Path:")
                print(f"{'='*60}")
                print(node.history)
                print_usage()
                return node
            # Generate children
            for step in proposed_steps.get("steps", []):
                score_result = score_step(input, step["plan"], step["equation"])
                step_score = score_result.get("score", 0)
                
                new_history = node.history + f"Plan: {step['plan']}\nEquation: {step['equation']}\n\n"
                new_history = compress_history(new_history)
                new_scores = node.scores + [step_score]
                new_node = Node(new_history, new_scores, depth=node.depth + 1)
                if new_node.get_total_score() >= 0.5:
                    all_candidates.append(new_node)
                    print(f"  Child (score: {step_score:.2f}): {step['plan'][:60]}...")
        
        all_candidates.sort(key=lambda x: x.get_total_score(), reverse=True)
        beam = all_candidates[:beam_width]
        
        print(f"\nKept top {beam_width} paths:")
        for j, node in enumerate(beam):
            print(f"  Path {j+1}: avg score = {node.get_total_score():.2f}")
            print(f"node history length: {len(node.history)} characters")
    
    # Max iterations reached - return best
    best = max(beam, key=lambda x: x.get_total_score())
    print("\n" + "="*60)
    print(f"Max iterations reached")
    print(f"Best path (avg score: {best.get_total_score():.2f}):")
    print("="*60)
    print(best.history)
    print_usage()
    return best

if __name__ == "__main__":
    beam_search()