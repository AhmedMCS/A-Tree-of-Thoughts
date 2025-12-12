import numpy as np
class Node:
    def __init__(self, history: str, scores:list[float], depth=0):
        self.history = history
        self.scores = scores
        self.depth = depth
    
    def get_total_score(self):
        return np.mean(self.scores) if self.scores else 0