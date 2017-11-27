import pygame
import pygame.freetype
from blockies import Blockies
import const
import copy
import operator

white = pygame.Color('White')

# INITIALIZATION
pygame.init()
screen = pygame.display.set_mode((const.SCREEN_SIZE, const.SCREEN_SIZE), pygame.FULLSCREEN)
pygame.display.set_caption("Blockies!!!")
clock = pygame.time.Clock()

huge_font = pygame.font.Font("/System/Library/Fonts/MarkerFelt.ttc", 128)
small_font = pygame.font.Font("/System/Library/Fonts/MarkerFelt.ttc", 44)
score_font = pygame.font.Font("/System/Library/Fonts/MarkerFelt.ttc", 86)


# HELPERS
def set_columns(num_players):
    if num_players == 2:
        const.SQ_COLUMNS = 8
    elif num_players == 3:
        const.SQ_COLUMNS = 10
    elif num_players == 4:
        const.SQ_COLUMNS = 12
    const.SQ_SIZE = int(const.SCREEN_SIZE / const.SQ_COLUMNS)


def draw_square(square, color=None):
    col, row = square
    rect = ((col * const.SQ_SIZE) + const.SQ_PADDING,
            (row * const.SQ_SIZE) + const.SQ_PADDING,
            const.SQ_SIZE - (const.SQ_PADDING * 2),
            const.SQ_SIZE - (const.SQ_PADDING * 2))
    if not color:
        color = grid.get_square((col, row))
    return pygame.draw.rect(screen, color, rect, 0)


def draw_piece(piece):
    return pygame.draw.polygon(screen, piece.color, piece.points, 0)


def mouse_is_on_screen():
    return (pygame.mouse.get_pos() != (0, 0)) and bool(pygame.mouse.get_focused())


def set_final_scores():
    scores = []
    total_points = 0
    for piece in grid.available_pieces:
        total_points += len(piece.squares)

    player_colors = ['Blue', 'Green', 'Red', 'Yellow'][:len(Blockies.player_pieces_available)]
    player_colors.reverse()
    player_scores = {}
    for player_pieces in Blockies.player_pieces_available[:len(player_colors)]:
        score = 0
        for piece in player_pieces:
            score += len(piece.squares)
        player_scores[player_colors.pop()] = total_points - score

    for color, score in sorted(player_scores.items(), key=operator.itemgetter(1), reverse=True):
        scores.append(color + ': ' + str(score))
    scores_text = '  '.join(scores)
    Blockies.final_scores = small_font.render(scores_text, True, (128, 128, 128))


def turn_swap():
    del(Blockies.player_pieces_available[Blockies.player_index][grid.active_piece_index])
    previous = Blockies.player_index
    # next player
    if previous < Blockies.num_players - 1:
        Blockies.player_index = previous + 1
    else:
        Blockies.player_index = 0
    while not grid.player_has_legal_move():
        # Player does not have legal move
        if previous == Blockies.player_index:
            return False
        if Blockies.player_index < Blockies.num_players - 1:
            Blockies.player_index += 1
        else:
            Blockies.player_index = 0
    grid.active_piece_index = 0
    grid.active_piece = Blockies.player_pieces_available[Blockies.player_index][grid.active_piece_index]
    return True


# ====================================================================
# NOTES
# make grid (10 by 10) - done
# make single square pieces - done
# place pieces - done
# Then, upgrade
#   two player
#   piece shape
#   rotate and flip piece
#   display unused pieces
#   calculate winner

# GRAPHICS
# grid - done
# piece - single square only, so far

# CODE
# grid - done
# piece - not done
# test - done
# place - single square only, so far
#
# Checkers-ish instead?
# ====================================================================


print('Started Blockies!')

# VARIABLES
done = False
new_square = None
ignore_illegal_square = False
Blockies.final_scores = None
started = False
begin_title = huge_font.render("Blockies!", True, const.WHITE)
begin_prompt = small_font.render("how many players? (2 to 4)", True, const.WHITE)

