# -*- coding: cp1251 -*-
import ctypes
import pygame
import sys
import random

# ������ DLL
game = ctypes.CDLL("C:/Users/Admin/source/repos/GameProject/x64/Debug/GameProject.dll")

# ����������� ������� �� DLL
game.initialize_board.argtypes = []
game.initialize_board.restype = None

game.make_move.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
game.make_move.restype = None

game.get_board.argtypes = [ctypes.POINTER(ctypes.c_int)]
game.get_board.restype = None

game.has_valid_moves.argtypes = [ctypes.c_int]
game.has_valid_moves.restype = ctypes.c_bool

# ����������� Pygame
pygame.init()

# �������� ��������� ���
ROW_COUNT = 8
COLUMN_COUNT = 8
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
RADIUS = 45  # �� �������� ������ �������
font = pygame.font.Font(None, 36)

# ��������� ������
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width and y < mouse_y < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, (x + width // 4, y + height // 4))

# ��������� �����
def draw_board(board, current_player, scores, turns_left, window_width, window_height, game_over=False, winner=None):
    screen.fill((0, 0, 0))  # ��� ����

    # ������������ �������� ��� �����
    board_texture = pygame.image.load("C:\\Users\\Admin\\source\\repos\\GameProject\\board.jpg") 
    square_size = min(window_width, window_height - 150) // max(ROW_COUNT, COLUMN_COUNT)

    # ����� �����
    board_width = square_size * COLUMN_COUNT
    board_height = square_size * ROW_COUNT

    # ���������� ������� ��� �����������
    offset_x = (window_width - board_width) // 2
    offset_y = (window_height - board_height - 100) // 2  # �������� ������ ��� ������

    # ���������� �������� �� ������ �����
    scaled_texture = pygame.transform.scale(board_texture, (board_width, board_height))

    # ������� �������� �� ��� �����
    screen.blit(scaled_texture, (offset_x, offset_y))

    # ��������� ���������� ������ ��������
    radius = square_size // 2 - 5

    # ������������ ���������� ������ � ���������� ������
    board_2d = [
        [board[r * COLUMN_COUNT + c] for c in range(COLUMN_COUNT)]
        for r in range(ROW_COUNT)
    ]

    # ��������� ������� ������ ��������
    for r in range(ROW_COUNT + 1):  # ������������ ��
        pygame.draw.line(screen, (0, 0, 0), 
                         (offset_x, offset_y + r * square_size), 
                         (offset_x + board_width, offset_y + r * square_size), 2)

    for c in range(COLUMN_COUNT + 1):  # ���������� ��
        pygame.draw.line(screen, (0, 0, 0), 
                         (offset_x + c * square_size, offset_y), 
                         (offset_x + c * square_size, offset_y + board_height), 2)

    # ��������� ��������� ����� (1, 2, 3, ...)
    for r in range(ROW_COUNT):
        label = font.render(str(r + 1), True, TEXT_COLOR)
        screen.blit(label, (offset_x - 30, offset_y + r * square_size + square_size // 2 - label.get_height() // 2))

    # ��������� ��������� ������� (a, b, c, ...)
    for c in range(COLUMN_COUNT):
        label = font.render(chr(ord('a') + c), True, TEXT_COLOR)
        screen.blit(label, (offset_x + c * square_size + square_size // 2 - label.get_width() // 2, offset_y - 30))

    # ��������� ����� �� �����
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            center_x = offset_x + c * square_size + square_size // 2
            center_y = offset_y + r * square_size + square_size // 2

            if board_2d[r][c] == 0:
                pygame.draw.circle(screen, (200, 200, 200), (center_x, center_y), radius)
            elif board_2d[r][c] == 1:
                pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
            elif board_2d[r][c] == 2:
                pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius)

    # ��������� ������ �� ������
    text_offset_y = offset_y + board_height + 10  
    player_text = font.render(f"ճ� ������: {'������' if current_player == 1 else '�����'}", True, TEXT_COLOR)
    score_text = font.render(f"������: {scores[0]}  �����: {scores[1]}", True, TEXT_COLOR)
    turns_text = font.render(f"���������� ����: {turns_left}", True, TEXT_COLOR)

    screen.blit(player_text, (10, text_offset_y))
    screen.blit(score_text, (300, text_offset_y))
    screen.blit(turns_text, (10, text_offset_y + 30))

    # ³���������� ���������� ���� ���������� ���
    if game_over:
        game_over_text = font.render("��� ���������!", True, (255, 0, 0))
        winner_text = font.render(f"����������: {winner}", True, (255, 0, 0))
        screen.blit(game_over_text, (window_width // 4, window_height // 2 - 40))
        screen.blit(winner_text, (window_width // 4, window_height // 2))

    pygame.display.update()
# ϳ�������� �����
def calculate_scores(board):
    black_count = 0
    white_count = 0
    for value in board:
        if value == 1:
            black_count += 1
        elif value == 2:
            white_count += 1
    return black_count, white_count

# ������� �������� ������� ����
def input_max_turns():
    while True:
        try:
            max_turns = int(input("������ ������� ���� (���������, 60): "))
            if max_turns > 0:
                return max_turns
            else:
                print("ʳ������ ���� �� ���� ����� 0.")
        except ValueError:
            print("���� �����, ������ ���� �����.")
            

# ������� ����
def main_menu():
    while True:
        screen.fill((0, 0, 0))  # ���

        button_width = window_width // 4
        button_height = window_height // 12
        button_x = (window_width - button_width) // 2
        button_y1 = (window_height - 4 * button_height) // 2
        button_y2 = button_y1 + 2 * button_height
        button_y3 = button_y2 + 2 * button_height

        title_text = font.render("������", True, TEXT_COLOR)
        screen.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 100))

        draw_button("���� ���", button_x, button_y1, button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR)
        draw_button("�����", button_x, button_y3, button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR)

        author_text = font.render("�����: ��������� ������", True, TEXT_COLOR)
        screen.blit(author_text, (window_width - author_text.get_width() - 20, window_height - author_text.get_height() - 20))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                update_window_size(event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if button_x < mouse_x < button_x + button_width and button_y1 < mouse_y < button_y1 + button_height:
                    return "start_game"
                
                elif button_x < mouse_x < button_x + button_width and button_y3 < mouse_y < button_y3 + button_height:
                    pygame.quit()
                    sys.exit()
# �������� ���� ���
def start_game():
    global window_width, window_height, screen

    game.initialize_board()
    player = 1
    board = (ctypes.c_int * (ROW_COUNT * COLUMN_COUNT))()

    # �������� ������� ���� ����� ����
    max_turns = input_turns_via_window()
    total_turns = 0

    while total_turns < max_turns:
        game.get_board(board)
        scores = calculate_scores(board)
        draw_board(board, player, scores, max_turns - total_turns, window_width, window_height)

        if not (game.has_valid_moves(1) or game.has_valid_moves(2)):
            break  # ��������� ���, ���� ���� ����

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:  # ������� ���� ������
                update_window_size(event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                square_size = min(window_width, window_height - 100) // max(ROW_COUNT, COLUMN_COUNT)

                # ����������� �������
                offset_x = (window_width - (square_size * COLUMN_COUNT)) // 2
                offset_y = (window_height - (square_size * ROW_COUNT)) // 2

                # ���������� ����� � ������� � ����������� �������
                col = (x - offset_x) // square_size
                row = (y - offset_y) // square_size

                # ����������, �� ���������� � ����� �����
                if 0 <= col < COLUMN_COUNT and 0 <= row < ROW_COUNT:
                    game.make_move(row, col, player)
                    game.get_board(board)  # ������� �����
                    new_scores = calculate_scores(board)

                    # ����������� ������
                    if scores != new_scores:  # ճ� ��� �������
                        player = 3 - player
                        total_turns += 1

    # ���������� ���
    game.get_board(board)
    scores = calculate_scores(board)
    winner = "ͳ���"
    if scores[0] > scores[1]:
        winner = "������"
    elif scores[1] > scores[0]:
        winner = "�����"

    # ³��������� ��������� ���������
    draw_board(board, player, scores, max_turns - total_turns, window_width, window_height, game_over=True, winner=winner)

    # �������� ����� ����������� �� ��������� ����
    pygame.time.wait(5000)
# ���� ������ ����
def update_window_size(width, height):
    global window_width, window_height, screen
    window_width, window_height = width, height
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    
def input_turns_via_window():
    input_box = pygame.Rect(300, 200, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # ���� ��������� ����, ����������, �� ���������� ����
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            turns = int(text)
                            if turns > 0:
                                return turns
                        except ValueError:
                            pass
                        text = ''  # �������� �����, ���� ������� ���������� ��������
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # ��������� �����
        screen.fill((0, 0, 0))
        info_text = font.render("������ ������� ����:", True, TEXT_COLOR)
        screen.blit(info_text, (300, 150))

        # ³���������� ������
        txt_surface = font.render(text, True, TEXT_COLOR)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        


# ����������� ����
window_width = 800
window_height = 800
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

# ������ ����������� ����
if __name__ == "__main__":
    while True:
        mode = main_menu()
        if mode == "start_game":
            start_game()
        elif mode == "start_ai_game":
            start_ai_game()