from pandas import *
from csv import writer
from assets.sudokuBoardV2 import Sudoku
import timeit


# A class to benchmark the sudoku solver
class Benchmark:
    def __init__(self):
        self.board = Sudoku()
        self.time = 0
        self.output = ''

    # Gets the time
    def solve_time(self):
        start_time = timeit.default_timer()
        self.board.solver()
        return timeit.default_timer() - start_time

    # Add the data to the file
    def add(self, board):
        # Board created
        self.board.create_board(board)
        # Solved time
        solve = self.solve_time()
        self.time += solve
        # Data that will be added
        add_data = [board, solve]
        with open(self.output, 'a+', newline='') as write_obj:
            # Create a writer from csv module
            csv_writer = writer(write_obj)
            # Add data in the csv file
            csv_writer.writerow(add_data)

    # Gets the data from a csv file and
    def csv_file(self, csv, col, number, output):
        self.output = output
        data = read_csv(csv)
        puzzles = data[col].tolist()
        for puzzle in range(number):
            print((puzzle + 1) / number)
            self.add(puzzles[puzzle])
        print(self.time)

