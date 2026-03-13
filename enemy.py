import heapq
from collections import deque

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
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    visited = []
    steps = 0

    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.append(current)
        steps += 1

        if current == goal:
            break

        neighbors = get_neighbors(current, max_cols, max_rows)

        # sortér naboer så dem tættest på målet tages først
        neighbors.sort(key=lambda n: manhattan(n, goal))

        for neighbor in neighbors:
            if neighbor in blocked:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                h = manhattan(neighbor, goal)
                f = tentative_g + h

                heapq.heappush(open_set, (f, neighbor))

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