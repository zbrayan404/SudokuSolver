from assets.doublyLinked import DoublyLinked


# A class for each squares on the Sudoku board
class Square:
    def __init__(self, row, col, value, editable):
        self._row = row
        self._col = col
        self._value = value
        self._editable = editable

    def get_row(self):
        return self._row

    def set_row(self, row):
        self._row = row

    def get_col(self):
        return self._col

    def set_col(self, col):
        self._col = col

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def set_editable(self, value):
        self._editable = value

    def get_editable(self):
        return self._editable


# A class for the Sudoku board
class Sudoku:
    def __init__(self):
        self.board = [[], [], [], [], [], [], [], [], []]
        self.empty = DoublyLinked()
        self.cursor = self.empty.get_header()
        self.create_board("000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    # Creates the new board
    def create_board(self, board):
        self.board = [[], [], [], [], [], [], [], [], []]
        end = 0
        for row in range(9):
            start = end
            end = start + 9
            rows = board[start:end]
            for col in range(9):
                if rows[col] == '0' or rows[col] == '.':
                    value = None
                    edit = True
                else:
                    value = int(rows[col])
                    edit = False
                self.board[row].append(Square(row, col, value, edit))
        self.empty_square()

    # Checks if the input is valid
    def valid_number(self, sq, num):
        for col in range(9):
            if self.board[sq.get_row()][col].get_value() == num and col != sq.get_col():
                return False
        for row in range(9):
            if self.board[row][sq.get_col()].get_value() == num and row != sq.get_row():
                return False
        for row in range(sq.get_row() // 3 * 3, sq.get_row() // 3 * 3 + 3):
            for col in range(sq.get_col() // 3 * 3, sq.get_col() // 3 * 3 + 3):
                if (self.board[row][col].get_value() == num and row != sq.get_row()
                        and col != sq.get_col()):
                    return False
        return True

    # Just check the col if the input is valid
    def check_col(self, sq, col):
        if (self.board[sq.get_row()][col].get_value() == sq.get_value() and col != sq.get_col()
                and sq.get_value() is not None):
            return True
        return False

    # Just check the row if the input is valid
    def check_row(self, sq, row):
        if (self.board[row][sq.get_col()].get_value() == sq.get_value() and row != sq.get_row()
                and sq.get_value() is not None):
            return True
        return False

    # Just check the box if the input is valid
    def check_box(self, sq, row, col):
        if (self.board[row][col].get_value() == sq.get_value() and row != sq.get_row()
                and col != sq.get_col() and sq.get_value() is not None):
            return True
        return False

    # Reset the whole board, just the editable or all
    def reset(self, setting=0):
        for row in self.board:
            for sq in row:
                if setting == 0:
                    if sq.get_editable():
                        sq.set_value(None)
                else:
                    self.create_board("000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    # Set the current numbers
    def set(self):
        for row in self.board:
            for sq in row:
                if sq.get_value() is not None:
                    sq.set_editable(False)
        self.empty_square()

    # Add the empty square into the doubly linked list
    def empty_square(self):
        self.empty = DoublyLinked()
        for row in range(9):
            for col in range(9):
                if self.board[row][col].get_value() is None:
                    self.empty.insert_last(self.board[row][col])
        self.cursor = self.empty.get_header()

    # The cursor will move forward and get an empty square
    def find_square(self):
        self.cursor = self.cursor.get_next()
        return self.cursor.get_element()

    # The cursor will move back to backtrack
    def prev(self):
        self.cursor = self.cursor.get_prev()

    # Backtracking Solver
    def solver(self):
        # Find Empty Square
        sq = self.find_square()
        # Checks if Square is Valid
        if not sq:
            return True
        # Input 1-9 in the Square
        for value in range(1, 10):
            if not self.valid_number(sq, value):
                continue
            sq.set_value(value)
            # Next Square
            if self.solver():
                return True
            else:
                # BackTrack
                self.prev()
                sq.set_value(None)
        return False











