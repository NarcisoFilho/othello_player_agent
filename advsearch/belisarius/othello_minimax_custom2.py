import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [6,   1,   1, 1, 1, 1, 1,   6],
    [2,   1,   1, 3, 3, 1, 1,   2],
    [2,   1,   1, 3, 3, 1, 1,   2],
    [6,   1,   1, 1, 1, 1, 1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def make_move(state) -> Tuple[int, int]:
    return minimax_move(state, 4, evaluate_custom)

def evaluate_custom(state: GameState, player: str) -> float:
    board = state.board.tiles
    opponent = 'W' if player == 'B' else 'B'

    position_score = 0
    corner_score = 0
    frontier_score = 0
    stable_score = 0

    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

    for y in range(8):
        for x in range(8):
            cell = board[y][x]
            if cell == '.':
                continue

            multiplier = 1 if cell == player else -1
            position_score += EVAL_TEMPLATE[y][x] * multiplier

            if (x, y) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                corner_score += 25 * multiplier

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == '.':
                    frontier_score += -multiplier
                    break

            if (x in [0, 7] or y in [0, 7]) and cell == player:
                stable_score += 1

    player_moves = len(state.get_possible_actions(player))
    opponent_moves = len(state.get_possible_actions(opponent))
    mobility_score = 0
    if player_moves + opponent_moves > 0:
        mobility_score = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)

    empty_tiles = sum(row.count('.') for row in board)
    parity = 1 if empty_tiles % 2 == 0 else -1

    return (
        15 * position_score +
        80 * mobility_score +
        100 * corner_score +
        40 * stable_score +
        25 * parity +
        10 * frontier_score
    )