while not started:
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # User clicked close
            quit(0)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_2]:
                Blockies.num_players = 2
                started = True
            elif pygame.key.get_pressed()[pygame.K_3]:
                Blockies.num_players = 3
                started = True
            elif pygame.key.get_pressed()[pygame.K_4]:
                Blockies.num_players = 4
            elif pygame.key.get_pressed()[pygame.K_q]:
                quit(0)
            else:
                continue
            set_columns(Blockies.num_players)
            grid = Blockies.Grid()
            Blockies.players = const.PIECE_COLORS[:Blockies.num_players]
            for player in range(Blockies.num_players):
                Blockies.player_pieces_available.append(copy.deepcopy(grid.available_pieces))
            Blockies.players_lt_colors = const.PIECE_LT_COLORS[:Blockies.num_players]
            grid.active_piece = Blockies.player_pieces_available[0][0]
            started = True

    screen.fill((0, 0, 0))
    total_height = begin_title.get_height() + begin_prompt.get_height()
    screen.blit(begin_title,
                ((const.SCREEN_SIZE/2) - begin_title.get_width() // 2,
                 begin_title.get_height()))

    screen.blit(begin_prompt,
                ((const.SCREEN_SIZE/2) - begin_prompt.get_width() // 2,
                 (const.SCREEN_SIZE/2) + 100 - total_height // 2))
    pygame.display.flip()               # Update display
    clock.tick(60)                      # Limit to 30 frames per second

while not done:
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # User clicked close
            quit(0)
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP]:
                grid.active_piece = grid.next_available_piece()
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                grid.active_piece = grid.previous_available_piece()
            elif pygame.key.get_pressed()[pygame.K_q]:
                quit(0)
            grid.active_piece.set_color(Blockies.players_lt_colors[Blockies.player_index])
            grid.active_piece.set_root_square(grid.square_from_pos(pygame.mouse.get_pos()))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid.update_active_piece(event.pos)
            clicked_square = grid.square_from_pos(event.pos)
            if grid.active_piece.is_legal:
                grid.active_piece.set_color_current()
                grid.set_square(clicked_square, grid.active_piece)
                if not turn_swap():
                    # Attempted turn_swap() but nobody can move!
                    set_final_scores()
                # turn_swap succeeded
                grid.update_active_piece(event.pos)
                new_square = clicked_square
                grid.display()
        elif event.type == pygame.MOUSEMOTION:
            if mouse_is_on_screen():
                if not grid.mouse_in_square(event.pos, new_square):
                    new_square = None
                    grid.update_active_piece(event.pos)
            else:
                pass
                # grid.hide_mouse_square()

    screen.fill((255, 255, 255))
    if Blockies.final_scores:
        score_title = small_font.render('FINAL SCORE', True, (128, 128, 128))
        total_height = score_title.get_height() + Blockies.final_scores.get_height()

        screen.blit(score_title,
            ((const.SCREEN_SIZE / 2) - score_title.get_width() // 2,
            (const.SCREEN_SIZE / 2) - total_height // 2))
        pygame.display.flip()  # Update display
        pygame.time.wait(500)
        screen.blit(Blockies.final_scores,
            ((const.SCREEN_SIZE / 2) - Blockies.final_scores.get_width() // 2,
            (const.SCREEN_SIZE / 2) + 60 - total_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
    else:
        for col_line_num in range(const.SQ_COLUMNS + 1):
            pygame.draw.line(screen,
                             const.GRID_LINE_COLOR,
                             ((col_line_num) * const.SQ_SIZE, 0),
                             ((col_line_num) * const.SQ_SIZE, const.SCREEN_SIZE))

        for row_line_num in range(const.SQ_COLUMNS + 1):
            pygame.draw.line(screen,
                             const.GRID_LINE_COLOR,
                             (0, row_line_num * const.SQ_SIZE),
                             (const.SCREEN_SIZE, row_line_num * const.SQ_SIZE))

        for col_sq in range(const.SQ_COLUMNS):
            for row_sq in range(const.SQ_COLUMNS):
                if grid._squares[col_sq][row_sq] is not None:
                    draw_square((col_sq, row_sq))

        if mouse_is_on_screen() and not grid.mouse_in_square(pygame.mouse.get_pos(), new_square):
            draw_piece(grid.active_piece)

    pygame.display.flip()               # Update display

    clock.tick(30)                      # Limit to 30 frames per second
