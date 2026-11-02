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

def divide_and_conquer(points):
    steps = []
    points_sorted = sorted(points, key=lambda p: p['x'])
    
    def solve(pts):
        n = len(pts)
        if n <= 3:
            best_pair, min_d = None, float('inf')
            for i in range(n):
                for j in range(i + 1, n):
                    steps.append({"type": "compare", "p1": pts[i], "p2": pts[j]})
                    d = dist(pts[i], pts[j])
                    if d < min_d:
                        min_d, best_pair = d, (pts[i], pts[j])
                        steps.append({"type": "update", "p1": pts[i], "p2": pts[j], "dist": min_d})
            return best_pair, min_d

        mid = n // 2
        mid_point = pts[mid]
        steps.append({"type": "line", "x": mid_point['x']})
        
        pairL, distL = solve(pts[:mid])
        pairR, distR = solve(pts[mid:])
        
        d = min(distL, distR)
        best = pairL if distL < distR else pairR
        
        strip = [p for p in pts if abs(p['x'] - mid_point['x']) < d]
        strip.sort(key=lambda p: p['y'])
        
        for i in range(len(strip)):
            for j in range(i+1, min(i+7, len(strip))):
                steps.append({"type": "compare", "p1": strip[i], "p2": strip[j]})
                curr_d = dist(strip[i], strip[j])
                if curr_d < d:
                    d, best = curr_d, (strip[i], strip[j])
                    steps.append({"type": "update", "p1": strip[i], "p2": strip[j], "dist": d})
                    
        return best, d

    if len(points) < 2:
        return []
        
    best_pair, final_dist = solve(points_sorted)
    steps.append({"type": "done", "best": best_pair, "dist": final_dist})
    return steps