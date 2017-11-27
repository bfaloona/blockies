import const


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
            self.squares = []
            self.matrix = [[]]
            self.corner_squares = []
            self.is_legal = False
            if not self.shape in ['square', 'rectangle']:
                raise ValueError('Only type `square` is currently supported')
            if self.root_square:
                self.hydrate()

        def set_color(self, color):
            self.color = color

        def set_color_current(self):
            self.color = Blockies.players[Blockies.player_index]

        def set_root_square(self, square):
            self.root_square = square
            self.hydrate()

        def _set_rect_points(self, x_squares, y_squares):
            p1 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            p2 = (
                int((self.root_square[0] * const.SQ_SIZE) + const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (y_squares * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p3 = (
                int((self.root_square[0] * const.SQ_SIZE) + (x_squares * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + (y_squares * const.SQ_SIZE) - const.SQ_PADDING),
            )
            p4 = (
                int((self.root_square[0] * const.SQ_SIZE) + (x_squares * const.SQ_SIZE) - const.SQ_PADDING),
                int((self.root_square[1] * const.SQ_SIZE) + const.SQ_PADDING),
            )
            self.points = [p1, p2, p3, p4]

        def hydrate(self):
            self.matrix = [[]]
            for y in range(self.y_squares):
                for x in range(self.x_squares):
                    if len(self.matrix) < x + 1:
                        self.matrix.append([])
                    self.matrix[x].append('*')
            self._set_rect_points(self.x_squares, self.y_squares)
            self._find_squares_taken()

        def display(self):
            print('   0  1')
            for row_num in range(len(self.matrix[0])):
                row = '{}: '.format(row_num)
                for col_num in range(len(self.matrix)):
                    row += ('*  ' if self.matrix[col_num][row_num] is not None else '   ')
                print('{}'.format(row))
            print('\n')

        def _find_squares_taken(self):
            new_squares = []
            for row_num in range(len(self.matrix[0])):
                for col_num in range(len(self.matrix)):
                    if self.matrix[col_num][row_num] is not None:
                        x = col_num + self.root_square[0]
                        y = row_num + self.root_square[1]
                        square = (x, y)
                        new_squares.append(square)
            self.squares = new_squares
            self.corner_squares = self.find_corner_coordinates(self)

        def find_corner_coordinates(self, piece):
            root_x = self.root_square[0]
            root_y = self.root_square[1]

            bottom_left = (root_x, len(self.matrix[0]) + root_y - 1)
            top_right = (len(self.matrix) + root_x - 1, root_y)
            bottom_right = (len(self.matrix) + root_x - 1, len(self.matrix[0]) + root_y - 1)

            return [self.root_square, bottom_left, top_right, bottom_right]

    class Grid:

        def __init__(self):
            self._squares = [[None for i in range(const.SQ_COLUMNS)] for x in range(const.SQ_COLUMNS)]
            self.available_pieces = [
                Blockies.Piece('square', 1, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 2, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 1, 2, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('square', 2, 2, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 3, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 1, 3, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('square', 3, 2, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('square', 2, 3, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('square', 3, 3, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('square', 4, 3, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('square', 3, 4, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 4, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                Blockies.Piece('rectangle', 1, 4, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('square', 4, 4, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('rectangle', 5, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('rectangle', 1, 5, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('rectangle', 6, 1, (0, 0), const.SQ_COLOR_ILLEGAL),
                # Blockies.Piece('rectangle', 1, 6, (0, 0), const.SQ_COLOR_ILLEGAL),
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
            piece.set_root_square(square)
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
                        piece.set_root_square((x, y))
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
            self.active_piece.set_root_square(new_square)
            if not self.is_legal_position(self.active_piece):
                color = const.SQ_COLOR_ILLEGAL
            else:
                color = Blockies.players_lt_colors[Blockies.player_index]
            self.active_piece.set_color(color)

        def display(self):
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
