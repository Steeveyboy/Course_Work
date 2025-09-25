"""
Tic Tac Toe Player
"""

import math
import random
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                yield (i, j)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i].count(board[i][0]) == len(board) and board[i][0] is not EMPTY:
            return board[i][0]
    
    
    for j in range(len(board)):
        column = [row[j] for row in board]
        if column.count(column[0]) == len(board) and column[0] is not EMPTY:
            return column[0]
        
    diagonal = [board[i][i] for i in range(len(board))]
    other_diagonal = [board[-i-1][i] for i in range(len(board))]
    
    if diagonal.count(diagonal[0]) == len(board) and diagonal[0] is not EMPTY:
        return diagonal[0]
    
    if other_diagonal.count(other_diagonal[0]) == len(board) and other_diagonal[0] is not EMPTY:
        return other_diagonal[0]
    
    return None    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    if all(cell != EMPTY for row in board for cell in row):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    
def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = -2
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = 2
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)
    
    current_player = player(board)
    
    if current_player == X:
        best_action = None
        best_score = -2
        for action in actions(board):
            util = min_value(result(board, action))
            if util > best_score:
                best_action = action
                best_score = util
        return best_action

    else:
        best_action = None
        best_score = 2
        for action in actions(board):
            util = max_value(result(board, action))
            if util < best_score:
                best_action = action
                best_score = util
        return best_action

