import pygame
import math

# Skærmindstillinger
WIDTH, HEIGHT = 1000, 800
RADIUS = 10
ROWS, COLS = 50, 55

# Farver
BG_COLOR = (20, 20, 20)
HEX_COLOR = (100, 180, 250)
LINE_COLOR = (50, 50, 50)

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
def draw_hex(surface, x, y):
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + RADIUS * math.cos(angle)
        py = y + RADIUS * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, HEX_COLOR, points)
    pygame.draw.polygon(surface, LINE_COLOR, points, 1)

# Main
def run_hex_map():
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
                if 0 <= cx <= WIDTH and 0 <= cy <= HEIGHT:
                    draw_hex(screen, cx, cy)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# Kør fil seperat, hvis den ikke køres ud fra main
if __name__ == "__main__":
    run_hex_map()
