import const
import math
import operator
import copy


class Blockies:

    @staticmethod
    def unique_from_list(ordered_list):
        seen = set()
        seen_add = seen.add
        return [x for x in ordered_list if not (x in seen or seen_add(x))]

    @staticmethod
    def pos_from_square(square):
        return square[0] * const.SQ_SIZE, square[1] * const.SQ_SIZE

    @staticmethod
    def lowest_bounding_square(squares):
        sorted_by_x = sorted(squares[:], key=operator.itemgetter(0))
        sorted_by_y = sorted(squares[:], key=operator.itemgetter(1))
        return sorted_by_x[0][0], sorted_by_y[0][1]

    @staticmethod
    def rotate_coords(coords, axis_coord):
        new_coords = []
        for coord in coords:
            x, y = coord
            new_x = axis_coord[1] - y + axis_coord[0]
            new_y = x - axis_coord[0] + axis_coord[1]
            new_coords.append((new_x, new_y))
        return new_coords

    @staticmethod
    def find_corners(squares):
        squares_by_x = sorted(squares, key=operator.itemgetter(0))
        squares_by_y = sorted(squares, key=operator.itemgetter(1))
        low_x_squares = [x_square for x_square in squares if x_square[0] == squares_by_x[0][0]]
        low_y_squares = [y_square for y_square in squares if y_square[1] == squares_by_y[0][1]]
        high_x_squares = [x_square for x_square in squares if x_square[0] == squares_by_x[-1][0]]
        high_y_squares = [y_square for y_square in squares if y_square[1] == squares_by_y[-1][1]]

        return Blockies.unique_from_list([
            low_x_squares[0], low_x_squares[-1],
            high_y_squares[0], high_y_squares[-1],
            high_x_squares[0], high_x_squares[-1],
            low_y_squares[0], low_y_squares[-1]
        ])

    @staticmethod
    def shift_coords_positive(coords):
        new_coords = coords
        # find lowest coord of bounding rectangle
        lowest_x, lowest_y = Blockies.lowest_bounding_square(coords)
        # if coord includes negative numbers
        if lowest_x < 0:
            # adjust x coord to remove negative values
            new_coords = [(x + abs(lowest_x), y) for (x, y) in new_coords]
        if lowest_y < 0:
            # adjust y coord to remove negative values
            new_coords = [(x, y + abs(lowest_y)) for (x, y) in new_coords]
        return new_coords

    @staticmethod
    def square_from_pos(pos):
        col = int(pos[0] / const.SQ_SIZE)
        row = int(pos[1] / const.SQ_SIZE)
        return col, row

    @staticmethod
    def color_char(color):
        """
        @type color: tuple, None
        @param color: RGB tuple
        """
        if color == const.BLUE:
            return 'B'
        elif color == const.GREEN:
            return 'G'
        elif color == const.YELLOW:
            return 'Y'
        elif color == const.RED:
            return 'R'
        elif color is None:
            return '.'
        else:
            return '?'

    @staticmethod
    def is_color(square, color):
        return True if square == color else False

    @staticmethod
    def is_off_screen(square):
        col_num, row_num = square
        if col_num < 0 or col_num > (const.SQ_COLUMNS - 1):
            return True
        if row_num < 0 or row_num > (const.SQ_COLUMNS - 1):
            return True
        return False

    @staticmethod
    def is_grid_corner(square):
        edge = const.SQ_COLUMNS - 1
        return True if square in [(0, 0), (0, edge), (edge, edge), (edge, 0)] else False

    @staticmethod
    def mouse_in_square(mouse_pos, square):
        if Blockies.square_from_pos(mouse_pos) == square:
            return True
        else:
            return False

    @staticmethod
    def shift_coord(coord, relative_coordinate):
        x = coord[0] + relative_coordinate[0]
        y = coord[1] + relative_coordinate[1]
        return x, y

    class Game:

        def __init__(self, num_players):

            self.player_index = 0
            self.players = []
            self.players_lt_colors = []
            self.player_pieces_available = []
            self.done = False
            self.final_scores = None
            self.num_players = num_players
            if self.num_players == 1:
                const.SQ_COLUMNS = 7
            elif self.num_players == 2:
                const.SQ_COLUMNS = 10
            elif self.num_players == 3:
                const.SQ_COLUMNS = 12
            elif self.num_players == 4:
                const.SQ_COLUMNS = 14
            const.SQ_SIZE = int(const.SCREEN_SIZE / const.SQ_COLUMNS)
            self.available_pieces = [
                Blockies.Piece('square', 1, 1),
                Blockies.Piece('rectangle', 2, 1),
                Blockies.Piece('square', 2, 2),
                Blockies.Piece('rectangle', 3, 1),
                Blockies.Piece('rectangle', 4, 1),
                Blockies.Piece('rectangle', 5, 1),
                Blockies.Piece('L', 2, 2),
                Blockies.Piece('X', 3, 3),
                Blockies.Piece('T', 3, 3),
                Blockies.Piece('T', 3, 2),
            ]
            self.grid = Blockies.Grid()
            self.players = const.PIECE_COLORS[:self.num_players]
            self.players_lt_colors = const.PIECE_LT_COLORS[:self.num_players]
            for player in range(self.num_players):
                self.player_pieces_available.append(copy.deepcopy(self.available_pieces))
            self.active_piece_index = 0
            self.active_piece = self.player_pieces_available[self.player_index][self.active_piece_index]

        def next_available_piece(self):
            if self.active_piece_index + 1 >= len(self.player_pieces_available[self.player_index]):
                self.active_piece_index = 0
            else:
                self.active_piece_index += 1
            return self.player_pieces_available[self.player_index][self.active_piece_index]

        def previous_available_piece(self):
            if self.active_piece_index - 1 <= 0:
                self.active_piece_index = len(self.player_pieces_available[self.player_index]) - 1
            else:
                self.active_piece_index -= 1
            return self.player_pieces_available[self.player_index][self.active_piece_index]

        def update_active_piece(self, pos):
            new_square = Blockies.square_from_pos(pos)
            if new_square != self.active_piece.root_square:
                self.active_piece.move_to(new_square)
            if not self.is_legal_position(self.active_piece):
                color = const.SQ_COLOR_ILLEGAL
            else:
                color = self.players_lt_colors[self.player_index]
            self.active_piece.set_color(color)

        def adjacent_are_free(self, square):
            for coord in [(0, -1), (0, 1), (-1, 0), (1, 0)]:        # UP, DOWN, LEFT, RIGHT
                if Blockies.is_color(self.grid.get_relative_square(square, coord), self.players[self.player_index]):
                    return False
            # all adjacent squares are free
            return True

        def is_connected_diagonally(self, square):
            for coord in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:        # UP LEFT, UP RIGHT, DOWN LEFT, DOWN RIGHT
                if Blockies.is_color(self.grid.get_relative_square(square, coord), self.players[self.player_index]):
                    return True
            # not connected diagonally to another square of the same color
            return False

        def square_count(self):
            count = 0
            for col in range(const.SQ_COLUMNS):
                for row in range(const.SQ_COLUMNS):
                    if self.grid.get_square((col, row)) == self.players[self.player_index]:
                        count += 1
            return count

        def is_legal_position(self, piece):
            piece.is_legal = False
            for square in piece.squares:
                if not self.grid.is_available_square(square):
                    piece.is_legal = False
                    return piece.is_legal
            if self.square_count() < 1:
                for corner_square in piece.corner_squares:
                    if Blockies.is_grid_corner(corner_square):
                        piece.is_legal = True
                        return piece.is_legal
            else:
                for piece_square in piece.squares:
                    if not self.adjacent_are_free(piece_square):
                        piece.is_legal = False
                        return piece.is_legal
                for corner_square in piece.corner_squares:
                    if self.is_connected_diagonally(corner_square):
                        piece.is_legal = True
                        return piece.is_legal
            return piece.is_legal

        def player_has_legal_move(self):
            # FOR THE CURRENT PLAYER
            current_player_index = self.player_index
            # FOR EACH REMAINING PIECE
            for piece in self.player_pieces_available[current_player_index]:
                for rotation in range(3):    # additional rotation states
                    piece.rotate_clockwise()
                    # FOR EACH const.SQUARE ACROSS
                    for x in range(const.SQ_COLUMNS):
                        # FOR EACH const.SQUARE DOWN
                        for y in range(const.SQ_COLUMNS):
                            # CHECK IF MOVE IS LEGAL
                            piece.move_to((x, y))
                            if self.is_legal_position(piece):
                                return True
            # PLAYER CAN'T MOVE
            return False

    class Piece:
        def __init__(self, shape, x_squares, y_squares, root_square=(0, 0), color=const.SQ_COLOR_ILLEGAL):
            self.shape = shape
            self.color = color
            self.root_square = root_square
            self.rotation_square = root_square
            self.x_squares = x_squares
            self.y_squares = y_squares
            self.points = []
            self.matrix = [[]]
            self.squares = []
            self.corner_squares = []
            self.is_legal = False
            if self.is_rectangle():
                self._initialize_matrix_rect()
                if self.root_square and isinstance(self.root_square, (tuple, list)) and len(self.root_square) == 2:
                    self.hydrate()
                else:
                    raise ValueError('`root_square` parameter must be coordinate (tuple or list)')
            elif self.shape == "T":
                if self.y_squares == 2:
                    self.matrix = [['*', None], ['*', '*'], ['*', None]]
                elif self.y_squares == 3:
                    self.matrix = [['*', None, None], ['*', '*', '*'], ['*', None, None]]
                self.hydrate()
            elif self.shape == "X":
                self.matrix = [[None, '*', None], ['*', '*', '*'], [None, '*', None]]
                self.hydrate()
            elif self.shape == "L":
                self.matrix = [['*', '*'], [None, '*']]
                self.hydrate()
            else:
                raise ValueError('Only type `square` is currently supported')

        def set_color(self, color):
            self.color = color

        def move_to(self, new_root_square):
            shift_x = new_root_square[0] - self.root_square[0]
            shift_y = new_root_square[1] - self.root_square[1]
            self.root_square = new_root_square
            new_squares = []
            for square in self.squares:
                new_squares.append((square[0] + shift_x, square[1] + shift_y))
            self.squares = new_squares
            new_points = []
            for point in self.points:
                new_points.append(
                    (point[0] + (shift_x * const.SQ_SIZE),
                     point[1] + (shift_y * const.SQ_SIZE)))
            self.points = new_points
            self.corner_squares = self._get_corners()
            self.rotation_square = self._get_rotation_square()

        def hydrate(self):
            self._populate_points()
            self._populate_squares()

        def is_rectangle(self):
            return True if self.shape in ['square', 'rectangle'] else False

        def rotate_clockwise(self):
            self.x_squares, self.y_squares = self.y_squares, self.x_squares
            new_squares = Blockies.rotate_coords(self.squares, self.rotation_square)
            self.squares = Blockies.shift_coords_positive(new_squares)
            self.root_square = Blockies.lowest_bounding_square(self.squares)
            self.corner_squares = self._get_corners()
            self.points = Blockies.rotate_coords(self.points, Blockies.pos_from_square(self.root_square))
            self._repopulate_matrix()

        def rotate_counter_clockwise(self):
            if self.is_rectangle():
                self.x_squares, self.y_squares = self.y_squares, self.x_squares
                new_squares = []
                for square in self.squares:
                    x, y = square
                    new_x = self.rotation_square[0] + (y - self.rotation_square[1])
                    new_y = self.rotation_square[1] - (x - self.rotation_square[0])
                    new_squares.append((new_x, new_y))
                self.squares = Blockies.shift_coords_positive(new_squares)
                self.root_square = Blockies.lowest_bounding_square(self.squares)
                self.corner_squares = self._get_corners()
                self._get_rect_points()
                self._repopulate_matrix()
            else:
                raise RuntimeError('Not implemented')

        def _populate_points(self):
            if self.shape == 'T':
                self._populate_t_points()
            elif self.shape == 'X':
                self._populate_x_points()
            elif self.shape == 'L':
                self._populate_l_points()
            elif self.is_rectangle():
                self.points = self._get_rect_points()

        def _get_rect_points(self):
            p1 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p2 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (self.y_squares * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p3 = (
                int((self.root_square[0] * const.SQ_SIZE) + (self.x_squares * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (self.y_squares * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p4 = (
                int((self.root_square[0] * const.SQ_SIZE) + (self.x_squares * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            return [p1, p2, p3, p4]

        # def _repopulate_polygon_points(self):
            # ignore padding!
            #  start with root square
            # find next border square
            # set point of current square
            # continue with next border square
            # if not root square and square[1] == root_square[1]
            #   we're done

        # def _get_next_border_square(self, start_square):
        #     self.get_next_vector_square()
        #
        # def _get_next_vector_square(self, start_square, vector_coordinate=(0, 0)):
        #     # down
        #     next_square = tuple(map(operator.add, start_square, vector_coordinate))
        #     if next in self.squares:
        #         return self._get_next_vector_square(next_square, vector_coordinate)
        #     else:
        #         return next_square

        def _populate_x_points(self):
            p1 = (
                int(((self.root_square[0] + 1) * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p2 = (
                int((self.root_square[0] * const.SQ_SIZE) + (1 * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (1 * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p3 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (1 * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p4 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (2 * const.SQ_SIZE)),
            )
            p5 = (
                int((self.root_square[0] * const.SQ_SIZE) + (1 * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (2 * const.SQ_SIZE)),
            )
            p6 = (
                int((self.root_square[0] * const.SQ_SIZE) + (1 * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (3 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p7 = (
                int((self.root_square[0] * const.SQ_SIZE) + (2 * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (3 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p8 = (
                int((self.root_square[0] * const.SQ_SIZE) + (2 * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (2 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p9 = (
                int((self.root_square[0] * const.SQ_SIZE) + (3 * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (2 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p10 = (
                int((self.root_square[0] * const.SQ_SIZE) + (3 * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (1 * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p11 = (
                int((self.root_square[0] * const.SQ_SIZE) + (2 * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (1 * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p12 = (
                int((self.root_square[0] * const.SQ_SIZE) + (2 * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            self.points = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]

        def _populate_l_points(self):
            p1 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p2 = Blockies.shift_coord(p1, (0, (2 * const.SQ_SIZE) - const.SQ_PADDING * 2))

            p3 = Blockies.shift_coord(p2, ((2 * const.SQ_SIZE) - const.SQ_PADDING * 2, 0))

            p4 = Blockies.shift_coord(p3, (0, (-1 * const.SQ_SIZE) + const.SQ_PADDING * 2))

            p5 = Blockies.shift_coord(p4, ((-1 * const.SQ_SIZE), 0))

            p6 = Blockies.shift_coord(p5, (0, (-1 * const.SQ_SIZE)))

            self.points = [p1, p2, p3, p4, p5, p6]

        def _populate_t_points(self):
            p1 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p2 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p3 = (
                int(((self.root_square[0] + 1) * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            if self.y_squares == 3:
                p4 = (
                    int(((self.root_square[0] + 1) * const.SQ_SIZE) + const.SQ_PADDING),
                    int(((self.root_square[1] + 2) * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
                )
                p5 = (
                    int(((self.root_square[0] + 2) * const.SQ_SIZE) - const.SQ_PADDING),
                    int(((self.root_square[1] + 2) * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
                )
            elif self.y_squares == 2:
                p4 = (
                    int(((self.root_square[0] + 1) * const.SQ_SIZE) + const.SQ_PADDING),
                    int(((self.root_square[1] + 1) * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
                )
                p5 = (
                    int(((self.root_square[0] + 2) * const.SQ_SIZE) - const.SQ_PADDING),
                    int(((self.root_square[1] + 1) * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
                )

            p6 = (
                int(((self.root_square[0] + 2) * const.SQ_SIZE) - const.SQ_PADDING),
                int(((self.root_square[1]) * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p7 = (
                int(((self.root_square[0] + 3) * const.SQ_SIZE) - const.SQ_PADDING),
                int(((self.root_square[1]) * const.SQ_SIZE) + (1 * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p8 = (
                int(((self.root_square[0] + 3) * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            self.points = [p1, p2, p3, p4, p5, p6, p7, p8]

        def _initialize_matrix_rect(self):
            self.matrix = [[]]
            for y in range(self.y_squares):
                for x in range(self.x_squares):
                    if len(self.matrix) < x + 1:
                        self.matrix.append([])
                    self.matrix[x].append('*')

        def _repopulate_matrix(self):
            # Use squares to populate matrix
            # ==============================
            # for each square in bounding rectangle
            # populate matrix with * if square is populated
            self.matrix = [[]]
            for y in range(self.y_squares):
                for x in range(self.x_squares):
                    if len(self.matrix) < x + 1:
                        self.matrix.append([])
                    if (self.root_square[0] + x, self.root_square[1] + y) in self.squares:
                        self.matrix[x].append('*')

        def _populate_squares(self):
            new_squares = []
            for row_num in range(self.y_squares):
                for col_num in range(self.x_squares):
                    if len(self.matrix) > col_num:
                        if len(self.matrix[col_num]) > row_num:
                            if self.matrix[col_num][row_num]:
                                x = col_num + self.root_square[0]
                                y = row_num + self.root_square[1]
                                square = (x, y)
                                new_squares.append(square)
            self.squares = new_squares
            self.corner_squares = self._get_corners()

        def _get_rotation_square(self):
            middle_x = self.root_square[0] + math.ceil(self.x_squares / 2) - 1
            middle_y = self.root_square[1] + math.ceil(self.y_squares / 2) - 1
            return middle_x, middle_y

        def _get_corners(self):
            return Blockies.find_corners(self.squares)
            # if self.is_rectangle():
            #     return self._get_corners_rectangle()
            # else:
            #     return self._get_corners_polygon()

        # def _get_corners_polygon(self):
        #     if self.shape == "T":
        #         root_x = self.root_square[0]
        #         root_y = self.root_square[1]
        #         bottom = (root_x + 1, root_y + self.y_squares - 1)
        #         top_right = (root_x + self.x_squares - 1, root_y)
        #         return [self.root_square, bottom, top_right]
        #     else:
        #         raise RuntimeError('Not Implemented')

        def _get_corners_rectangle(self):
            root_x = self.root_square[0]
            root_y = self.root_square[1]
            bottom_left = (root_x, self.y_squares + root_y - 1)
            top_right = (self.x_squares + root_x - 1, root_y)
            bottom_right = (self.x_squares + root_x - 1, self.y_squares + root_y - 1)
            return [self.root_square, bottom_left, bottom_right, top_right]

        def _display(self):
            print('   0  1')
            for row_num in range(len(self.matrix[0])):
                row = '{}: '.format(row_num)
                for col_num in range(len(self.matrix)):
                    row += ('*  ' if self.matrix[col_num][row_num] is not None else '   ')
                print('{}'.format(row))
            print('\n')

    class Grid:

        def __init__(self):
            self._squares = [[None for i in range(const.SQ_COLUMNS)] for x in range(const.SQ_COLUMNS)]

        def set_square(self, square, piece):
            piece.move_to(square)
            for col_num, row_num in piece.squares:
                # print('Set square: [{}][{}] to {}'.format(col_num, row_num, piece.color))
                self._squares[col_num][row_num] = piece.color

        def get_square(self, square):
            if Blockies.is_off_screen(square):
                return None
            col_num, row_num = square
            return self._squares[col_num][row_num]

        def is_available_square(self, square):
            if self.is_taken(square) or Blockies.is_off_screen(square):
                return False
            else:
                return True

        def is_taken(self, square):
            return bool(self.get_square(square))

        def get_relative_square(self, square, relative_coordinate):
            x = square[0] + relative_coordinate[0]
            y = square[1] + relative_coordinate[1]
            return self.get_square((x, y))

        def _display(self):
            col_header = ' ' * (len(str(const.SQ_COLUMNS)))
            for i in range(const.SQ_COLUMNS):
                col_header += ' {}{}'.format(' ' * (3 - len(str(const.SQ_COLUMNS))), i)
            print(col_header)
            for row_num in range(const.SQ_COLUMNS):
                row = '{}: {}'.format(row_num, ' ' * (len(str(const.SQ_COLUMNS)) - len(str(row_num))))
                for col_num in range(const.SQ_COLUMNS):
                    row += str(Blockies.color_char(self._squares[col_num][row_num])) + '  '
                print('{}'.format(row))
            print('\n')
