import pygame
from sys import exit
from assets.sudokuBoardV2 import Sudoku
import time

# Size of Window
width = 504
height = 848
# Size of Squares
sudoku_sq = 40
answer_sq = 45

# Display the Window
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sudoku')

color1 = (255, 255, 255)  # Non-editable Numbers
color2 = (229, 229, 229)  # Square Outline
color3 = (252, 163, 17)  # Selected Square Outline and Number
color4 = (252, 84, 17)  # Wrong Number
color5 = (36, 59, 110)  # Selected Square
color6 = (20, 33, 61)  # Background


# A Child class of the Parent class, pygame.Rect.
# To add rows and columns values
class RectSquare(pygame.Rect):
    def __init__(self, left, top, row, col, s_width, s_height):
        super().__init__(left, top, s_width, s_height)
        self.left = left
        self.top = top
        self.row = row
        self.col = col


# Creates the grid for the clicks inputs
def create_answer():
    board_answer = [[], [], []]
    top = 620
    for row in range(3):
        left = (width - (3 * answer_sq + 2 * (answer_sq * 0.2))) / 2
        for col in range(3):
            board_answer[row].append(RectSquare(left, top, row, col, answer_sq, answer_sq))
            left += answer_sq + (answer_sq * 0.2)
        top += answer_sq + (answer_sq * 0.2)
    size = (3 * answer_sq + 2 * (answer_sq * 0.2))
    top = answer_sq + (answer_sq * 0.2)
    board_answer[2].append(RectSquare(board_answer[0][0].left, (board_answer[2][2].top + top), 2, 3, size, answer_sq))
    return board_answer


# Draws the clicks inputs
def answers(answer, numbers):
    font = pygame.font.Font('assets/font/Prestij_Bold.otf', int(answer_sq * 0.87))
    for row in answer:
        for sq in row:
            text = font.render(str(numbers[sq.row][sq.col]), True, color1)
            square(sq, text, sq.width, sq.height, color3, 3)


# Creates the grid for sudoku
def create_board():
    board_sudoku = [[], [], [], [], [], [], [], [], []]
    left = (width - (9 * sudoku_sq + 6 * (sudoku_sq * 0.2) + 2 * (sudoku_sq * 0.4))) / 2
    top = 110
    for row in range(9):
        for col in range(9):
            board_sudoku[row].append(RectSquare(left, top, row, col, sudoku_sq, sudoku_sq))
            left += sudoku_sq + (sudoku_sq * 0.2)
            if col != 0 and (col + 1) % 3 == 0:
                left = left + (sudoku_sq * 0.2)
        top += sudoku_sq + (sudoku_sq * 0.2)
        if row != 0 and (row + 1) % 3 == 0:
            top = top + (sudoku_sq * 0.2)
        left = (width - (9 * sudoku_sq + 6 * (sudoku_sq * 0.2) + 2 * (sudoku_sq * 0.4))) / 2
    return board_sudoku


# Draws the sudoku board
def sudoku(sqs, sudo):
    font = pygame.font.Font('assets/font/Prestij_Bold.otf', int(sudoku_sq * 0.8))
    for row in sqs:
        for sq in row:
            sudo_sq = sudo.board[sq.row][sq.col]
            if sudo_sq.get_value() is None:
                square(sq, None, sudoku_sq, sudoku_sq, color2)
                continue
            if not sudo_sq.get_editable():
                text = font.render(f'{sudo_sq.get_value()}', True, color1)
            else:
                if sudo.valid_number(sudo_sq, sudo_sq.get_value()):
                    text = font.render(f'{sudo_sq.get_value()}', True, color3)
                else:
                    text = font.render(f'{sudo_sq.get_value()}', True, color4)
            square(sq, text, sudoku_sq, sudoku_sq, color2)


# Draw squares and rectangle
def square(sq, text, sq_width, sq_height, color, thickness=2):
    x, y = sq.topleft
    pygame.draw.rect(screen, color, pygame.Rect(x, y, sq_width, sq_height), thickness, thickness)
    if text is not None:
        x, y = sq.center
        textbox = text.get_rect(center=(x, y))
        screen.blit(text, textbox)


