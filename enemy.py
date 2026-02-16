import heapq

# 4-retningers grid (firkantet map)
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


def a_star_search(start, goal, max_cols, max_rows, blocked=None):
    if blocked is None:
        blocked = set()

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            break

        for neighbor in get_neighbors(current, max_cols, max_rows):

            # 🔥 IGNORER WALLS
            if neighbor in blocked:
                continue

            new_cost = cost_so_far[current] + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + manhattan(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current

    # Hvis ingen vej findes
    if goal not in came_from and goal != start:
        return []

    # Rekonstruer path
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []

    path.append(start)
    path.reverse()

    return path
