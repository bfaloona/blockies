import const
import operator


class Blockies:

    player_index = 0
    num_players = 0
    players = []
    players_lt_colors = []
    player_pieces_available = []

    class Piece:
        def __init__(self, shape, x_squares, y_squares, root_square, color):
            self.shape = shape
            self.color = color
            self.root_square = root_square
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
            else:
                raise ValueError('Only type `square` is currently supported')

        def set_color(self, color):
            self.color = color

        def set_color_current(self):
            self.color = Blockies.players[Blockies.player_index]

        def move_to(self, new_root_square):
            self.root_square = new_root_square
            self.hydrate()

        def hydrate(self):
            if self.is_rectangle():
                self._populate_rect_points()
            else:
                raise RuntimeError('Not implemented')
            self._populate_squares()

        def is_rectangle(self):
            return True if self.shape in ['square', 'rectangle'] else False

        def lowest_bounding_square(self, squares):
            sorted_by_x = sorted(squares[:], key=operator.itemgetter(0))
            sorted_by_y = sorted(squares[:], key=operator.itemgetter(1))
            return sorted_by_x[0][0], sorted_by_y[0][1]

        def rotate_clockwise(self):
            if self.is_rectangle():
                self.x_squares, self.y_squares = self.y_squares, self.x_squares
                new_squares = []
                for square in self.squares:
                    x, y = square
                    new_x = self.root_square[1] - y + self.root_square[0]
                    new_y = x - self.root_square[0] + self.root_square[1]
                    new_squares.append((new_x, new_y))
                self.squares = self._shift_squares_positive(new_squares)
                self.root_square = self.lowest_bounding_square(self.squares)
                self.corner_squares = self._get_corners()
                self._populate_rect_points()
                self._repopulate_matrix()
            else:
                raise RuntimeError('Not implemented')

        def _shift_squares_positive(self, squares):
            squares_copy = squares
            # find lowest square of bounding rectangle
            lowest_x, lowest_y = self.lowest_bounding_square(squares_copy)
            # if square includes negative numbers
            if lowest_x < 0:
                # adjust x squares to remove negative values
                squares_copy = [(x - lowest_x, y) for (x, y) in squares_copy]
            if lowest_y < 0:
                # adjust y squares to remove negative values
                squares_copy = [(y, y - lowest_y) for (x, y) in squares_copy]
            return squares_copy

        def _populate_rect_points(self):
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
            self.points = [p1, p2, p3, p4]

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
            for row_num in range(len(self.matrix[0])):
                for col_num in range(len(self.matrix)):
                    if self.matrix[col_num][row_num] is not None:
                        x = col_num + self.root_square[0]
                        y = row_num + self.root_square[1]
                        square = (x, y)
                        new_squares.append(square)
            self.squares = new_squares
            self.corner_squares = self._get_corners()

        def _get_corners(self):
            if self.is_rectangle():
                return self._get_corners_rectangle()
            else:
                return self._get_corners_polygon()

        def _get_corners_polygon(self):
            raise RuntimeError('Not Implemented')

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
            self.available_pieces = [
                Blockies.Piece('square', 1, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 2, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('square', 2, 2, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 3, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('square', 3, 2, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 4, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 5, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 6, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
            ]
            self.active_piece_index = 0

        def next_available_piece(self):
            if self.active_piece_index + 1 >= len(Blockies.player_pieces_available[Blockies.player_index]):
                self.active_piece_index = 0
            else:
                self.active_piece_index += 1
            return Blockies.player_pieces_available[Blockies.player_index][self.active_piece_index]

        def previous_available_piece(self):
            if self.active_piece_index - 1 <= 0:
                self.active_piece_index = len(Blockies.player_pieces_available[Blockies.player_index]) - 1
            else:
                self.active_piece_index -= 1
            return Blockies.player_pieces_available[Blockies.player_index][self.active_piece_index]

        def square_count(self):
            count = 0
            for col in range(const.SQ_COLUMNS):
                for row in range(const.SQ_COLUMNS):
                    if self._squares[col][row] == Blockies.players[Blockies.player_index]:
                        count += 1
            return count

        def per_taken_square(self, function, params):
            for col in range(const.SQ_COLUMNS):
                for row in range(const.SQ_COLUMNS):
                    if self._squares[col][row] is not None:
                        function(col, row, *params)

        def set_square(self, square, piece):
            piece.move_to(square)
            for col_num, row_num in piece.squares:
                # print('Set square: [{}][{}] to {}'.format(col_num, row_num, piece.color))
                self._squares[col_num][row_num] = piece.color

        def is_off_screen(self, square):
            col_num, row_num = square
            if col_num < 0 or col_num > (const.SQ_COLUMNS - 1):
                return True
            if row_num < 0 or row_num > (const.SQ_COLUMNS - 1):
                return True
            return False

        def get_square(self, square):
            if self.is_off_screen(square):
                return None
            col_num, row_num = square
            return self._squares[col_num][row_num]

        # def add_square(self, square, color):
        #     self.set_square(square, color)
        #     self.display()

        def square_from_pos(self, pos):
            col = int(pos[0] / const.SQ_SIZE)
            row = int(pos[1] / const.SQ_SIZE)
            return (col, row)

        def is_legal_position(self, piece):
            piece.is_legal = False
            for piece_square in piece.squares:
                if not self.is_available_square(piece_square):
                    piece.is_legal = False
                    return piece.is_legal
            if self.square_count() < 1:
                for corner_square in piece.corner_squares:
                    if self.is_grid_corner(corner_square):
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

        def is_available_square(self, square):
            if self.is_taken(square) or self.is_off_screen(square):
                return False
            else:
                return True

        def is_grid_corner(self, square):
            edge = const.SQ_COLUMNS - 1
            return True if square in [(0, 0), (0, edge), (edge, edge), (edge, 0)] else False

        def is_taken(self, square):
            return bool(self.get_square(square))

        def adjacent_are_free(self, square):
            if self.is_same_color(self.get_relative_square(square, (0, -1))):     # UP
                return False
            elif self.is_same_color(self.get_relative_square(square, (0, 1))):    # DOWN
                return False
            elif self.is_same_color(self.get_relative_square(square, (-1, 0))):   # LEFT
                return False
            elif self.is_same_color(self.get_relative_square(square, (1, 0))):    # RIGHT
                return False
            # all adjacent squares are free
            return True

        def is_same_color(self, square):
            return True if square == Blockies.players[Blockies.player_index] else False

        def is_connected_diagonally(self, square):
            if self.is_same_color(self.get_relative_square(square, (-1, -1))):     # UP LEFT
                return True
            elif self.is_same_color(self.get_relative_square(square, (-1, 1))):    # UP RIGHT
                return True
            elif self.is_same_color(self.get_relative_square(square, (1, -1))):   # DOWN LEFT
                return True
            elif self.is_same_color(self.get_relative_square(square, (1, 1))):    # DOWN RIGHT
                return True
            # not connected diagonally to another square of the same color
            return False

        def player_has_legal_move(self):
            # FOR THE CURRENT PLAYER
            current_player_index = Blockies.player_index
            # FOR EACH REMAINING PIECE
            for piece in Blockies.player_pieces_available[current_player_index]:
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




        def get_relative_square(self, square, relative_coordinate):
            x = square[0] + relative_coordinate[0]
            y = square[1] + relative_coordinate[1]
            return self.get_square((x, y))

        def mouse_in_square(self, mouse_pos, square):
            if self.square_from_pos(mouse_pos) == square:
                return True
            else:
                return False

        def hide_mouse_square(self):
            self.active_piece = Blockies.Piece('square', 1, 1, (0, 0), const.WHITE)

        def update_active_piece(self, pos):
            new_square = self.square_from_pos(pos)
            self.active_piece.move_to(new_square)
            if not self.is_legal_position(self.active_piece):
                color = const.SQ_COLOR_ILLEGAL
            else:
                color = Blockies.players_lt_colors[Blockies.player_index]
            self.active_piece.set_color(color)

        def _display(self):
            col_header = ' ' * (len(str(const.SQ_COLUMNS)))
            for i in range(const.SQ_COLUMNS):
                col_header += ' {}{}'.format(' ' * (3 - len(str(const.SQ_COLUMNS))), i)
            print(col_header)
            for row_num in range(const.SQ_COLUMNS):
                row = '{}: {}'.format(row_num, ' ' * (len(str(const.SQ_COLUMNS)) - len(str(row_num))))
                for col_num in range(const.SQ_COLUMNS):
                    row += (str(self.color_char(self._squares[col_num][row_num])) + '  ')
                print('{}'.format(row))
            print('\n')

        def color_char(self, color):
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
