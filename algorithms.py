import math

def dist(p1, p2):
    return math.hypot(p1['x'] - p2['x'], p1['y'] - p2['y'])

def brute_force(points):
    steps = []
    min_val = float('inf')
    best_pair = None
    n = len(points)
    
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            steps.append({"type": "compare", "p1": p1, "p2": p2})
            d = dist(p1, p2)
            if d < min_val:
                min_val = d
                best_pair = (p1, p2)
                steps.append({"type": "update", "p1": p1, "p2": p2, "dist": min_val})
                
    steps.append({"type": "done", "best": best_pair, "dist": min_val})
    return steps