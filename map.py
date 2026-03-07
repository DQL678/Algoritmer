import pygame
import random
from enemy import get_pathfinder
from player import Player

# Skærmindstillinger
WIDTH, HEIGHT = 1200, 700
TILE_SIZE = 12
UI_TOP = 40

ROWS = (HEIGHT - UI_TOP) // TILE_SIZE
COLS = WIDTH // TILE_SIZE

# FARVER
BG_COLOR = (35, 35, 35)
TILE_COLOR = (235, 235, 235)
LINE_COLOR = (180, 180, 180)

ENEMY_COLOR = (200, 50, 50)
FLAG_COLOR = (0, 120, 0)

SEARCH_COLOR = (80, 140, 255)   # blå search tiles
PATH_COLOR = (255, 215, 0)      # gul final path

BUTTON_COLOR = (80, 80, 80)
BUILD_BUTTON_COLOR = (70, 120, 70)
REMOVE_BUTTON_COLOR = (150, 70, 70)
MOVE_BUTTON_COLOR = (70, 100, 160)

# Aktive knapfarver
ACTIVE_BUILD_BUTTON_COLOR = (110, 180, 110)
ACTIVE_REMOVE_BUTTON_COLOR = (210, 100, 100)
ACTIVE_MOVE_BUTTON_COLOR = (110, 150, 220)

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

def run_map(difficulty="hard"):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Protect the Flag - {difficulty.upper()}")
    clock = pygame.time.Clock()

    pathfinder = get_pathfinder(difficulty)

    start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    player = Player()

    path = []
    search_tiles = []

    path_index = 0
    search_index = 0

    started = False          # final path animation
    searching = False        # search animation
    dragging = False

    path_length = 0
    search_steps = 0
    show_path_info = False

    font = pygame.font.SysFont(None, 24)

    start_button = pygame.Rect(WIDTH // 2 - 50, 5, 100, 30)
    build_button = pygame.Rect(10, 5, 120, 30)
    remove_button = pygame.Rect(140, 5, 130, 30)
    move_flag_button = pygame.Rect(280, 5, 140, 30)

    running = True
    while running:
        screen.fill(BG_COLOR)

        # START-knap
        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        screen.blit(font.render("START", True, (255, 255, 255)), (start_button.x + 20, start_button.y + 6))

        # BUILD-knap
        current_build_color = ACTIVE_BUILD_BUTTON_COLOR if player.build_mode else BUILD_BUTTON_COLOR
        pygame.draw.rect(screen, current_build_color, build_button)
        screen.blit(font.render("BUILD", True, (255, 255, 255)), (build_button.x + 25, build_button.y + 6))

        # REMOVE-knap
        current_remove_color = ACTIVE_REMOVE_BUTTON_COLOR if player.remove_mode else REMOVE_BUTTON_COLOR
        pygame.draw.rect(screen, current_remove_color, remove_button)
        screen.blit(font.render("REMOVE", True, (255, 255, 255)), (remove_button.x + 20, remove_button.y + 6))

        # MOVE FLAG-knap
        current_move_color = ACTIVE_MOVE_BUTTON_COLOR if player.move_flag_mode else MOVE_BUTTON_COLOR
        pygame.draw.rect(screen, current_move_color, move_flag_button)
        screen.blit(font.render("MOVE FLAG", True, (255, 255, 255)), (move_flag_button.x + 10, move_flag_button.y + 6))

        # Difficulty / Path / Steps
        difficulty_text = font.render(f"Difficulty: {difficulty.upper()}", True, (255, 255, 255))
        screen.blit(difficulty_text, (WIDTH - 420, 10))

        if show_path_info:
            length_text = font.render(f"Path: {path_length}", True, (255, 255, 255))
            steps_text = font.render(f"Steps: {search_steps}", True, (255, 255, 255))
            screen.blit(length_text, (WIDTH - 250, 10))
            screen.blit(steps_text, (WIDTH - 120, 10))

        # Grid
        for row in range(ROWS):
            for col in range(COLS):
                draw_tile(screen, col, row, TILE_COLOR)

        # Walls / Flag / Enemy
        player.draw_walls(screen, draw_tile)
        player.draw_flag(screen, draw_tile, FLAG_COLOR)
        draw_tile(screen, *start, ENEMY_COLOR)

        # -------------------------
        # SEARCH animation (blå)
        # -------------------------
        if searching and search_tiles:
            for i in range(search_index + 1):
                tile = search_tiles[i]

                # undgå at search-farve tegnes ovenpå start og flag
                if tile != start and tile != player.get_flag():
                    draw_tile(screen, *tile, SEARCH_COLOR)

            if search_index < len(search_tiles) - 1:
                search_index += 1
                pygame.time.delay(5)
            else:
                searching = False
                started = True

        # -------------------------
        # FINAL PATH animation (gul)
        # -------------------------
        if started and path:
            for i in range(path_index + 1):
                tile = path[i]

                if tile != start and tile != player.get_flag():
                    draw_tile(screen, *tile, PATH_COLOR)

            if path_index < len(path) - 1:
                path_index += 1
                pygame.time.delay(20)
            else:
                show_path_info = True

        # tegn flag og enemy igen ovenpå, så de altid er synlige
        player.draw_flag(screen, draw_tile, FLAG_COLOR)
        draw_tile(screen, *start, ENEMY_COLOR)

        pygame.display.flip()
        clock.tick(60)

        # Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Start
                if start_button.collidepoint((mx, my)) and player.get_flag() and not started and not searching:
                    path, search_steps, search_tiles = pathfinder(
                        start,
                        player.get_flag(),
                        COLS,
                        ROWS,
                        blocked=player.get_walls()
                    )

                    path_length = len(path)
                    path_index = 0
                    search_index = 0

                    searching = True
                    started = False
                    show_path_info = False

                # Toggle build mode
                elif build_button.collidepoint((mx, my)) and not started and not searching:
                    player.toggle_build_mode()

                # Toggle remove mode
                elif remove_button.collidepoint((mx, my)) and not started and not searching:
                    player.toggle_remove_mode()

                # Toggle move-flag mode
                elif move_flag_button.collidepoint((mx, my)) and not started and not searching:
                    player.toggle_move_flag_mode()

                # Klik på grid
                elif not started and not searching:
                    clicked = tile_from_pos((mx, my))
                    if clicked:
                        dragging = True

                        if player.build_mode:
                            player.add_wall(clicked)

                        elif player.remove_mode:
                            player.remove_wall(clicked)

                        elif player.move_flag_mode:
                            player.set_flag(clicked)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging and not started and not searching:
                    mx, my = pygame.mouse.get_pos()
                    clicked = tile_from_pos((mx, my))
                    if clicked:
                        if player.build_mode:
                            player.add_wall(clicked)
                        elif player.remove_mode:
                            player.remove_wall(clicked)
                        elif player.move_flag_mode:
                            player.set_flag(clicked)

    pygame.quit()

if __name__ == "__main__":
    run_map()