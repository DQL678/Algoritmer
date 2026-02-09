import pygame
import random
from enemy import a_star_search

# Skærmindstillinger
WIDTH, HEIGHT = 1200, 700
TILE_SIZE = 12

# Beregn rækker og kolonner
ROWS, COLS = (HEIGHT - 40) // TILE_SIZE, WIDTH // TILE_SIZE


# Farver
BG_COLOR = (20, 20, 20)
TILE_COLOR = (100, 180, 250)
LINE_COLOR = (50, 50, 50)
ENEMY_COLOR = (200, 50, 50)
FLAG_COLOR = (50, 200, 50)
PATH_COLOR = (255, 255, 0)
BUTTON_COLOR = (100, 100, 100)

# Find center af en firkant
def square_center(col, row):
    x = col * TILE_SIZE
    y = row * TILE_SIZE + 40  # plads til knap
    return x, y

# Tegn en firkant
def draw_tile(surface, col, row, color):
    x, y = square_center(col, row)
    pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(surface, LINE_COLOR, (x, y, TILE_SIZE, TILE_SIZE), 1)

# Find firkant fra klik
def tile_from_pos(pos):
    px, py = pos
    py -= 40  # justering for knap
    col = px // TILE_SIZE
    row = py // TILE_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return col, row
    return None

# Kør spillet
def run_map():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Square Grid Map")
    clock = pygame.time.Clock()

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

        # Knap
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        text = font.render("START", True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 20, button_rect.y + 5))

        # Tegn grid
        for row in range(ROWS):
            for col in range(COLS):
                draw_tile(screen, col, row, TILE_COLOR)

        # Mål og start
        if goal:
            draw_tile(screen, *goal, FLAG_COLOR)
        if start:
            draw_tile(screen, *start, ENEMY_COLOR)

        # Path
        if started and path:
            for i in range(path_index + 1):
                draw_tile(screen, *path[i], PATH_COLOR)
            if path_index < len(path) - 1:
                path_index += 1
                pygame.time.delay(30)

        pygame.display.flip()
        clock.tick(60)

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
                    clicked = tile_from_pos((mx, my))
                    if clicked:
                        goal = clicked

    pygame.quit()