# Draws the sudoku screen with each update
def draw_sudoku_board(clicked, sqs, sudo):
    title()
    pygame.draw.rect(screen, color3, pygame.Rect(0, 0, width, height), 2, 2)
    if solving:
        stop_button()
    else:
        auto_button()
    restart_button()
    answers(create_answers, answer_board)
    sudoku(sqs, sudo)
    if clicked is not None:
        sq = sudo.board[clicked.row][clicked.col]
        pygame.draw.rect(screen, color5, clicked)
        sudoku(sqs, sudo)
        for row in range(clicked.row // 3 * 3, clicked.row // 3 * 3 + 3):
            for col in range(clicked.col // 3 * 3, clicked.col // 3 * 3 + 3):
                if sudo.check_box(sq, row, col):
                    square(sqs[row][col], None, sudoku_sq, sudoku_sq, color4)
                else:
                    square(sqs[row][col], None, sudoku_sq, sudoku_sq, color3)
        for row in range(9):
            if sudo.check_row(sq, row):
                square(sqs[row][clicked.col], None, sudoku_sq, sudoku_sq, color4)
            else:
                square(sqs[row][clicked.col], None, sudoku_sq, sudoku_sq, color3)
        for col in range(9):
            if sudo.check_col(sq, col):
                square(sqs[clicked.row][col], None, sudoku_sq, sudoku_sq, color4)
            else:
                square(sqs[clicked.row][col], None, sudoku_sq, sudoku_sq, color3)

# Visual Solver
def solver(sudo, sqs):
    screen.fill(color6)
    sq = sudo.find_square()
    if not sq:
        return True
    for value in range(1, 10):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if stop.collidepoint(mouse_pos):
                    return True
        if not sudo.valid_number(sq, value):
            continue
        sq.set_value(value)
        screen.fill(color6)
        draw_sudoku_board(sqs[sq.get_row()][sq.get_col()], sqs, sudo)
        pygame.display.flip()
        time.sleep(0.05)
        if solver(sudo, sqs):
            return True
        else:
            sudo.prev()
            sq.set_value(None)
    return False


# Click input for which square was clicked
def square_click(clicked, mouse_pos):
    for row in sudoku_board:
        for sq in row:
            if sq.collidepoint(mouse_pos):
                clicked = sq
                click = board.board[clicked.row][clicked.col]
                if clicked and not click.get_editable():
                    clicked = None
    return clicked


# Click input for which number enter
def click_input(clicked, number, mouse_pos):
    for row in create_answers:
        for sq in row:
            if sq.collidepoint(mouse_pos):
                number = sq
                if clicked is not None:
                    click = board.board[clicked.row][clicked.col]
                    click_num = answer_board[number.row][number.col]
                    if click_num == 0:
                        click.set_value(None)
                    else:
                        click.set_value(click_num)
                else:
                    number = None
    return number


# Keyboard input for which number enter
def key_input(click, key):
    clicked = board.board[click.row][click.col]
    if key == pygame.K_0:
        clicked.set_value(None)
    if key == pygame.K_1:
        clicked.set_value(1)
    if key == pygame.K_2:
        clicked.set_value(2)
    if key == pygame.K_3:
        clicked.set_value(3)
    if key == pygame.K_4:
        clicked.set_value(4)
    if key == pygame.K_5:
        clicked.set_value(5)
    if key == pygame.K_6:
        clicked.set_value(6)
    if key == pygame.K_7:
        clicked.set_value(7)
    if key == pygame.K_8:
        clicked.set_value(8)
    if key == pygame.K_9:
        clicked.set_value(9)
    if key == pygame.K_BACKSPACE:
        clicked.set_value(None)


# Restart Button
def restart_button():
    font = pygame.font.Font('assets/font/Prestij_Bold.otf', 20)
    text = font.render(f'{"RESET"}', True, color1)
    square(restart, text, restart.width, restart.height, color1)


# Solver Button
def auto_button():
    font = pygame.font.Font('assets/font/Prestij_Bold.otf', 20)
    text = font.render(f'{"AUTO"}', True, color1)
    square(auto, text, auto.width, auto.height, color1)

# Stop Button
def stop_button():
    font = pygame.font.Font('assets/font/Prestij_Bold.otf', 20)
    text = font.render(f'{"STOP"}', True, color1)
    square(stop, text, stop.width, stop.height, color1)

# Sudoku Title
def title():
    font = pygame.font.Font('assets/font/Prestij_Bold.otf', 80)
    text = font.render(f'{"SUDOKU"}', True, color1)
    square(titles, text, titles.width, titles.height, color6)


# Back Button
def home_button():
    home_icon = pygame.image.load('assets/icon/back_icon.png').convert_alpha()
    square(home, home_icon, home.width, home.height, color6)


# Version 1
def play_button():
    font = pygame.font.Font('assets/font/Prestij_Bold.otf', 25)
    text = font.render(f'{"SOLVER"}', True, color1)
    square(play, text, play.width, play.height, color1)

# The Start-up Screen
def intro_screen():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if play.collidepoint(mouse_pos):
                board.reset(1)
                game_state = 'solver_game'
    screen.fill(color6)
    title()
    pygame.draw.rect(screen, color3, pygame.Rect(0, 0, width, height), 2, 2)
    play_button()
    pygame.display.flip()


# The Solver Screen
def solver_screen():
    global current_click
    global answer_click
    global solving
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            current_click = square_click(current_click, mouse_pos)
            answer_click = click_input(current_click, answer_click, mouse_pos)
            if restart.collidepoint(mouse_pos):
                board.reset(1)
            if auto.collidepoint(mouse_pos):
                board.set()
                board.reset()
                solving = True
                solver(board, sudoku_board)
                solving = False
            if home.collidepoint(mouse_pos):
                game_state = 'intro'
        if event.type == pygame.KEYUP:
            key = event.key
            if current_click is not None:
                key_input(current_click, key)
    screen.fill(color6)
    home_button()
    title()
    draw_sudoku_board(current_click, sudoku_board, board)
    pygame.display.flip()


# Create Asset
titles = pygame.Rect(0, 0, width, 110)
restart = pygame.Rect(32, (548 + (sudoku_sq * 0.4)), 100, 40)
auto = pygame.Rect(width - (32 + 100), (548 + (sudoku_sq * 0.4)), 100, 40)
stop = pygame.Rect(width - (32 + 100), (548 + (sudoku_sq * 0.4)), 100, 40)
play = pygame.Rect((width - 200) / 2, 448, 200, 70)
home = pygame.Rect(20, 30, 35, 50)

# Game Manager
game_state = 'intro'

# Creating Sudoku Board
sudoku_board = create_board()
board = Sudoku()
sudoku(sudoku_board, board)

# Creating Answer Board
create_answers = create_answer()
answer_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9, 0]]
answers(create_answers, answer_board)

# For Click Inputs
current_click = None
answer_click = None
solving = False

def main():
    global game_state
    while True:
        if game_state == 'intro':
            intro_screen()
        if game_state == 'solver_game':
            solver_screen()


if __name__ == "__main__":
    main()


