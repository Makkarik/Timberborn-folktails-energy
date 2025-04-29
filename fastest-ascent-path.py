import numpy 

def find_fastest_ascent_path(heatmap):
    """
    Find the path with the fastest ascent from bottom-left to top-right.
    
    Args:
        heatmap: An n×m matrix with values in non-descending order
        
    Returns:
        A list of coordinates representing the fastest ascent path
    """
    n = len(heatmap)
    m = len(heatmap[0])
    
    # Initialize distance matrix with negative infinity
    # (we're maximizing the minimum difference)
    distances = [[-float('inf') for _ in range(m)] for _ in range(n)]
    distances[n-1][0] = float('inf')  # Start point
    
    # Initialize parent matrix to track the path
    parents = [[None for _ in range(m)] for _ in range(n)]
    
    # Priority queue for Dijkstra's algorithm
    # We'll use a list and sort it each time (for simplicity)
    # In a real implementation, use a proper priority queue
    queue = [(n-1, 0, float('inf'))]  # (row, col, min_difference)
    
    # Possible moves: up, right, up-right (diagonal)
    moves = [(-1, 0), (0, 1), (-1, 1)]
    
    visited = set()
    
    while queue:
        # Sort in descending order of minimum difference
        queue.sort(key=lambda x: x[2], reverse=True)
        r, c, min_diff = queue.pop(0)
        
        # Skip if already processed
        if (r, c) in visited:
            continue
        
        visited.add((r, c))
        
        # Found the destination
        if r == 0 and c == m-1:
            break
        
        # Check all possible moves
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            # Check if the new position is within bounds
            if 0 <= nr < n and 0 <= nc < m:
                # Calculate the difference between the new cell and current cell
                diff = heatmap[nr][nc] - heatmap[r][c]
                
                # The new minimum difference is the minimum of the current minimum
                # and the difference between the current and new cell
                new_min_diff = min(min_diff, diff)
                
                # If this path provides a better (larger) minimum difference
                if new_min_diff > distances[nr][nc]:
                    distances[nr][nc] = new_min_diff
                    parents[nr][nc] = (r, c)
                    queue.append((nr, nc, new_min_diff))
    
    # Reconstruct the path from destination to start
    path = []
    r, c = 0, m-1  # Destination
    
    while (r, c) != (n-1, 0):  # Until we reach the start
        path.append((r, c))
        r, c = parents[r][c]
    
    path.append((n-1, 0))  # Add the start point
    path.reverse()  # Reverse to get the path from start to destination
    
    return path


def calculate_path_differences(heatmap, path):
    """Calculate the differences between consecutive cells in the path."""
    differences = []
    for i in range(1, len(path)):
        r1, c1 = path[i-1]
        r2, c2 = path[i]
        diff = heatmap[r2][c2] - heatmap[r1][c1]
        differences.append(diff)
    return differences


# Example usage
if __name__ == "__main__":
    # Example heatmap (values in non-descending order)
    heatmap = np.load()
    
    path = find_fastest_ascent_path(heatmap)
    differences = calculate_path_differences(heatmap, path)
    
    print("Fastest ascent path:", path)
    print("Differences between consecutive cells:", differences)
    print("Minimum difference (to maximize):", min(differences) if differences else 0)
