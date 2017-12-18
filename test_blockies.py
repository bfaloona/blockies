import unittest
from blockies import Blockies
import const


# const.SCREEN_SIZE = 600
# const.SQ_COLUMNS = 10
# Blockies.num_players = 2
# Blockies.players = const.PIECE_COLORS[:Blockies.num_players]


class TestBlockiesStatic(unittest.TestCase):

    def test_shift_coords_positive_xy(self):
        negative_coords = [(-1, -1),    (0, -1),    (-1, 0),    (0, 0)]
        expected_coords = [(0, 0),      (1, 0),     (0, 1),     (1, 1)]
        self.assertEqual(Blockies.shift_coords_positive(negative_coords), expected_coords)

    def test_shift_coords_positive_x(self):
        negative_coords = [(-100, 0),   (-50, 100),    (-100, 0),  (-50, 100)]
        expected_coords = [(0, 0),      (50, 100),     (0, 0),     (50, 100)]
        self.assertEqual(Blockies.shift_coords_positive(negative_coords), expected_coords)

    def test_shift_coords_positive_y(self):
        negative_coords = [(100, -75),    (150, -60),    (100, -75),   (150, -60)]
        expected_coords = [(100, 0),      (150, 15),     (100, 0),     (150, 15)]
        self.assertEqual(Blockies.shift_coords_positive(negative_coords), expected_coords)


