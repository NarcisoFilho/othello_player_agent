import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move


EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [6,    1, 1, 1, 1, 1, 1,   6],
    [2,    1, 1, 3, 3, 1, 1,   2],
    [2,    1, 1, 3, 3, 1, 1,   2],
    [6,    1, 1, 1, 1, 1, 1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def make_move(state) -> Tuple[int, int]:
    return minimax_move(state, 4, evaluate_custom)

def evaluate_custom(state, player: str) -> float:
    """
    Avalia estado com base em:
    - diferença de peças,
    - mobilidade,
    - controle de cantos,
    - valor posicional das peças.
    """
    board = state.board.tiles
    opponent = 'W' if player == 'B' else 'B'

    piece_count = 0
    position_score = 0
    corner_score = 0

    player_moves = len(state.actions)
    # gerar estado do oponente para contar mobilidade dele
    opponent_state = state.copy()
    opponent_state.player = opponent
    opponent_moves = len(opponent_state.actions)

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece == player:
                piece_count += 1
                position_score += EVAL_TEMPLATE[y][x]
            elif piece == opponent:
                piece_count -= 1
                position_score -= EVAL_TEMPLATE[y][x]

    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for x, y in corners:
        if board[y][x] == player:
            corner_score += 1
        elif board[y][x] == opponent:
            corner_score -= 1

    # Pesos para cada fator da heurística
    piece_weight = 10
    mobility_weight = 80
    position_weight = 15
    corner_weight = 100

    mobility_value = 0
    if player_moves + opponent_moves != 0:
        mobility_value = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)

    return (
        piece_weight * piece_count +
        mobility_weight * mobility_value +
        position_weight * position_score +
        corner_weight * corner_score
    )