import unittest
from blockies import Blockies
import const
import copy

const.SCREEN_SIZE = 600
const.SQ_COLUMNS = 10
Blockies.num_players = 2
Blockies.players = const.PIECE_COLORS[:Blockies.num_players]


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
        piece.set_root_square((2, 2))
        self.assertEqual(piece.squares, [(2, 2)])

    def test_piece2_squares_taken(self):
        piece = Blockies.Piece('square', 2, 2, (1, 2), (100, 100, 100))
        expected_squares = [(1, 2), (2, 2), (1, 3), (2, 3)]
        for square in expected_squares:
            self.assertTrue(square in piece.squares)

    def test_find_corner_coordinates(self):
        piece = Blockies.Piece('rectangle', 3, 2, (2, 2), const.WHITE)
        expected_squares = [(2, 2), (2, 3), (4, 2), (4, 3)]
        self.assertEqual(piece.find_corner_coordinates(), expected_squares)

    def test_rotate_2_1_rect_clockwise(self):
        piece = Blockies.Piece('rectangle', 2, 1, (0, 0), const.WHITE)
        initial_squares = [(0, 0), (1, 0)]
        expected_squares = [(0, 0), (0, 1)]
        self.assertEqual(piece.squares, initial_squares)
        piece.rotate_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'rotated 2x1 rect does not occupy expected squares')

    def test_rotate_1_2_rect_clockwise(self):
        piece = Blockies.Piece('rectangle', 1, 2, (0, 0), const.WHITE)
        initial_squares = [(0, 0), (0, 1)]
        expected_squares = [(0, 0), (1, 0)]
        self.assertEqual(piece.squares, initial_squares)
        piece.rotate_clockwise()
        self.assertEqual(piece.squares, expected_squares, 'rotated 1x2 rect does not occupy expected squares')

    def test_rotate_3_2_rect_clockwise(self):
        piece = Blockies.Piece('rectangle', 3, 2, (0, 0), const.WHITE)
        initial_squares = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)]
        expected_squares = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]
        self.assertEqual(piece.squares, initial_squares)
        piece.rotate_clockwise()
        self.assertEqual(set(piece.squares), set(expected_squares), 'rotated 3x2 rect does not occupy expected squares')


class TestBlockiesGrid(unittest.TestCase):

    def make_empty_grid(self):
        return Blockies.Grid()

    def make_basic_grid(self):
        grid = Blockies.Grid()
        blue_squares = [(0, 0), (1, 1), (2, 2)]
        green_squares = [(9, 9), (8, 8), (7, 7)]
        for square in blue_squares:
            grid.set_square(square, Blockies.Piece('square', 1, 1, square, const.BLUE))
        for square in green_squares:
            grid.set_square(square, Blockies.Piece('square', 1, 1, square, const.GREEN))
        return grid

    def make_full_grid(self):
        grid = Blockies.Grid()
        squares = []
        for i in range(10):
            for j in range(10):
                squares.append((i, j))
        for square in squares:
            grid.set_square(square, Blockies.Piece('square', 1, 1, square, const.BLUE))
        return grid

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
            self.assertEqual(square, Blockies.Grid.square_from_pos(None, point),
                             'point in wrong square: {} on a {} square size grid'.format(
                                 point, const.SQ_SIZE
                             ))

    def test_grid_get_square(self):
        grid = self.make_basic_grid()
        self.assertIsNotNone(grid.get_square((0, 0)))
        self.assertIsNotNone(grid.get_square((7, 7)))

    def test_grid_get_square_empty(self):
        grid = self.make_basic_grid()
        self.assertIsNone(grid.get_square((5, 5)))
        self.assertIsNone(grid.get_square((0, 9)))

    def test_grid_get_square_off_grid(self):
        grid = self.make_basic_grid()
        self.assertIsNone(grid.get_square((-1, 9)))
        self.assertIsNone(grid.get_square((-1, 10)))
        self.assertIsNone(grid.get_square((0, 10)))

    def test_is_legal_position_false_same(self):
        grid = self.make_basic_grid()
        piece = self.make_square_at((1, 1))
        self.assertFalse(grid.is_legal_position(piece))

    def test_is_legal_position_false_up(self):
        grid = self.make_basic_grid()
        piece = self.make_square_at((2, 3))
        self.assertFalse(grid.is_legal_position(piece))

    def test_is_legal_position_false_down(self):
        grid = self.make_basic_grid()
        piece = self.make_square_at((8, 8))
        self.assertFalse(grid.is_legal_position(piece))

    def test_is_legal_position_false_left(self):
        grid = self.make_basic_grid()
        piece = self.make_square_at((9, 8))
        self.assertFalse(grid.is_legal_position(piece))

    def test_is_legal_position_false_right(self):
        grid = self.make_basic_grid()
        piece = self.make_square_at((6, 7))
        self.assertFalse(grid.is_legal_position(piece))

    def test_is_legal_position_first_move(self):
        grid = self.make_empty_grid()
        piece1 = self.make_square_at((0, 0))
        self.assertTrue(grid.is_legal_position(piece1))
        piece2 = self.make_square_at((0, 9))
        self.assertTrue(grid.is_legal_position(piece2))
        piece3 = self.make_square_at((9, 0))
        self.assertTrue(grid.is_legal_position(piece3))
        piece4 = self.make_square_at((9, 9))
        self.assertTrue(grid.is_legal_position(piece4))

    def test_is_legal_position_true_diagonal(self):
        grid = self.make_basic_grid()
        piece = self.make_square_at((3, 3))
        self.assertTrue(grid.is_legal_position(piece))

    def test_player_has_legal_move_false_full_grid(self):
        grid = self.make_full_grid()
        for player in range(Blockies.num_players):
            Blockies.player_pieces_available.append(copy.deepcopy(grid.available_pieces))
        self.assertFalse(grid.player_has_legal_move())

    def test_grid_print(self):
        grid = Blockies.Grid()
        from pprint import pprint
        pprint(grid.display())


# class TestBlockiesPiece(unittest.TestCase):
#
#     def test_construct_square(self):
#         square = Blockies.Piece('square', 4)
#         print(square.matrix)
#         self.assertEqual(len(square.matrix), 2)
#         self.assertEqual(len(square.matrix[0]), 2)
#         self.assertEqual(len(square.matrix[1]), 2)
#
#     def test_down_nodes(self):
#         square = Blockies.Piece('square', 4)
#         self.assertEqual(len(square._down_nodes(square.root_node)), 2)
#
#     def test_right_nodes(self):
#         square = Blockies.Piece('square', 4)
#         self.assertEqual(len(square._right_nodes(square.root_node)), 2)


if __name__ == '__main__':
    unittest.main()
