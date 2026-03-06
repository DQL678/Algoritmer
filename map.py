import pygame
import random
from enemy import a_star_search
from player import Player

# Skærmindstillinger
WIDTH, HEIGHT = 1200, 700
TILE_SIZE = 12
UI_TOP = 40

ROWS = (HEIGHT - UI_TOP) // TILE_SIZE
COLS = WIDTH // TILE_SIZE

# Farver
BG_COLOR = (35, 35, 35)
TILE_COLOR = (235, 235, 235)
LINE_COLOR = (180, 180, 180)
ENEMY_COLOR = (200, 50, 50)
FLAG_COLOR = (0, 120, 0)
PATH_COLOR = (255, 215, 0)
BUTTON_COLOR = (80, 80, 80)
BUILD_BUTTON_COLOR = (70, 120, 70)
REMOVE_BUTTON_COLOR = (150, 70, 70)

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
    dragging = False

    # Nyt
    path_length = 0
    show_path_length = False

    font = pygame.font.SysFont(None, 24)

    start_button = pygame.Rect(WIDTH // 2 - 50, 5, 100, 30)
    build_button = pygame.Rect(10, 5, 130, 30)
    remove_button = pygame.Rect(150, 5, 140, 30)

    running = True
    while running:
        screen.fill(BG_COLOR)

        # UI
        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        screen.blit(font.render("START", True, (255,255,255)), (start_button.x+20, start_button.y+6))

        pygame.draw.rect(screen, BUILD_BUTTON_COLOR, build_button)
        screen.blit(font.render("BUILD", True, (255,255,255)), (build_button.x+25, build_button.y+6))

        pygame.draw.rect(screen, REMOVE_BUTTON_COLOR, remove_button)
        screen.blit(font.render("REMOVE", True, (255,255,255)), (remove_button.x+20, remove_button.y+6))

        # Vis path-længde kun når animation er færdig
        if show_path_length:
            length_text = font.render(f"Path length: {path_length}", True, (255,255,255))
            screen.blit(length_text, (WIDTH - 200, 10))

        # Grid
        for row in range(ROWS):
            for col in range(COLS):
                draw_tile(screen, col, row, TILE_COLOR)

        player.draw_walls(screen, draw_tile)
        player.draw_flag(screen, draw_tile, FLAG_COLOR)
        draw_tile(screen, *start, ENEMY_COLOR)

        # Path
        if started and path:
            for i in range(path_index + 1):
                draw_tile(screen, *path[i], PATH_COLOR)

            if path_index < len(path) - 1:
                path_index += 1
                pygame.time.delay(20)
            else:
                show_path_length = True

        pygame.display.flip()
        clock.tick(60)

        # Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Start knap
                if start_button.collidepoint((mx,my)) and player.get_flag() and not started:
                    path, _ = a_star_search(
                        start,
                        player.get_flag(),
                        COLS,
                        ROWS,
                        blocked=player.get_walls()
                    )
                    path_length = len(path)
                    path_index = 0
                    started = True
                    show_path_length = False

                # Build mode
                elif build_button.collidepoint((mx,my)) and not started:
                    player.enable_build_mode()

                # Remove mode
                elif remove_button.collidepoint((mx,my)) and not started:
                    player.enable_remove_mode()

                # Klik på grid
                elif not started:
                    clicked = tile_from_pos((mx,my))
                    if clicked:
                        dragging = True

                        if player.build_mode:
                            # placer væg midlertidigt
                            player.add_wall(clicked)

                            # hvis flag findes, test path
                            if player.get_flag():
                                path_test, _ = a_star_search(start,player.get_flag(),COLS,ROWS,blocked=player.get_walls())

                                # hvis ingen path → fjern væg
                                if not path_test:
                                    player.remove_wall(clicked)

                        elif player.remove_mode:
                            player.remove_wall(clicked)
                        else:
                            player.set_flag(clicked)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging and not started:
                    mx, my = pygame.mouse.get_pos()
                    clicked = tile_from_pos((mx,my))
                    if clicked:
                        if player.build_mode:
                            # placer væg midlertidigt
                            player.add_wall(clicked)

                            # hvis flag findes, test path
                            if player.get_flag():
                                path_test, _ = a_star_search(start,player.get_flag(),COLS,ROWS,blocked=player.get_walls())

                                # hvis ingen path → fjern væg
                                if not path_test:
                                    player.remove_wall(clicked)

                        elif player.remove_mode:
                            player.remove_wall(clicked)

    pygame.quit()

if __name__ == "__main__":
    run_map()
