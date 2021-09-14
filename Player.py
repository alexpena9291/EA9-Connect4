import numpy as np
import random
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        moves = 0
        player = 0
        maxEval = -1000
        maxCol = []
        minCol = []
        minEval = 1000
        nPlayer = 0
        alpha = -1000
        beta = 1000

        #Find out whose turn it is
        for col in range(0, 7):
            for row in range(5, -1, -1):
                if (board[row][col] != 0):
                    moves += 1
        if (moves % 2 == 0):
            player = 1
            nPlayer = 2
        else:
            player = 2
            nPlayer = 1

        #print("Player" + str(player))
        for col in range(0, 7):
            for row in range(5, -1, -1):
                if (board[row][col] == 0):
                    board[row][col] = player
                    if (self.game_completed(player, board)):
                        return col
                    eval = self.minimax(board, 5 + (moves // 14), alpha, beta, nPlayer)
                    board[row][col] = 0
                    #print ("Col : " + str(col) + " Row : " + str(row) + " Eval : " + str(eval))
                    if (eval >= maxEval):
                        if (eval > maxEval):
                            maxCol.clear()
                        maxEval = eval
                        maxCol.append(col)
                    if (eval <= minEval):
                        if (eval < minEval):
                            minCol.clear()
                        minEval = eval
                        minCol.append(col)
                    break
        #print ("\n")

        if (player == 1):
            return maxCol[random.randint(0, len(maxCol) - 1)]
        if (player == 2):
            return minCol[random.randint(0, len(minCol) - 1)]

    #Recursive alpha beta minimax algorithm
    def minimax(self, board, depth, alpha, beta, player):
        if (depth == 0):
            return self.evaluation_function(board, player)
        if (player == 1):
            if (self.game_completed(2, board)):
                return -50
            maxEval = -1000
            for col in range(0, 7):
                for row in range(5, -1, -1):
                    if (board[row][col] == 0):
                        board[row][col] = player
                        eval = self.minimax(board, depth - 1, alpha, beta, 2)
                        maxEval = max(maxEval, eval)
                        alpha = max(alpha, eval)
                        board[row][col] = 0
                        break
                if (beta <= alpha):
                    break
            return maxEval
        if (player == 2):
            if (self.game_completed(1, board)):
                return 50
            minEval = 1000
            for col in range(0, 7):
                for row in range(5, -1, -1):
                    if (board[row][col] == 0):
                        board[row][col] = player
                        eval = self.minimax(board, depth - 1, alpha, beta, 1)
                        minEval = min(minEval, eval)
                        beta = min(beta, eval)
                        board[row][col] = 0
                        break
                if (beta <= alpha):
                    break
            return minEval


    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        raise NotImplementedError('Whoops I don\'t know what to do')


    def game_completed(self, player_num, board):
        """Returns True if player_num is in a winning position on the gameboard"""
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b

                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))


    def check_three(self, player_num, board):
        """Returns the number of potential connect 4s possible for a given player"""
        threeStrings = ['0{0}{0}{0}'.format(player_num),
        '{0}0{0}{0}'.format(player_num),
        '{0}{0}0{0}'.format(player_num),
        '{0}{0}{0}0'.format(player_num)]
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            threeCount = 0
            for row in b:
                for threeStr in threeStrings:
                    if threeStr in to_str(row):
                        threeCount += 1
            return threeCount

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            threeCount = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b

                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                for threeStr in threeStrings:
                    if threeStr in to_str(root_diag):
                        threeCount += 1

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        for threeStr in threeStrings:
                            if threeStr in diag:
                                threeCount += 1

            return threeCount

        return (check_horizontal(board) +
                check_verticle(board) +
                check_diagonal(board))


    def evaluation_function(self, board, player):
        """
        Given the current stat of the board, return the scalar value that
        represents the evaluation function for the current player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        evalCount = 0
        evalCount += self.check_three(1, board)
        evalCount -= self.check_three(2, board)

        return evalCount



class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move
