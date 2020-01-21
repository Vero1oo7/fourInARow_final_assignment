import numpy as np
from constants import *
#  class board contains all the moving and counting of the pieces


class Board:

    def __init__(self):
        self.board = np.zeros((ROWS, COLUMNS))  # creating 6 arrays with 7 fields with the value zero

    def place_piece(self, row, col, piece):
        self.board[row][col] = piece  # drop the piece in the row and column given with the function

    def next_open_row(self, col):
        for row in range(ROWS):  # return the next open row of a column
            if self.board[row][col] == 0:
                return row

    def print_board(self):
        print(np.flip(self.board, 0))  # print the board with the first row on the bottom

    def is_end_move(self):
        # when player or AI wins or there are no possible moves (board is full)
        return self.winning_move(player_piece) or self.winning_move(AI_piece) or len(
            self.get_possible_moves()) == 0

    def is_possible_move(self, column):
        # check if the column is not full
        return self.board[ROWS - 1][column] == 0

    def get_possible_moves(self):
        # get all the possible moves and put them in an array
        possible_moves = []
        for column in range(COLUMNS):
            if self.is_possible_move(column):
                possible_moves.append(column)
        return possible_moves

    def winning_move(self, piece):

        # horizontal
        for r in range(ROWS):
            row_array = [int(i) for i in list(self.board[r, :])]  # it takes a row out of the 2D array
            for c in range(COLUMNS - 3):  # for 4 columns
                array_4 = row_array[c:c + 4]  # it looks for four pieces
                if array_4.count(piece) == 4:  # if in the array, there are 4 of the same piece
                    return True

        # vertical
        for c in range(COLUMNS):
            column_array = [int(i) for i in list(self.board[:, c])]  # it takes a column out of the 2D array
            for r in range(ROWS - 3):  # for 3 rows
                array_4 = column_array[r:r + 4]  # it looks for 4 pieces
                if array_4.count(piece) == 4:  # if these 4 pieces are all the same piece
                    return True

        # / diagonals
        for r in range(ROWS - 3):  # for the three rows with possible /-diagonals
            for c in range(COLUMNS - 3):  # in the column there are four possible diagonals
                array_4 = [self.board[r + i][c + i] for i in range(4)]  # it will go diagonally up till the 4th piece
                if array_4.count(piece) == 4:  # if the four pieces are all the same
                    return True

        # \ diagonals
        for r in range(3, ROWS):  # for the three top rows (3,4,5) with possible /-diagonals
            for c in range(COLUMNS - 3):  # in the column there are four possible diagonals
                array_4 = [self.board[r - i][c + i] for i in range(4)]  # count downwards \ till the 4th piece
                if array_4.count(piece) == 4:  # if the four pieces are the same piece in the diagonal
                    return True
