import pygame
from blockies import Blockies
import const
import operator
import sys

white = pygame.Color('White')

# INITIALIZATION
pygame.init()
if sys.gettrace() is None:
    screen = pygame.display.set_mode((const.SCREEN_SIZE, const.SCREEN_SIZE), pygame.FULLSCREEN)
else:
    # Running in the debugger
    screen = pygame.display.set_mode((const.SCREEN_SIZE, const.SCREEN_SIZE))
pygame.display.set_caption("Blockies!!!")
clock = pygame.time.Clock()
huge_font = pygame.font.Font('agencyb.ttf', 128)
small_font = pygame.font.Font('agencyb.ttf', 48)
winner_font = pygame.font.Font('agencyb.ttf', 84)
score_font = pygame.font.Font('agencyb.ttf', 72)


# HELPERS
def draw_square(square, color=None):
    col, row = square
    rect = ((col * const.SQ_SIZE) + const.SQ_PADDING,
            (row * const.SQ_SIZE) + const.SQ_PADDING,
            const.SQ_SIZE - (const.SQ_PADDING * 2),
            const.SQ_SIZE - (const.SQ_PADDING * 2))
    if not color:
        color = game.grid.get_square((col, row))
    return pygame.draw.rect(screen, color, rect, 0)


def draw_piece(piece):
    return pygame.draw.polygon(screen, piece.color, piece.points, 0)


def mouse_is_on_screen():
    return (pygame.mouse.get_pos() != (0, 0)) and bool(pygame.mouse.get_focused())


def set_final_scores():
    Blockies.final_scores = []
    total_points = 0
    for piece in game.available_pieces:
        total_points += len(piece.squares)

    player_colors = ['Blue', 'Green', 'Red', 'Yellow'][:len(game.player_pieces_available)]
    player_colors.reverse()
    player_scores = {}
    for player_pieces in game.player_pieces_available[:len(player_colors)]:
        score = 0
        for piece in player_pieces:
            score += len(piece.squares)
        player_scores[player_colors.pop()] = total_points - score

    winner = False
    for color, player_score in sorted(player_scores.items(), key=operator.itemgetter(1), reverse=True):
        if not winner:
            Blockies.final_scores.append(
                winner_font.render(color.upper() + ': ' + str(player_score), True, (50, 50, 50)))
            winner = True
        else:
            Blockies.final_scores.append(score_font.render(color + ': ' + str(player_score), True, (50, 50, 50)))


def turn_swap():
    del(game.player_pieces_available[game.player_index][game.active_piece_index])
    previous = game.player_index
    # next player
    if previous < game.num_players - 1:
        game.player_index = previous + 1
    else:
        game.player_index = 0
    while not game.player_has_legal_move():
        # Player does not have legal move
        if previous == game.player_index:
            return False
        if game.player_index < game.num_players - 1:
            game.player_index += 1
        else:
            game.player_index = 0
    game.active_piece_index = 0
    game.active_piece = game.player_pieces_available[game.player_index][game.active_piece_index]
    return True

print('Started Blockies!')

# VARIABLES
game = None
new_square = None
ignore_illegal_square = False
begin_title = huge_font.render("Blockies!", True, const.WHITE)
begin_prompt = small_font.render("press 1, 2, 3 or 4 players", True, const.WHITE)
quit_prompt = small_font.render("press q to quit", True, const.WHITE)
num_players = None

