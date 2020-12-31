def winner(board):
    """
    Returns the winner of the game, if there is one.

        [[EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

        winning indexes:
            Horizontally:
                [(0,0), (0,1), (0,2)],
                [(1,0), (1,1), (1,2)],
                [(2,0), (2,1), (2,2)],
            Vertically:
                [(0,0), (1,0), (2, 0)],
                [(0,1), (1,1), (2, 1)],
                [(0,2), (1,2), (2, 2)],
            Diagnolly:
                [(0, 0), (1, 1), (2, 2)],
                [(0, 2), (1, 1), (2, 0)]
    """
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

a = [['X', 'X', 'O'],
    ['O', 'X', 'X'],
    ['O', 'X', 'O']]

print(winner(a))
print(a[0][1])
