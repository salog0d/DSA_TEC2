import heapq
from collections import deque
import numpy as np

def loadMap(fileName):
    grid = []
    with open(fileName, "r") as f:
        for line in f:
            row = list(map(int, line.strip().split()))
            grid.append(row)
    return np.array(grid)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    rows, cols = grid.shape
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        for d in dirs:
            nr, nc = current[0] + d[0], current[1] + d[1]
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                neighbor = (nr, nc)
                tentative_g = cost + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, tentative_g, neighbor))
                    came_from[neighbor] = current
    return None

goal_state = ((1,2,3),(4,5,6),(7,8,0))

def neighbors(state):
    s = [list(row) for row in state]
    for i in range(3):
        for j in range(3):
            if s[i][j] == 0:
                r, c = i, j
    moves = []
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            s2 = [row[:] for row in s]
            s2[r][c], s2[nr][nc] = s2[nr][nc], s2[r][c]
            moves.append(tuple(tuple(row) for row in s2))
    return moves

def bfs_puzzle(start):
    q = deque([start])
    parent = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal_state:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        for nxt in neighbors(cur):
            if nxt not in parent:
                parent[nxt] = cur
                q.append(nxt)
    return None

if __name__ == "__main__":
    grid = loadMap("optimizacion/map2.txt")
    start = (9,1)
    goal = (5,8)
    path = astar(grid, start, goal)
    print("Path encontrado:")
    print(path)
    print("Longitud:", len(path)-1)

    print("\nN-Puzzle:\n")

    start_puzzle = (
        (3,2,0),
        (7,1,4),
        (6,5,8),
    )

    solution = bfs_puzzle(start_puzzle)
    print("Pasos totales:", len(solution)-1)
    for step, mat in enumerate(solution):
        print(f"\nPaso {step}:")
        for row in mat:
            print(row)
