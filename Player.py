import numpy as np
import time

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
        raise NotImplementedError('Whoops I don\'t know what to do')

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
        startTime = time.time()

        def expectimax(is_max, currDepth, board):
            if currDepth == 4:
                #print('D: ', currDepth, ' eval: ', self.evaluation_function(board))
                enemyPlayer = (1 if self.player_number == 2 else 2)
                return self.eval2(self.player_number, board) - self.eval2(enemyPlayer, board)
            if is_max:
                maxEval = 0
                for loc in self.get_next_possible_moves(board):
                    board[loc[0], loc[1]] = self.player_number
                    val = expectimax(False, currDepth + 1, board)
                    if val > maxEval:
                        maxEval = val
                    board[loc[0], loc[1]] = 0
                return maxEval
            else: 
                count = 0
                total = 0
                for loc in self.get_next_possible_moves(board):
                    count += 1
                    board[loc[0], loc[1]] = (2 if self.player_number == 1 else 1)
                    total += expectimax(True, currDepth + 1, board)
                    board[loc[0], loc[1]] = 0
                return total / count
        
        nextMoves = self.get_next_possible_moves(board)
        col = nextMoves[0][1]
        currentBest = 0
        for move in nextMoves:
            board[move[0], move[1]] = self.player_number
            val = expectimax(False, 0, board)
            if val > currentBest:
                currentBest = val
                col = move[1]
            board[move[0], move[1]] = 0

        return col



    def evaluation_function(self, board):
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


        visited = set()

        """
        Recursive function to process chunks. 
        """




    def get_next_possible_moves(self, board):
        possiblePlaces = []
        for i in range(len(board[0])):
            for j in range(len(board) - 1, -1, -1):
                if board[j, i] == 0:
                    possiblePlaces.append((j, i))
                    break
        return possiblePlaces

    def valid_location(self, x, y):
        if x > 5 or x < 0:
            return False
        if y > 6 or y < 0:
            return False
        return True


    


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

