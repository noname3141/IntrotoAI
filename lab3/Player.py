import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def make_mov(self, next_state, col):
        if(next_state[0][col] != 0):
            raise Exception("col full")
        for i in range(next_state.shape[0]-1, -1, -1):
            if next_state[i][col] == 0:
                next_state[i][col] = self.player_number
                break

    def max_val(self, board, depth, alpha, beta):
        if depth == 0:
            return self.evaluation_function(board)
        v = -9999
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        if not valid_cols:
            return self.evaluation_function(board)

        actions = []
        for col in valid_cols:
            next_state = board.copy()
            self.make_mov(next_state, col)
            actions.append(next_state)

        for a in actions:
            v = max(v, self.min_val(a, depth - 1, alpha, beta))
            if alpha >= beta:
                break

        return v
    
    def min_val(self, board, depth, alpha, beta):
        if depth == 0:
            return self.evaluation_function(board)
        v = 9999
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        if not valid_cols:
            return self.evaluation_function(board)

        actions = []
        for col in valid_cols:
            next_state = board.copy()
            self.make_mov(next_state, col)
            actions.append(next_state)

        for a in actions:
            v = min(v, self.max_val(a, depth - 1, alpha, beta))
            if alpha >= beta:
                break

        return v

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
        depth = 7
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        result = valid_cols[0]
        best = -9999
        alpha = -9999
        beta = 9999
        for i in range(len(valid_cols)):
            next_state = board.copy()
            self.make_mov(next_state, valid_cols[i])
            score = self.min_val(next_state, depth - 1, alpha, beta)
            if(score > best):
                result = valid_cols[i]
                best = score
        return result
        #raise NotImplementedError('Whoops I don\'t know what to do')

    def chance(self, board, depth):
        if depth == 0:
            return self.evaluation_function(board)
        depth  -= 1
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        if not valid_cols:
            return self.evaluation_function(board)
        
        actions = []
        for col in valid_cols:
            next_state = board.copy()
            self.make_mov(next_state, col)
            actions.append(next_state)


        total = 0
        for a in actions:
            total += self.exp_max(a, depth)

        return total/len(valid_cols)



    def exp_max(self, board, depth):
        if depth == 0:
            return self.evaluation_function(board)
        v = -9999
        depth -= 1
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        if not valid_cols:
            return self.evaluation_function(board)

        actions = []
        for col in valid_cols:
            next_state = board.copy()
            self.make_mov(next_state, col)
            actions.append(next_state)

        for a in actions:
            v = max(v, self.chance(a, depth))

        return v

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
        depth = 7
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        result = valid_cols[0]
        best = -9999
        for i in range(len(valid_cols)):
            next_state = board.copy()
            self.make_mov(next_state, valid_cols[i])
            score = self.chance(next_state, depth - 1)
            if(score > best):
                result = valid_cols[i]
                best = score
        return result
            
        #raise NotImplementedError('Whoops I don\'t know what to do')




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
        return 0


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