class TestBlockiesPiece(unittest.TestCase):

    def test_piece2_construct_square_2x(self):
        piece = Blockies.Piece('square', 2, 2, (0, 0), (100, 100, 100))
        self.assertEqual(len(piece.matrix), 2)
        self.assertEqual(len(piece.matrix[0]), 2)
        self.assertEqual(len(piece.matrix[1]), 2)

    def test_piece2_construct_square_1x(self):
        piece = Blockies.Piece('square', 1, 1, (0, 0), const.WHITE)
        self.assertEqual(len(piece.matrix), 1)
        self.assertEqual(len(piece.matrix[0]), 1)

    def test_piece2_update_square_1x(self):
        piece = Blockies.Piece('square', 1, 1, (0, 0), const.WHITE)
        piece.move_to((2, 2))
        self.assertEqual(piece.squares, [(2, 2)])

    def test_piece2_squares_taken(self):
        piece = Blockies.Piece('square', 2, 2, (1, 2), const.WHITE)
        expected_squares = [(1, 2), (2, 2), (1, 3), (2, 3)]
        self.assertEqual(set(piece.squares), set(expected_squares))

    def test_find_corner_coordinates(self):
        piece = Blockies.Piece('rectangle', 3, 2, (2, 2), const.WHITE)
        expected_squares = [(2, 2), (2, 3), (4, 2), (4, 3)]
        self.assertEqual(set(piece._get_corners_rectangle()), set(expected_squares))

    def test_rotate_2_1_squares_clockwise(self):
        piece = Blockies.Piece('rectangle', 2, 1, (2, 4), const.WHITE)
        initial_squares = [(2, 4), (3, 4)]
        expected_squares = [(2, 4), (2, 5)]
        self.assertEqual(set(piece.squares), set(initial_squares))
        piece.rotate_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'rotated 2x1 rect does not occupy expected squares')

    def test_rotate_2_1_points_clockwise(self):
        piece = Blockies.Piece('rectangle', 2, 1, (2, 4), const.WHITE)
        initial_points = [(163, 323), (163, 397), (317, 397), (317, 323)]
        expected_points = [(163, 323), (163, 477), (237, 477), (237, 323)]
        self.assertEqual(set(piece.points), set(initial_points))
        piece.rotate_clockwise()
        self.assertEqual(set(piece.points), set(expected_points), 'rotated 2x1 rect does not occupy expected squares')

    def test_rotate_2_1_rect_counter_clockwise(self):
        piece = Blockies.Piece('rectangle', 2, 1, (2, 4), const.WHITE)
        initial_squares = [(2, 4), (3, 4)]
        expected_squares = [(2, 4), (2, 3)]
        self.assertEqual(set(piece.squares), set(initial_squares))
        piece.rotate_counter_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'counter rotated 2x1 rect does not occupy expected squares')

    def test_rotate_1_2_rect_counter_clockwise(self):
        piece = Blockies.Piece('rectangle', 1, 2, (2, 4), const.WHITE)
        initial_squares = [(2, 4), (2, 5)]
        expected_squares = [(2, 4), (3, 4)]
        self.assertEqual(set(piece.squares), set(initial_squares))
        piece.rotate_counter_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'counter rotated 2x1 rect does not occupy expected squares')

    def test_rotate_2_1_rect_counter_clockwise_twice(self):
        piece = Blockies.Piece('rectangle', 2, 1, (2, 4), const.WHITE)
        initial_squares = [(2, 4), (3, 4)]
        expected_squares = [(2, 4), (1, 4)]
        self.assertEqual(set(piece.squares), set(initial_squares))
        piece.rotate_counter_clockwise()
        piece.rotate_counter_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'twice counter rotated 2x1 rect does not occupy expected squares')

    def test_rotate_1_2_rect_clockwise(self):
        piece = Blockies.Piece('rectangle', 1, 2, (3, 6), const.WHITE)
        initial_squares = [(3, 6), (3, 7)]
        expected_squares = [(2, 6), (3, 6)]
        self.assertEqual(set(piece.squares), set(initial_squares))
        piece.rotate_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'rotated 1x2 rect does not occupy expected squares')

    def test_rotate_3_2_rect_clockwise(self):
        piece = Blockies.Piece('rectangle', 3, 2, (2, 2), const.WHITE)
        initial_squares = [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (4, 3)]
        expected_squares = [(1, 2), (2, 2), (1, 3), (2, 3), (1, 4), (2, 4)]
        self.assertEqual(set(piece.squares), set(initial_squares))
        piece.rotate_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'rotated 3x2 rect does not occupy expected squares')

    def test_rotate_3_2_rect_clockwise_twice(self):
        piece = Blockies.Piece('rectangle', 3, 2, (2, 2), const.WHITE)
        initial_squares = [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (4, 3)]
        expected_squares = [(0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
        self.assertEqual(set(piece.squares), set(initial_squares))
        piece.rotate_clockwise()
        piece.rotate_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'twice rotated 3x2 rect does not occupy expected squares')

    def test_find_corner_squares_3x3(self):

        piece = Blockies.Piece('square', 3, 3, (3, 3), const.WHITE)
        expected_squares = [
            (3, 3), (4, 3), (5, 3),
            (3, 4), (4, 4), (5, 4),
            (3, 5), (4, 5), (5, 5)
        ]
        expected_corners = [(3, 3), (3, 5), (5, 5), (5, 3)]
        self.assertEqual(piece.squares, expected_squares)
        self.assertEqual(Blockies.find_corners(piece.squares), expected_corners)

    def test_unique_from_list(self):
        ordered_list = [1, "Hello", (3, 3), "Hello", (1, 1), (3, 3)]
        self.assertEqual(Blockies.unique_from_list(ordered_list), [1, "Hello", (3, 3), (1, 1)])


class TestBlockiesGrid(unittest.TestCase):

    def make_empty_game_grid(self):
        return Blockies.Game(2)

    def make_basic_game_grid(self):
        game = Blockies.Game(2)
        blue_squares = [(0, 0), (1, 1), (2, 2)]
        green_squares = [(9, 9), (8, 8), (7, 7)]
        for square in blue_squares:
            game.grid.set_square(square, Blockies.Piece('square', 1, 1, square, const.BLUE))
        for square in green_squares:
            game.grid.set_square(square, Blockies.Piece('square', 1, 1, square, const.GREEN))
        return game

    def make_game_full_grid(self):
        game = Blockies.Game(1)
        squares = []
        for i in range(const.SQ_COLUMNS):
            for j in range(const.SQ_COLUMNS):
                squares.append((i, j))
        for square in squares:
            game.grid.set_square(square, Blockies.Piece('square', 1, 1, square, const.BLUE))
        return game

    def make_square_at(self, pos):
        return Blockies.Piece('square', 1, 1, pos, const.WHITE)

    def test_grid(self):
        grid = Blockies.Grid()

        self.assertEqual(len(grid._squares), 10)
        self.assertEqual(len(grid._squares[0]), 10)

    def test_grid_set_squares(self):
        grid = Blockies.Grid()
        square = (0, 9)
        grid.set_square(square, Blockies.Piece('square', 1, 1, square, const.BLUE))
        self.assertIsNotNone(grid._squares[0][9])
        self.assertIsNone(grid._squares[1][8])

    def test_grid_set_squares_3x_piece(self):
        grid = Blockies.Grid()
        square = (1, 2)
        grid.set_square(square, Blockies.Piece('square', 3, 1, square, const.BLUE))
        self.assertIsNotNone(grid._squares[1][2])
        self.assertIsNotNone(grid._squares[2][2])
        self.assertIsNotNone(grid._squares[3][2])
        self.assertIsNone(grid._squares[4][2])
        self.assertIsNone(grid._squares[5][2])
        self.assertIsNone(grid._squares[0][2])

    def test_square_from_pos(self):
        # init constants with 2 person game
        Blockies.Game(2)
        test_values = {
            (0, 0): (0, 0),
            (0, 0): (-57, -57),
            (0, 0): (-57, 57),
            (0, 0): (3, 57),
            (0, 0): (57, 57),
            (0, 0): (57, 3),
            (1, 0): (83, 57),
            (2, 3): (163, 240),
        }
        for square, point in test_values.items():
            self.assertEqual(square, Blockies.square_from_pos(point),
                             'point in wrong square: {} on a {} square size grid'.format(
                                 point, const.SQ_SIZE
                             ))

    def test_grid_get_square(self):
        grid = self.make_basic_game_grid().grid
        self.assertIsNotNone(grid.get_square((0, 0)))
        self.assertIsNotNone(grid.get_square((7, 7)))

    def test_grid_get_square_empty(self):
        grid = self.make_basic_game_grid().grid
        self.assertIsNone(grid.get_square((5, 5)))
        self.assertIsNone(grid.get_square((0, 9)))

    def test_grid_get_square_off_grid(self):
        grid = self.make_basic_game_grid().grid
        self.assertIsNone(grid.get_square((-1, 9)))
        self.assertIsNone(grid.get_square((-1, 10)))
        self.assertIsNone(grid.get_square((0, 10)))

    def test_is_legal_position_false_same(self):
        game = self.make_basic_game_grid()
        piece = self.make_square_at((1, 1))
        self.assertFalse(game.is_legal_position(piece))

    def test_is_legal_position_false_up(self):
        game = self.make_basic_game_grid()
        piece = self.make_square_at((2, 3))
        self.assertFalse(game.is_legal_position(piece))

    def test_is_legal_position_false_down(self):
        game = self.make_basic_game_grid()
        piece = self.make_square_at((8, 8))
        self.assertFalse(game.is_legal_position(piece))

    def test_is_legal_position_false_left(self):
        game = self.make_basic_game_grid()
        piece = self.make_square_at((9, 8))
        self.assertFalse(game.is_legal_position(piece))

    def test_is_legal_position_false_right(self):
        game = self.make_basic_game_grid()
        piece = self.make_square_at((6, 7))
        self.assertFalse(game.is_legal_position(piece))

    def test_is_legal_position_first_move(self):
        game = self.make_empty_game_grid()
        piece1 = self.make_square_at((0, 0))
        self.assertTrue(game.is_legal_position(piece1))
        piece2 = self.make_square_at((0, 9))
        self.assertTrue(game.is_legal_position(piece2))
        piece3 = self.make_square_at((9, 0))
        self.assertTrue(game.is_legal_position(piece3))
        piece4 = self.make_square_at((9, 9))
        self.assertTrue(game.is_legal_position(piece4))

    def test_is_legal_position_true_diagonal(self):
        game = self.make_basic_game_grid()
        piece = self.make_square_at((3, 3))
        self.assertTrue(game.is_legal_position(piece))

    def test_player_has_legal_move_false_full_grid(self):
        game = self.make_game_full_grid()
        self.assertFalse(game.player_has_legal_move())

    def test_grid_print(self):
        grid = Blockies.Grid()
        from pprint import pprint
        pprint(grid._display())


if __name__ == '__main__':
    unittest.main()
