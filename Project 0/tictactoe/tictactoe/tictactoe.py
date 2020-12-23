"""
Tic Tac Toe Player
"""

import math
import copy

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

def letterCount(board):
    x_count = 0
    o_count = 0
    for i in board:
        for j in i:
            if(j == 'X'):
                x_count+=1
            elif(j == 'O'):
                o_count+=1
    return (x_count, o_count)



def player(board):
    """
    Returns player who has the next turn on a board. Assuming x always goes first
    """
    if(letterCount(board)[0] > letterCount(board)[1]):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    emp_slots = set()
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                emp_slots.add((i, j))
    
    # print("Available slots: ", emp_slots)
    return emp_slots


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    dup_board = copy.deepcopy(board)
    if(type(action)==tuple):
        dup_board[action[0]][action[1]] = player(dup_board)

    # for i in dup_board:
    #     print(i)
    
    return dup_board


def winner(board):
    """
    Returns the winner of the game, if there is one.

    """

    #     [[EMPTY, EMPTY, EMPTY],
    #     [EMPTY, EMPTY, EMPTY],
    #     [EMPTY, EMPTY, EMPTY]]

    #     winning indexes:
    #         Horizontally:
    #             [(0,0), (0,1), (0,2)],
    #             [(1,0), (1,1), (1,2)],
    #             [(2,0), (2,1), (2,2)],
    #         Vertically:
    #             [(0,0), (1,0), (2, 0)],
    #             [(0,1), (1,1), (2, 1)],
    #             [(0,2), (1,2), (2, 2)],
    #         Diagnolly:
    #             [(0, 0), (1, 1), (2, 2)],
    #             [(0, 2), (1, 1), (2, 0)]

    winning_index = [[(0,0), (0,1), (0,2)],
                    [(1,0), (1,1), (1,2)],
                    [(2,0), (2,1), (2,2)],
                    [(0,0), (1,0), (2, 0)],
                    [(0,1), (1,1), (2, 1)],
                    [(0,2), (1,2), (2, 2)],
                    [(0, 0), (1, 1), (2, 2)],
                    [(0, 2), (1, 1), (2, 0)]]
    won = None
    for i in range(8):
        for j in range(2):
            #print(board[winning_index[i][j][0]][winning_index[i][j][1]], " => ", board[winning_index[i][j+1][0]][winning_index[i][j+1][1]])
            if(board[winning_index[i][j][0]][winning_index[i][j][1]] != board[winning_index[i][j+1][0]][winning_index[i][j+1][1]]):
                break
            if(j >= 1):
                won = board[winning_index[i][j][0]][winning_index[i][j][1]]
                return won
    return won

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) is not None):
        return True
    #true if noone wins but the slots have been filled up
    for row in board:
        for slot in row:
            if slot==EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if(winner(board) == 'X'):
        return 1
    elif(winner(board) == 'O'):
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    c_player = 'X' if player(board)=='X' else 'O'
    #when AI is X
    if(c_player == 'X'):
        print(c_player)
        v = -99999
        for action in actions(board):
            if(utility(result(board, action)) > v):
                v = utility(result(board, action))
                to_take = action
        return (v, to_take)
    #when AI is O
    else:
        v = -99999
        for action in actions(board):
            if(utility(result(board, action))*-1 > v):
                v = utility(result(board, action))*-1
                to_take = action
        return (v, to_take)

def min_value(board):
    v = 9999
    c_player = 'X' if player(board)=='X' else 'O'
    #when AI is X
    if(c_player == 'X'):
        for action in actions(board):
            if(utility(result(result(board, action), action)) < v):
                v = utility(result(result(board, action), action))
                to_take = action
        return (v, to_take)
        #when AI is O
    else:
        for action in actions(board):
            if(utility(result(result(board, action), action))*-1 < v):
                v = utility(result(result(board, action), action))*-1
                to_take = action
        return (v, to_take)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # f_board = None
    c_player = 'X' if player(board)=='X' else 'O'
    if(c_player == 'X'):
        if(max_value(board)[0] > 0):
            return max_value(board)[1]
        else:
            return min_value(board)[1]
    else:
        if(max_value(board)[0] < 0):
            return max_value(board)[1]
        else:
            return min_value(board)[1]
