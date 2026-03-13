import heapq
from collections import deque

# hvor aggressivt A* skal søge mod målet
# højere tal = mere direkte mod målet
HEURISTIC_WEIGHT = 2.0


# 4-retningers grid
def get_neighbors(pos, max_cols, max_rows):
    col, row = pos
    directions = [
        (1, 0),   # højre
        (-1, 0),  # venstre
        (0, 1),   # ned
        (0, -1)   # op
    ]

    neighbors = []
    for dc, dr in directions:
        nc = col + dc
        nr = row + dr

        if 0 <= nc < max_cols and 0 <= nr < max_rows:
            neighbors.append((nc, nr))

    return neighbors


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# HARD = A*
# returnerer: path, steps, visited_tiles
def a_star_search(start, goal, max_cols, max_rows, blocked=None):
    if blocked is None:
        blocked = set()

    if start == goal:
        return [start], 0, [start]

    open_set = []

    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    visited = []
    steps = 0
    counter = 0

    start_h = manhattan(start, goal)
    start_f = start_h * HEURISTIC_WEIGHT

    # (f, h, counter, node)
    heapq.heappush(open_set, (start_f, start_h, counter, start))

    while open_set:
        _, _, _, current = heapq.heappop(open_set)

        if current in closed_set:
            continue

        closed_set.add(current)
        visited.append(current)
        steps += 1

        if current == goal:
            break

        neighbors = get_neighbors(current, max_cols, max_rows)

        # naboer der er tættest på målet behandles først
        neighbors.sort(key=lambda n: manhattan(n, goal))

        for neighbor in neighbors:
            if neighbor in blocked:
                continue

            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                h = manhattan(neighbor, goal)
                f = tentative_g + (h * HEURISTIC_WEIGHT)

                counter += 1
                heapq.heappush(open_set, (f, h, counter, neighbor))

    if goal not in came_from:
        return [], steps, visited

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return path, steps, visited


# EASY = BFS
# returnerer: path, steps, visited_tiles
def bfs_search(start, goal, max_cols, max_rows, blocked=None):
    if blocked is None:
        blocked = set()

    if start == goal:
        return [start], 0, [start]

    queue = deque([start])
    came_from = {start: None}
    visited_set = {start}

    visited = []
    steps = 0

    while queue:
        current = queue.popleft()
        visited.append(current)
        steps += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, max_cols, max_rows):
            if neighbor in blocked:
                continue

            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current

    if goal not in came_from:
        return [], steps, visited

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return path, steps, visited


def get_pathfinder(difficulty):
    if difficulty == "easy":
        return bfs_search
    return a_star_search