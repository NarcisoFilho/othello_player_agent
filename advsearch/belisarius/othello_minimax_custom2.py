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

def evaluate_custom(state, player: str) -> float:
    board = state.board.tiles
    opponent = 'W' if player == 'B' else 'B'

    score = 0
    player_tiles = 0
    opponent_tiles = 0
    player_moves = len(state.actions)

    # Inverter jogador para estimar mobilidade do oponente
    opponent_state = state.copy()
    opponent_state.player = opponent
    opponent_moves = len(opponent_state.actions)

    # Posicional, Canto, Estabilidade, Fronteira
    position_score = 0
    corner_score = 0
    stable = 0
    frontier = 0

    directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece == '.':
                continue
            # Positional score
            mult = 1 if piece == player else -1
            position_score += EVAL_TEMPLATE[y][x] * mult

            # Tile count
            if piece == player:
                player_tiles += 1
            else:
                opponent_tiles += 1

            # Corner control
            if (x, y) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                corner_score += mult

            # Frontier discs (penalizar)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == '.':
                    frontier += mult
                    break

            # Estabilidade (simples): cantos e bordas protegidas
            if (x in [0, 7] or y in [0, 7]) and piece == player:
                stable += 1

    # Mobilidade normalizada
    mobility_score = 0
    total_moves = player_moves + opponent_moves
    if total_moves > 0:
        mobility_score = 100 * (player_moves - opponent_moves) / total_moves

    # Paridade (jogador que joga por último tem vantagem)
    empty_squares = sum(row.count('.') for row in board)
    parity = 1 if empty_squares % 2 == 0 else -1

    # Combinação ponderada dos fatores
    return (
        15 * position_score +
        80 * mobility_score +
        1000 * corner_score +
        50 * stable +
        -25 * frontier +
        10 * parity
    )
