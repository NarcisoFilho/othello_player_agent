import random
from typing import Tuple, Callable

def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:
    """
    Retorna a melhor jogada usando Minimax com poda alfa-beta.
    :param state: estado atual (GameState)
    :param max_depth: profundidade máxima (-1 = ilimitada)
    :param eval_func: função de avaliação (state, player) -> valor
    :return: tupla (x, y) com a melhor jogada
    """
    player = state.player

    def alphabeta(current_state, depth, alpha, beta, maximizing_player):
        # Caso terminal ou corte por profundidade
        if current_state.is_terminal():
            return eval_func(current_state, player)

        if max_depth != -1 and depth >= max_depth:
            return eval_func(current_state, player)

        actions = current_state.legal_moves()
        if not actions:
            return eval_func(current_state, player)

        successors = [current_state.next_state(a) for a in actions]

        # Segurança: remove estados nulos ou repetidos
        successors = [s for s in successors if s is not None and s != current_state]
        if not successors:
            return eval_func(current_state, player)

        if maximizing_player:
            value = float('-inf')
            for child in successors:
                value = max(value, alphabeta(child, depth + 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # poda beta
            return value
        else:
            value = float('inf')
            for child in successors:
                value = min(value, alphabeta(child, depth + 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # poda alfa
            return value

    # Movimento raiz
    actions = state.legal_moves()
    if not actions:
        return (1, 1)  # fallback seguro

    successors = [state.next_state(a) for a in actions]
    successors = [s for s in successors if s is not None and s != state]
    if not successors:
        return random.choice(actions)

    best_value = float('-inf')
    best_move = None

    for action, successor in zip(actions, successors):
        value = alphabeta(successor, 1, float('-inf'), float('inf'), False)
        if value > best_value:
            best_value = value
            best_move = action

    return best_move if best_move else random.choice(actions)