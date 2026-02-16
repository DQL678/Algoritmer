import pygame
import random
from enemy import a_star_search
from player import Player

# Skærmindstillinger
WIDTH, HEIGHT = 1200, 700
TILE_SIZE = 12
UI_TOP = 40

ROWS, COLS = (HEIGHT - UI_TOP) // TILE_SIZE, WIDTH // TILE_SIZE

# Farver
BG_COLOR = (35, 35, 35)
TILE_COLOR = (235, 235, 235)
LINE_COLOR = (180, 180, 180)
ENEMY_COLOR = (200, 50, 50)
FLAG_COLOR = (0, 120, 0)
PATH_COLOR = (255, 215, 0)
BUTTON_COLOR = (80, 80, 80)
WALL_BUTTON_COLOR = (120, 120, 120)

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
    pygame.display.set_caption("Protect the Flag")
    clock = pygame.time.Clock()

    start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    player = Player()

    path = []
    path_index = 0
    started = False

    font = pygame.font.SysFont(None, 24)
    start_button_rect = pygame.Rect(WIDTH // 2 - 50, 5, 100, 30)
    wall_button_rect = pygame.Rect(10, 5, 140, 30)

    running = True
    while running:
        screen.fill(BG_COLOR)

        # START KNAP
        pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)
        start_text = font.render("START", True, (255, 255, 255))
        screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 6))

        # BUILD WALL KNAP
        pygame.draw.rect(screen, WALL_BUTTON_COLOR, wall_button_rect)
        wall_text = font.render("BUILD WALL", True, (255, 255, 255))
        screen.blit(wall_text, (wall_button_rect.x + 10, wall_button_rect.y + 6))

        # GRID
        for row in range(ROWS):
            for col in range(COLS):
                draw_tile(screen, col, row, TILE_COLOR)

        # WALLS
        player.draw_walls(screen, draw_tile)

        # FLAG
        player.draw_flag(screen, draw_tile, FLAG_COLOR)

        # ENEMY
        draw_tile(screen, *start, ENEMY_COLOR)

        # PATH
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
                if start_button_rect.collidepoint((mx, my)) and player.get_flag() and not started:
                    path = a_star_search(start, player.get_flag(), COLS, ROWS)
                    path_index = 0
                    started = True

                # WALL MODE TOGGLE
                elif wall_button_rect.collidepoint((mx, my)) and not started:
                    player.toggle_wall_mode()

                # PLACERING
                elif not started:
                    clicked = tile_from_pos((mx, my))
                    if clicked:
                        if player.wall_mode:
                            player.add_wall(clicked)
                        else:
                            player.set_flag(clicked)

    pygame.quit()

if __name__ == "__main__":
    run_map()
