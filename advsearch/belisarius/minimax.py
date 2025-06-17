import random
from typing import Tuple, Callable



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    player = state.player # jogador na raiz

    def alphabeta(current_state, depth, alpha, beta, maximizing_player):
        if current_state.is_terminal() or (max_depth != -1 and depth == max_depth):
            return eval_func(current_state, player)

        actions = current_state.get_actions()
        successors = current_state.get_successors(actions)

        if maximizing_player:
            value = float('-inf')
            for child in successors:
                value = max(value, alphabeta(child, depth + 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break   # poda alpha
            return value
        else:
            value = float('inf')
            for child in successors:
                value = min(value, alphabeta(child, depth + 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # poda beta
            return value 

    best_value = float('-inf')
    best_move = None
    actions = state.get_actions()
    successors = state.get_successors(actions)

    for action, successor in zip(actions, successors):
        value = alphabeta(successor, 1, float('-inf'), float('inf'), False)
        if value > best_value:
            best_value = value
            best_move = action

    # fallback caso nenhuma jogada tenha sido selecionada
    if best_move is None and actions:
        best_move = random.choice(actions)

    return best_move
