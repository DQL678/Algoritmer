import pygame
import math
import random
from enemy import a_star_search

WIDTH, HEIGHT = 1000, 800
RADIUS = 10
ROWS, COLS = 50, 55

BG_COLOR = (20, 20, 20)
HEX_COLOR = (100, 180, 250)
LINE_COLOR = (50, 50, 50)
ENEMY_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 255, 0)
PATH_COLOR = (255, 255, 0)

HEX_WIDTH = math.sqrt(3) * RADIUS
HEX_HEIGHT = 2 * RADIUS
HORIZ_SPACING = HEX_WIDTH
VERT_SPACING = 0.75 * HEX_HEIGHT

def hex_center(col, row):
    x = col * HORIZ_SPACING
    y = row * VERT_SPACING
    if col % 2 == 1:
        y += VERT_SPACING / 2
    return int(x + RADIUS), int(y + RADIUS)

def draw_hex(surface, x, y, color):
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + RADIUS * math.cos(angle)
        py = y + RADIUS * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, LINE_COLOR, points, 1)

def run_hex_map():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hex Map")
    clock = pygame.time.Clock()
    running = True

    start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    goal = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    while goal == start:
        goal = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))

    path = a_star_search(start, goal, COLS, ROWS)

    step_index = 0
    step_timer = 0
    step_delay = 300  # ms mellem trin

    while running:
        dt = clock.tick(60)
        screen.fill(BG_COLOR)

        for row in range(ROWS):
            for col in range(COLS):
                cx, cy = hex_center(col, row)
                draw_hex(screen, cx, cy, HEX_COLOR)

        for pos in path:
            cx, cy = hex_center(*pos)
            draw_hex(screen, cx, cy, PATH_COLOR)

        gx, gy = hex_center(*goal)
        draw_hex(screen, gx, gy, GOAL_COLOR)

        if path:
            step_timer += dt
            if step_timer >= step_delay and step_index < len(path) - 1:
                step_index += 1
                step_timer = 0
            ex, ey = hex_center(*path[step_index])
            draw_hex(screen, ex, ey, ENEMY_COLOR)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
