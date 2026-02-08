import pygame
import math
import random
from enemy import a_star_search

# Skærmindstillinger
WIDTH, HEIGHT = 1000, 800
RADIUS = 10
ROWS, COLS = 50, 55

# Farver
BG_COLOR = (20, 20, 20)
HEX_COLOR = (100, 180, 250)
LINE_COLOR = (50, 50, 50)
ENEMY_COLOR = (200, 50, 50)
FLAG_COLOR = (50, 200, 50)
PATH_COLOR = (255, 255, 0)
BUTTON_COLOR = (100, 100, 100)

# Hexagon dimensioner
HEX_WIDTH = math.sqrt(3) * RADIUS
HEX_HEIGHT = 2 * RADIUS
HORIZ_SPACING = HEX_WIDTH
VERT_SPACING = 0.75 * HEX_HEIGHT

# Hexagon center-beregning
def hex_center(col, row):
    x = col * HORIZ_SPACING
    y = row * VERT_SPACING + 40  # giver plads til knap
    if col % 2 == 1:
        y += VERT_SPACING / 2
    return int(x + RADIUS), int(y + RADIUS)

# Tegn en hexagon
def draw_hex(surface, x, y, color):
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + RADIUS * math.cos(angle)
        py = y + RADIUS * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, LINE_COLOR, points, 1)

# Klik-detection
def hex_from_pos(pos):
    px, py = pos
    closest = None
    min_dist = float("inf")

    for row in range(ROWS):
        for col in range(COLS):
            cx, cy = hex_center(col, row)
            dist = math.hypot(px - cx, py - cy)
            if dist < min_dist:
                min_dist = dist
                closest = (col, row)

    return closest

# Kør spillet
def run_hex_map():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hex Map")
    clock = pygame.time.Clock()

    # Initiale værdier
    start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    goal = None
    path = []
    path_index = 0
    started = False

    font = pygame.font.SysFont(None, 24)
    button_rect = pygame.Rect(WIDTH // 2 - 50, 5, 100, 30)

    running = True
    while running:
        screen.fill(BG_COLOR)

        # --- Tegn knap ---
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        text = font.render("START", True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 20, button_rect.y + 5))

        # --- Tegn hexagoner ---
        for row in range(ROWS):
            for col in range(COLS):
                cx, cy = hex_center(col, row)
                draw_hex(screen, cx, cy, HEX_COLOR)

        if goal:
            gx, gy = hex_center(*goal)
            draw_hex(screen, gx, gy, FLAG_COLOR)

        if start:
            sx, sy = hex_center(*start)
            draw_hex(screen, sx, sy, ENEMY_COLOR)

        if started and path:
            for i in range(path_index + 1):
                cx, cy = hex_center(*path[i])
                draw_hex(screen, cx, cy, PATH_COLOR)

            if path_index < len(path) - 1:
                path_index += 1
                pygame.time.delay(30)

        pygame.display.flip()
        clock.tick(60)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_rect.collidepoint((mx, my)) and goal and not started:
                    path = a_star_search(start, goal, COLS, ROWS)
                    path_index = 0
                    started = True
                elif not goal:
                    clicked = hex_from_pos((mx, my))
                    if clicked:
                        goal = clicked

    pygame.quit()
