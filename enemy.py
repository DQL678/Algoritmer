import heapq
from collections import deque
from itertools import count

# 4-retningers grid
def get_neighbors(pos, max_cols, max_rows):
    col, row = pos
    directions = [
        (1, 0), (-1, 0),
        (0, 1), (0, -1)
    ]

    neighbors = []
    for dc, dr in directions:
        nc, nr = col + dc, row + dr
        if 0 <= nc < max_cols and 0 <= nr < max_rows:
            neighbors.append((nc, nr))

    return neighbors


def manhattan(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


# HARD = A*
# returnerer: path, steps, visited_tiles
def a_star_search(start, goal, max_cols, max_rows, blocked=None):
    if blocked is None:
        blocked = set()

    unique = count()

    open_set = []
    start_h = manhattan(start, goal)
    heapq.heappush(open_set, (start_h, start_h, next(unique), start))

    came_from = {}
    cost_so_far = {start: 0}

    visited = []
    steps = 0
    closed_set = set()

    while open_set:
        _, _, _, current = heapq.heappop(open_set)

        if current in closed_set:
            continue

        closed_set.add(current)
        visited.append(current)
        steps += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, max_cols, max_rows):
            if neighbor in blocked:
                continue

            if neighbor in closed_set:
                continue

            new_cost = cost_so_far[current] + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                h = manhattan(neighbor, goal)
                f = new_cost + h
                heapq.heappush(open_set, (f, h, next(unique), neighbor))
                came_from[neighbor] = current

    if goal not in came_from and goal != start:
        return [], steps, visited

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], steps, visited

    path.append(start)
    path.reverse()
    return path, steps, visited


# EASY = BFS
# returnerer: path, steps, visited_tiles
def bfs_search(start, goal, max_cols, max_rows, blocked=None):
    if blocked is None:
        blocked = set()

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

    if goal not in came_from and goal != start:
        return [], steps, visited

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], steps, visited

    path.append(start)
    path.reverse()
    return path, steps, visited


def get_pathfinder(difficulty):
    if difficulty == "easy":
        return bfs_search
    return a_star_search