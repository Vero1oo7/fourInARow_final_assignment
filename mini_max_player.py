import math
import copy
from constants import *


class MiniMaxPlayer:

    def __init__(self):
        pass

    def do_move(self, board):  # return the best column to place the piece
        return self.calculate_next_move(board)

    def calculate_next_move(self, board):  # calculate the best score and next move for the AI
        depth = 1
        score_move_pairs = []
        for next_move in board.get_possible_moves():  # look for possible moves
            next_score = self.min_max(board, next_move, depth, -math.inf, math.inf, AI_piece)  # call minimax
            score_move_pairs.append((next_score, next_move))  # store the possible moves in a list

        if not score_move_pairs:  # if no possible moves
            return 0

        else:
            # compute the max score/move
            highest_score, best_move = max(score_move_pairs)  # calculate the best move
            print(score_move_pairs)
            # return the move
            return best_move

    def min_max(self, board, col_move, depth, alpha, beta, piece):
        next_board = copy.deepcopy(board)
        row = next_board.next_open_row(col_move)
        next_board.place_piece(row, col_move, piece)  # drop the AI piece

        if next_board.is_end_move():
            if next_board.winning_move(AI_piece):  # if AI won
                return 500000
            else:  # board is full
                return 0

        lowest_score = math.inf  # lowest score will definitely be updated
        if depth == 4:  # if depth reaches 5, calculate the heuristic value
            heuristicV = self.calculate_heuristics(next_board)
            return heuristicV

        for col in next_board.get_possible_moves():  # get possible moves for the Player piece
            new_score = self.max_min(next_board, col, depth + 1, alpha, beta,
                                     player_piece)  # look for score of next move
            lowest_score = min(new_score, lowest_score)  # take the lowest score
            beta = min(beta, lowest_score)  # minimizing player updates beta
            if alpha >= beta:  # if alpha (highest value (maximizer) ) is bigger than lowest value of minimizer
                break  # do not return a value
        return lowest_score / depth  # divide the lowest score by depth, so the deeper it goes the lower the value

    def max_min(self, board, col_move, depth, alpha, beta, piece):
        next_board = copy.deepcopy(board)
        row = next_board.next_open_row(col_move)
        next_board.place_piece(row, col_move, piece)  # drop the PLAYER piece

        if next_board.is_end_move():
            if next_board.winning_move(player_piece):
                return -500000
            else:  # board is full
                return 0

        highest_score = -math.inf
        if depth == 4:
            heuristicV = self.calculate_heuristics(next_board)  # if depth reaches 5, calculate the heuristic value
            return heuristicV

        for col in next_board.get_possible_moves():  # get possible moves for the AI piece
            new_score = self.min_max(next_board, col, depth + 1, alpha, beta, AI_piece)
            highest_score = max(new_score, highest_score)
            alpha = max(alpha, highest_score)  # maximizer player updates alpha
            if alpha >= beta:  # if alpha (highest value (maximizer) ) is bigger than lowest value of minimizer
                break
        return highest_score / depth  # divide the lowest score by depth, so the deeper it goes the lower the value

    def calculate_heuristics(self, board):
        score = 0
        ## Score center column
        center_array = [int(i) for i in list(board.board[:, COLUMNS // 2])]
        center_count = center_array.count(AI_piece)
        print(center_count)
        score += center_count * 5

        # horizontal
        for r in range(ROWS):
            row_array = [int(i) for i in list(board.board[r, :])]  # it takes a row out of the 2D array
            for c in range(COLUMNS - 3):  # for 4 columns
                array_4 = row_array[c:c + 4]  # it looks for four pieces
                score += self.evaluate_board(array_4)

        # vertical
        for c in range(COLUMNS):
            column_array = [int(i) for i in list(board.board[:, c])]  # it takes a column out of the 2D array
            for r in range(ROWS - 3):  # for 3 rows
                array_4 = column_array[r:r + 4]  # it looks for 4 pieces
                score += self.evaluate_board(array_4)

        # / diagonals
        for r in range(ROWS - 3):  # for the three rows with possible /-diagonals
            for c in range(COLUMNS - 3):  # in the column there are four possible diagonals
                array_4 = [board.board[r + i][c + i] for i in range(4)]  # it will go diagonally up till the 4th piece
                score += self.evaluate_board(array_4)

        # \ diagonals
        for r in range(3, ROWS):  # for the three top rows (3,4,5) with possible /-diagonals
            for c in range(COLUMNS - 3):  # in the column there are four possible diagonals
                array_4 = [board.board[r - i][c + i] for i in range(4)]  # count downwards \ till the 4th piece
                score += self.evaluate_board(array_4)

        return score

    def evaluate_board(self, array_4):
        score = 0

        if array_4.count(AI_piece) == 3 and array_4.count(empty) == 1:  # if 3 AI player pieces and 1 empty spot
            score += 150
        if array_4.count(AI_piece) == 2 and array_4.count(empty) == 2:
            score += 5

        # decrease the score for certain amount of PLAYER pieces
        if array_4.count(player_piece) == 3 and array_4.count(empty) == 1:
            score -= 1500
        if array_4.count(player_piece) == 2 and array_4.count(empty) == 2:
            score -= 50

        return score
