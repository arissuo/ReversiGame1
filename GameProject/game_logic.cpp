#include "pch.h"
#include "game_logic.h"
#include <vector>
#include <iostream>


constexpr int BOARD_SIZE = 8;

class GameBoard {
private:
    std::vector<std::vector<int>> board;

public:
    GameBoard() : board(BOARD_SIZE, std::vector<int>(BOARD_SIZE, 0)) {}

    void initialize_board() {
        for (auto& row : board) {
            std::fill(row.begin(), row.end(), 0);
        }
        board[3][3] = 1;
        board[4][4] = 1;
        board[3][4] = 2;
        board[4][3] = 2;
    }

    bool is_valid_move(int row, int col, int player) {
        if (board[row][col] != 0) return false;

        int directions[8][2] = { {-1, -1}, {-1, 0}, {-1, 1}, {1, 1},
                                {1, 0},  {1, -1}, {0, 1},  {0, -1} };
        for (auto& dir : directions) {
            int x = row + dir[0];
            int y = col + dir[1];
            bool has_opponent = false;

            while (x >= 0 && x < BOARD_SIZE && y >= 0 && y < BOARD_SIZE) {
                if (board[x][y] == 0) break;
                if (board[x][y] == player) {
                    if (has_opponent) return true;
                    break;
                }
                else {
                    has_opponent = true;
                }
                x += dir[0];
                y += dir[1];
            }
        }
        return false;
    }

    void make_move(int row, int col, int player) {
        if (!is_valid_move(row, col, player)) return;

        board[row][col] = player;

        int directions[8][2] = { {-1, -1}, {-1, 0}, {-1, 1}, {1, 1},
                                {1, 0},  {1, -1}, {0, 1},  {0, -1} };
        for (auto& dir : directions) {
            int x = row + dir[0];
            int y = col + dir[1];
            std::vector<std::pair<int, int>> to_flip;

            while (x >= 0 && x < BOARD_SIZE && y >= 0 && y < BOARD_SIZE) {
                if (board[x][y] == 0) break;
                if (board[x][y] == player) {
                    for (size_t i = 0; i < to_flip.size(); ++i) {
                        int fx = to_flip[i].first;
                        int fy = to_flip[i].second;
                        board[fx][fy] = player;
                    }
                    break;
                }
                else {
                    to_flip.emplace_back(x, y);
                }
                x += dir[0];
                y += dir[1];
            }
        }
    }

    void get_board(int* output) {
        for (int i = 0; i < BOARD_SIZE; ++i) {
            for (int j = 0; j < BOARD_SIZE; ++j) {
                output[i * BOARD_SIZE + j] = board[i][j];
            }
        }
    }

    bool has_valid_moves(int player) {
        for (int row = 0; row < BOARD_SIZE; ++row) {
            for (int col = 0; col < BOARD_SIZE; ++col) {
                if (is_valid_move(row, col, player)) {
                    return true;
                }
            }
        }
        return false;
    }
};

GameBoard game;
std::vector<std::pair<int, int>> get_valid_moves(int player) {
    std::vector<std::pair<int, int>> valid_moves;
    for (int row = 0; row < BOARD_SIZE; ++row) {
        for (int col = 0; col < BOARD_SIZE; ++col) {
            if (game.is_valid_move(row, col, player)) {
                valid_moves.emplace_back(row, col);
            }
        }
    }
    return valid_moves;
}

extern "C" {
    void ai_make_move(int player) {
        std::vector<std::pair<int, int>> valid_moves = get_valid_moves(player);
        if (!valid_moves.empty()) {
            // Вибираємо перший доступний хід
            auto move = valid_moves.front();
            game.make_move(move.first, move.second, player);
        }
    }
    void initialize_board() {
        game.initialize_board();
    }

    bool is_valid_move(int row, int col, int player) {
        return game.is_valid_move(row, col, player);
    }

    void make_move(int row, int col, int player) {
        game.make_move(row, col, player);
    }

    void get_board(int* output) {
        game.get_board(output);
    }

    bool has_valid_moves(int player) {
        return game.has_valid_moves(player);
    }
}
