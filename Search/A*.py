import sys
import numpy as np
from pathlib import Path
import heapq
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from models.gpt import client
from models.gpt import print_usage
from models.agents import propose_step, f_score_step, compress_history
from problem_statements.problems import algebraic_geometry_problem, number_theory_problem
from Node import Node


def AStarSearch():
    input = number_theory_problem
    max_iterations = 8
    k = 2
    gamma = 0.7
    maxHeap = []
    root = Node("", [], depth=0)
    heapq.heappush(maxHeap, [-root.get_total_score(), 0, root])
    iterations = 0
    node_count = 0 

    while maxHeap and iterations < max_iterations:
        node = heapq.heappop(maxHeap)[2]
        iterations += 1
        print(f"\n{'='*60}")
        print(f"Iteration {iterations}")
        print(f"{'='*60}")
        
        proposed_steps = propose_step(input, node.history, k=k)
        if proposed_steps.get("complete", False):
            print(f"\n{'='*60}")
            print(f"✓ SOLUTION FOUND!")
            print(f"Final Answer: {proposed_steps.get('final_answer', '')}")
            print(f"Solution Path:")
            print(node.history)
            print_usage()
            return node 
        for step in proposed_steps.get("steps", []):
            score_result = f_score_step(input, node.history, step["plan"], step["equation"])
            step_score = score_result.get("score", 0)
            heuristic_score = score_result.get("heuristic_score", 0)
            new_history = node.history + f"Plan: {step['plan']}\nEquation: {step['equation']}\n\n"
            new_history = compress_history(new_history)
            new_scores = node.scores + [step_score]
            new_node = Node(new_history, new_scores, depth=node.depth + 1)
            g = new_node.get_total_score()
            h = heuristic_score
            f = gamma * g + (1-gamma) * h
            if f > 0.5:
                print(f"Child (score: {f:.2f}): {step['plan'][:80]}...")
                print(f"node history length: {len(new_node.history)} characters")
                node_count += 1
                heapq.heappush(maxHeap, (-f, node_count, new_node))
            else:
                print(f"Pruned Node Score: {f:.2f}: {step['plan'][:80]}...")

    print("\n" + "="*60)
    print(f"Max iterations reached without problem completion")
    print("="*60)
    print_usage()

if __name__ == "__main__":
    AStarSearch()
