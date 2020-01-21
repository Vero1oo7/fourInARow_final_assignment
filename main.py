from board import Board
from open_cv import OpenCV
from mini_max_player import MiniMaxPlayer
from arduino import Arduino
import random
import time
from constants import *

# code based on: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
# Module 6 final assignment programming Python by Feline Waardenburg s2157993 and Veronique Kochetov s2168405
# 4 in a row installation with minimax, alpha-beta pruning, heuristics and a physical representation (LEDs, Arduino)
# use of library openCV to detect player's moves

class Main:

    def __init__(self):
        self.board = Board()
        self.game_over = False
        self.opencv = OpenCV()
        self.turn = random.randint(player_piece, AI_piece)
        self.minmaxPlayer = MiniMaxPlayer()
        self.arduino = Arduino()

    def game_loop(self):
        self.opencv.capture()  # start opencv record and "red" detection

        if self.arduino.arduino_receive() == 1:  # if button is pressed

            if self.turn == player_piece:
                col = self.opencv.get_new_stone()  # detect red object, get column of location

                if self.board.is_possible_move(col):
                    row = self.board.next_open_row(col)
                    self.board.place_piece(row, col, player_piece)
                    self.arduino.arduino_com_PLAYER(row, col)  # send piece position to arduino

                    if self.board.winning_move(player_piece):
                        print("player wins")
                        self.game_over = True
                        self.arduino.arduino_com_PLAYER(10, 10)  # turn all the LEDs on (player color)

                    self.board.print_board()
                    self.turn = AI_piece

        #  AI turn
        if self.turn == AI_piece and not self.game_over:
            time.sleep(1)  # wait a second to establish the arduino connection if AI starts

            col = self.minmaxPlayer.do_move(self.board)  # get the best column to place the move

            if self.board.is_possible_move(col):
                row = self.board.next_open_row(col)
                self.board.place_piece(row, col, AI_piece)
                self.arduino.arduino_com_AI(row, col)

                if self.board.winning_move(AI_piece):
                    print("AI wins")
                    self.game_over = True
                    self.arduino.arduino_com_AI(10, 10)

                self.board.print_board()
                self.turn = player_piece


if __name__ == "__main__":
    game = Main()
    while not game.game_over:
        game.game_loop()