while not game:
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # User clicked close
            quit(0)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_1]:
                num_players = 1
            elif pygame.key.get_pressed()[pygame.K_2]:
                num_players = 2
            elif pygame.key.get_pressed()[pygame.K_3]:
                num_players = 3
            elif pygame.key.get_pressed()[pygame.K_4]:
                num_players = 4
            elif pygame.key.get_pressed()[pygame.K_q]:
                quit(0)
            else:
                continue
            game = Blockies.Game(num_players)

    screen.fill((0, 0, 0))
    total_height = begin_title.get_height() + begin_prompt.get_height()
    screen.blit(begin_title,
                ((const.SCREEN_SIZE/2) - begin_title.get_width() // 2,
                 begin_title.get_height()))

    screen.blit(begin_prompt,
                ((const.SCREEN_SIZE/2) - begin_prompt.get_width() // 2,
                 (const.SCREEN_SIZE/2) + 25 - total_height // 2))

    screen.blit(quit_prompt,
                ((const.SCREEN_SIZE/2) - quit_prompt.get_width() // 2,
                 (const.SCREEN_SIZE/2) + 100 - total_height // 2))

    pygame.draw.polygon(screen, const.LT_BLUE,
                        [[0, 0], [0, 75], [75, 75], [75, 300], [150, 300], [150, 0]])
    pygame.draw.polygon(screen, const.LT_GREEN,
                        [[0, 425], [0, 575], [150, 575], [150, 650],
                         [225, 650], [225, 500], [75, 500], [75, 425]])
    pygame.draw.polygon(screen, const.LT_RED,
                        [[525, 75], [525, 150], [800, 150], [800, 75]])
    pygame.draw.polygon(screen, const.LT_YELLOW,
                        [[650, 300], [650, 525], [725, 525], [725, 450],
                         [800, 450], [800, 375], [725, 375], [725, 300]])

    pygame.display.flip()               # Update display
    clock.tick(60)                      # Limit to 30 frames per second

while not game.done:
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # User clicked close
            quit(0)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP]:
                game.active_piece = game.grid.next_available_piece()
                game.active_piece.move_to(Blockies.square_from_pos(pygame.mouse.get_pos()))
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                game.active_piece = game.grid.previous_available_piece()
                game.active_piece.move_to(Blockies.square_from_pos(pygame.mouse.get_pos()))
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                game.active_piece.rotate_clockwise()
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                game.active_piece.rotate_counter_clockwise()
            elif pygame.key.get_pressed()[pygame.K_q]:
                quit(0)
            game.active_piece.set_color(game.players_lt_colors[game.player_index])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.update_active_piece(event.pos)
            clicked_square = Blockies.square_from_pos(event.pos)
            if game.active_piece.is_legal:
                game.active_piece.set_color(game.players[game.player_index])
                game.grid.set_square(clicked_square, game.active_piece)
                if not turn_swap():
                    # Attempted turn_swap() but nobody can move!
                    set_final_scores()
                # turn_swap succeeded
                game.update_active_piece(event.pos)
                new_square = clicked_square
                # game.grid._display()
        elif event.type == pygame.MOUSEMOTION:
            if mouse_is_on_screen():
                if not Blockies.mouse_in_square(event.pos, new_square):
                    new_square = None
                    game.update_active_piece(event.pos)

    screen.fill((255, 255, 255))
    for col_line_num in range(const.SQ_COLUMNS + 1):
        pygame.draw.line(screen,
                         const.GRID_LINE_COLOR,
                         (col_line_num * const.SQ_SIZE, 0),
                         (col_line_num * const.SQ_SIZE, const.SCREEN_SIZE))

    for row_line_num in range(const.SQ_COLUMNS + 1):
        pygame.draw.line(screen,
                         const.GRID_LINE_COLOR,
                         (0, row_line_num * const.SQ_SIZE),
                         (const.SCREEN_SIZE, row_line_num * const.SQ_SIZE))

    for col_sq in range(const.SQ_COLUMNS):
        for row_sq in range(const.SQ_COLUMNS):
            if game.grid.get_square((col_sq, row_sq)) is not None:
                draw_square((col_sq, row_sq))

    if not game.final_scores:
        if mouse_is_on_screen() and not Blockies.mouse_in_square(pygame.mouse.get_pos(), new_square):
            draw_piece(game.active_piece)
    else:
        overlay = pygame.Surface((const.SCREEN_SIZE, const.SCREEN_SIZE))  # the size of your rect
        overlay.set_alpha(188)              # alpha level
        overlay.fill((255, 255, 255))       # this fills the entire surface
        screen.blit(overlay, (0, 0))        # (0,0) are the top-left coordinates
        score_title = huge_font.render('FINAL SCORE', True, (50, 50, 50))
        total_height = score_title.get_height() + game.final_scores[0].get_height()

        screen.blit(score_title,
                    ((const.SCREEN_SIZE / 2) - score_title.get_width() // 2,
                        (const.SCREEN_SIZE / 2) - 100 - total_height // 2))

        score_y = (const.SCREEN_SIZE / 2) + 60 - total_height // 2

        for final_score in game.final_scores:
            screen.blit(final_score, (
                (const.SCREEN_SIZE / 2) - game.final_scores[0].get_width() // 2,
                score_y))
            score_y += (game.final_scores[-1].get_height() + 20)

    pygame.display.flip()               # Update display

    clock.tick(30)                      # Limit to 30 frames per second
