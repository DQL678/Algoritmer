import pygame
import random
from enemy import a_star_search
from player import Player

# Skærmindstillinger
WIDTH, HEIGHT = 1200, 700
TILE_SIZE = 12

UI_TOP = 40  # plads til knap i toppen

ROWS, COLS = (HEIGHT - UI_TOP) // TILE_SIZE, WIDTH // TILE_SIZE

# Farver
BG_COLOR = (20, 20, 20)
TILE_COLOR = (100, 180, 250)
LINE_COLOR = (50, 50, 50)
ENEMY_COLOR = (200, 50, 50)
FLAG_COLOR = (50, 200, 50)
PATH_COLOR = (255, 255, 0)
BUTTON_COLOR = (100, 100, 100)

def draw_tile(surface, col, row, color):
    x = col * TILE_SIZE
    y = row * TILE_SIZE + UI_TOP
    pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(surface, LINE_COLOR, (x, y, TILE_SIZE, TILE_SIZE), 1)

def tile_from_pos(pos):
    px, py = pos
    py -= UI_TOP
    col = px // TILE_SIZE
    row = py // TILE_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return int(col), int(row)
    return None

def run_map():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Square Grid Map")
    clock = pygame.time.Clock()

    start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    player = Player()

    path = []
    path_index = 0
    started = False

    font = pygame.font.SysFont(None, 24)
    button_rect = pygame.Rect(WIDTH // 2 - 50, 5, 100, 30)

    running = True
    while running:
        screen.fill(BG_COLOR)

        # START knap
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        text = font.render("START", True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 20, button_rect.y + 6))

        # grid
        for row in range(ROWS):
            for col in range(COLS):
                draw_tile(screen, col, row, TILE_COLOR)

        # flag + enemy
        player.draw_flag(screen, draw_tile, FLAG_COLOR)
        draw_tile(screen, *start, ENEMY_COLOR)

        # path animation
        if started and path:
            for i in range(path_index + 1):
                draw_tile(screen, *path[i], PATH_COLOR)

            if path_index < len(path) - 1:
                path_index += 1
                pygame.time.delay(20)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # START
                if button_rect.collidepoint((mx, my)) and player.get_flag() and not started:
                    path = a_star_search(start, player.get_flag(), COLS, ROWS)
                    path_index = 0
                    started = True

                # flyt flag (indtil start)
                elif not started:
                    clicked = tile_from_pos((mx, my))
                    if clicked:
                        player.set_flag(clicked)

    pygame.quit()

if __name__ == "__main__":
    run_map()
