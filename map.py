import pygame
import random
from enemy import get_pathfinder, a_star_search
from player import Player

WIDTH, HEIGHT = 1200, 700
TILE_SIZE = 12
UI_TOP = 60

ROWS = (HEIGHT - UI_TOP) // TILE_SIZE
COLS = WIDTH // TILE_SIZE

BG_COLOR = (35, 35, 35)
TILE_COLOR = (235, 235, 235)
LINE_COLOR = (180, 180, 180)

ENEMY_COLOR = (200, 50, 50)
FLAG_COLOR = (0, 120, 0)

SEARCH_COLOR = (80, 140, 255)
PATH_COLOR = (255, 215, 0)

BUTTON_COLOR = (80, 80, 80)
BUILD_BUTTON_COLOR = (70, 120, 70)
REMOVE_BUTTON_COLOR = (150, 70, 70)
MOVE_BUTTON_COLOR = (70, 100, 160)

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


def run_map(game_manager):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        difficulty = game_manager.get_difficulty()
        level = game_manager.get_level()
        step_limit = game_manager.get_step_limit()
        wall_limit = game_manager.get_wall_limit()

        pygame.display.set_caption(f"Protect the Flag - {difficulty.upper()} - Level {level}")

        pathfinder = get_pathfinder(difficulty)

        start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        player = Player()
        player.max_walls = wall_limit

        path = []
        search_tiles = []

        path_index = 0
        search_index = 0

        started = False
        searching = False
        dragging = False

        path_length = 0
        search_steps = 0
        show_path_info = False

        result_message = None
        waiting_after_result = False

        font = pygame.font.SysFont(None, 24)
        big_font = pygame.font.SysFont(None, 36)

        start_button = pygame.Rect(WIDTH // 2 - 50, 5, 100, 30)
        build_button = pygame.Rect(10, 5, 120, 30)
        remove_button = pygame.Rect(140, 5, 130, 30)
        move_flag_button = pygame.Rect(280, 5, 140, 30)
        restart_button = pygame.Rect(430, 5, 120, 30)

        running = True
        while running:
            screen.fill(BG_COLOR)

            pygame.draw.rect(screen, BUTTON_COLOR, start_button)
            screen.blit(font.render("START", True, (255, 255, 255)), (start_button.x + 20, start_button.y + 6))

            current_build_color = ACTIVE_BUILD_BUTTON_COLOR if player.build_mode else BUILD_BUTTON_COLOR
            pygame.draw.rect(screen, current_build_color, build_button)
            screen.blit(font.render("BUILD", True, (255, 255, 255)), (build_button.x + 25, build_button.y + 6))

            current_remove_color = ACTIVE_REMOVE_BUTTON_COLOR if player.remove_mode else REMOVE_BUTTON_COLOR
            pygame.draw.rect(screen, current_remove_color, remove_button)
            screen.blit(font.render("REMOVE", True, (255, 255, 255)), (remove_button.x + 20, remove_button.y + 6))

            current_move_color = ACTIVE_MOVE_BUTTON_COLOR if player.move_flag_mode else MOVE_BUTTON_COLOR
            pygame.draw.rect(screen, current_move_color, move_flag_button)
            screen.blit(font.render("MOVE FLAG", True, (255, 255, 255)), (move_flag_button.x + 10, move_flag_button.y + 6))

            pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
            screen.blit(font.render("RESTART", True, (255, 255, 255)), (restart_button.x + 15, restart_button.y + 6))

            difficulty_text = font.render(f"Difficulty: {difficulty.upper()}", True, (255, 255, 255))
            screen.blit(difficulty_text, (WIDTH - 450, 8))

            level_text = font.render(f"Level: {level}", True, (255, 255, 255))
            screen.blit(level_text, (WIDTH - 320, 8))

            limit_text = font.render(f"Step limit: {step_limit}", True, (255, 255, 255))
            screen.blit(limit_text, (WIDTH - 220, 8))

            wall_text = font.render(f"Walls: {len(player.get_walls())}/{player.max_walls}", True, (255, 255, 255))
            screen.blit(wall_text, (WIDTH - 450, 32))

            if show_path_info:
                path_text = font.render(f"Path: {path_length}", True, (255, 255, 255))
                steps_text = font.render(f"Steps: {search_steps}", True, (255, 255, 255))
                screen.blit(path_text, (WIDTH - 250, 32))
                screen.blit(steps_text, (WIDTH - 120, 32))

            objective_text = font.render(
                f"Objective: make algorithm use MORE than {step_limit} search steps",
                True,
                (255, 255, 255)
            )
            screen.blit(objective_text, (10, HEIGHT - 25))

            for row in range(ROWS):
                for col in range(COLS):
                    draw_tile(screen, col, row, TILE_COLOR)

            player.draw_walls(screen, draw_tile)
            player.draw_flag(screen, draw_tile, FLAG_COLOR)
            draw_tile(screen, *start, ENEMY_COLOR)

            if searching and search_tiles:
                for i in range(search_index + 1):
                    tile = search_tiles[i]
                    if tile != start and tile != player.get_flag():
                        draw_tile(screen, *tile, SEARCH_COLOR)

                if search_index < len(search_tiles) - 1:
                    search_index += 1
                    pygame.time.delay(5)
                else:
                    searching = False
                    started = True

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

                    if not waiting_after_result:
                        if search_steps > step_limit:
                            if game_manager.next_level():
                                result_message = "LEVEL COMPLETE - click to continue"
                            else:
                                result_message = "YOU WON THE GAME - click to restart"
                                game_manager.restart_game()
                        else:
                            result_message = "YOU FAILED - click to retry level"
                        waiting_after_result = True

            player.draw_flag(screen, draw_tile, FLAG_COLOR)
            draw_tile(screen, *start, ENEMY_COLOR)

            if result_message:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 140))
                screen.blit(overlay, (0, 0))

                msg_surface = big_font.render(result_message, True, (255, 255, 255))
                msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(msg_surface, msg_rect)

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    if waiting_after_result:
                        running = False
                        break

                    elif restart_button.collidepoint((mx, my)):
                        start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
                        player = Player()
                        player.max_walls = wall_limit
                        path = []
                        search_tiles = []
                        path_index = 0
                        search_index = 0
                        started = False
                        searching = False
                        show_path_info = False
                        path_length = 0
                        search_steps = 0
                        result_message = None
                        waiting_after_result = False
                        dragging = False

                    elif start_button.collidepoint((mx, my)) and player.get_flag() and not started and not searching:
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
                        result_message = None

                    elif build_button.collidepoint((mx, my)) and not started and not searching:
                        player.toggle_build_mode()

                    elif remove_button.collidepoint((mx, my)) and not started and not searching:
                        player.toggle_remove_mode()

                    elif move_flag_button.collidepoint((mx, my)) and not started and not searching:
                        player.toggle_move_flag_mode()

                    elif not started and not searching:
                        clicked = tile_from_pos((mx, my))

                        if clicked:
                            dragging = True

                            if player.build_mode:
                                player.add_wall(clicked, start)

                                if player.get_flag():
                                    path_test, _, _ = a_star_search(
                                        start,
                                        player.get_flag(),
                                        COLS,
                                        ROWS,
                                        blocked=player.get_walls()
                                    )
                                    if not path_test:
                                        player.remove_wall(clicked)

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
                                player.add_wall(clicked, start)

                                if player.get_flag():
                                    path_test, _, _ = a_star_search(
                                        start,
                                        player.get_flag(),
                                        COLS,
                                        ROWS,
                                        blocked=player.get_walls()
                                    )
                                    if not path_test:
                                        player.remove_wall(clicked)

                            elif player.remove_mode:
                                player.remove_wall(clicked)

                            elif player.move_flag_mode:
                                player.set_flag(clicked)

                # Keybinds
                elif event.type == pygame.KEYDOWN:

                    # F: Move Flag Mode
                    if event.key == pygame.K_f and not started and not searching:
                        player.toggle_move_flag_mode()

                    # B: Build Mode
                    if event.key == pygame.K_b and not started and not searching:
                        player.toggle_build_mode()

                    # R: Remove Mode
                    if event.key == pygame.K_r and not started and not searching:
                        player.toggle_remove_mode()

                    # S: Start pathfinding
                    if event.key == pygame.K_s and player.get_flag() and not started and not searching:
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
                        result_message = None

                    # G: Restart game
                    if event.key == pygame.K_g:
                        start = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
                        player = Player()
                        player.max_walls = wall_limit
                        path = []
                        search_tiles = []
                        path_index = 0
                        search_index = 0
                        started = False
                        searching = False
                        show_path_info = False
                        path_length = 0
                        search_steps = 0
                        result_message = None
                        waiting_after_result = False
                        dragging = False

