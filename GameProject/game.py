import ctypes
import pygame
import sys

game = ctypes.CDLL("C:/Users/Admin/source/repos/GameProject/x64/Debug/GameProject.dll")

game.initialize_board.argtypes = []
game.initialize_board.restype = None

game.make_move.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
game.make_move.restype = None

game.get_board.argtypes = [ctypes.POINTER(ctypes.c_int)]
game.get_board.restype = None

pygame.init()
SQUARESIZE = 100
ROW_COUNT = 8
COLUMN_COUNT = 8
size = (SQUARESIZE * COLUMN_COUNT, SQUARESIZE * ROW_COUNT)
screen = pygame.display.set_mode(size)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RADIUS = SQUARESIZE // 2 - 5

def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            color = GRAY
            if board[r][c] == 1:
                color = WHITE
            elif board[r][c] == 2:
                color = BLACK
            pygame.draw.circle(screen, color, (c * SQUARESIZE + SQUARESIZE // 2,
                                               r * SQUARESIZE + SQUARESIZE // 2), RADIUS)
    pygame.display.update()

game.initialize_board()

running = True
player = 1
board = (ctypes.c_int * (ROW_COUNT * COLUMN_COUNT))()

while running:
    game.get_board(board)
    draw_board(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // SQUARESIZE
            row = y // SQUARESIZE

            game.make_move(row, col, player)
            player = 3 - player

pygame.quit()