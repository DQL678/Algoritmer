import pygame
import math
import random

# Skærmindstillinger
WIDTH, HEIGHT = 1000, 800
RADIUS = 10
ROWS, COLS = 50, 55

# Farver
BG_COLOR = (20, 20, 20)
HEX_COLOR = (100, 180, 250)
LINE_COLOR = (50, 50, 50)
FLAG_COLOR = (0, 200, 0)
ENEMY_COLOR = (200, 0, 0)

# Hexagon dimensioner
HEX_WIDTH = math.sqrt(3) * RADIUS
HEX_HEIGHT = 2 * RADIUS
HORIZ_SPACING = HEX_WIDTH
VERT_SPACING = 0.75 * HEX_HEIGHT

# Hexagon center-beregning
def hex_center(col, row):
    x = col * HORIZ_SPACING
    y = row * VERT_SPACING
    if col % 2 == 1:
        y += VERT_SPACING / 2
    return int(x + RADIUS), int(y + RADIUS)

# Tegning af en hexagon
def draw_hex(surface, x, y, color=HEX_COLOR):
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + RADIUS * math.cos(angle)
        py = y + RADIUS * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, LINE_COLOR, points, 1)

# Find hex baseret på klikposition
def get_hex_at_pos(pos):
    x, y = pos
    for row in range(ROWS):
        for col in range(COLS):
            cx, cy = hex_center(col, row)
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist < RADIUS:
                return (col, row)
    return None

# Main
flag_position = None
enemy_position = (random.randint(0, COLS-1), random.randint(0, ROWS-1))

def run_hex_map():
    global flag_position

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hex Map")
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BG_COLOR)

        for row in range(ROWS):
            for col in range(COLS):
                cx, cy = hex_center(col, row)

                if (col, row) == flag_position:
                    draw_hex(screen, cx, cy, FLAG_COLOR)
                elif (col, row) == enemy_position:
                    draw_hex(screen, cx, cy, ENEMY_COLOR)
                else:
                    draw_hex(screen, cx, cy)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = get_hex_at_pos(pygame.mouse.get_pos())
                if clicked:
                    flag_position = clicked

    pygame.quit()

# Kør fil seperat, hvis den ikke køres ud fra main
if __name__ == "__main__":
    run_hex_map()
