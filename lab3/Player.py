import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def make_mov(self, next_state, col, player_number):
        if(next_state[0][col] != 0):
            raise Exception("col full")
        for i in range(next_state.shape[0]-1, -1, -1):
            if next_state[i][col] == 0:
                next_state[i][col] = player_number
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
            self.make_mov(next_state, col, 1)
            actions.append(next_state)

        for a in actions:
            v = max(v, self.min_val(a, depth - 1, alpha, beta))
            alpha = max(alpha, v)
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
            self.make_mov(next_state, col, 2)
            actions.append(next_state)

        for a in actions:
            v = min(v, self.max_val(a, depth - 1, alpha, beta))
            beta = min(beta, v)
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
        depth = 5
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        result = valid_cols[0]
        best = -9999
        alpha = -9999
        beta = 9999
        best_board = board.copy()
        for i in range(len(valid_cols)):
            next_state = board.copy()
            self.make_mov(next_state, valid_cols[i], self.player_number)
            score = self.min_val(next_state, depth - 1, alpha, beta)
            if(score > best):
                result = valid_cols[i]
                best = score
                best_board = next_state
            alpha = max(alpha, score)
        
        #debugging
        return result
        #raise NotImplementedError('Whoops I don\'t know what to do')

    def chance(self, board, depth):
        if depth == 0:
            return self.evaluation_function(board)
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        if not valid_cols:
            return self.evaluation_function(board)
        
        actions = []
        for col in valid_cols:
            next_state = board.copy()
            self.make_mov(next_state, col, 2)
            actions.append(next_state)


        total = 0
        for a in actions:
            total += self.exp_max(a, depth - 1)

        return total/len(valid_cols)



    def exp_max(self, board, depth):
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
            self.make_mov(next_state, col, 1)
            actions.append(next_state)

        for a in actions:
            v = max(v, self.chance(a, depth - 1))

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
        depth = 5
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)
        result = valid_cols[0]
        best = -9999
        best_board = board.copy()
        for i in range(len(valid_cols)):
            next_state = board.copy()
            self.make_mov(next_state, valid_cols[i], self.player_number)
            score = self.chance(next_state, depth - 1)
            if(score > best):
                result = valid_cols[i]
                best = score
                best_board = next_state
        #debugging
        return result
        #raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):
        "float(-inf)"
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
        def scan_index(start):
            """
            THIS FUNCTION TAKES IN AN INDEX AND SCANS A SEGMENT OF 4 SLOTS IN ALL VALID DIRECTIONS

            Metrics:    Threat by One block -> 0.25; Two blocks -> 5;
                        Three blocks WITH immediate threat -> 100;
                        Three blocks WITHOUT immediate threat -> 25

                        Along with this, Three-block-threats from the opponent are given a lot more
                        'score' than three-block-threats from us, to make sure their threat is blocked.
            """
            vectors = [(0,1), (1,0), (1,1), (1, -1)] # horiz, vert, p.diag, s.diag
            one_score = 0.25
            two_score = 5
            three_score = 50
            for vector in vectors:
                end = (start[0] + 3*vector[0], start[1]+ 3*vector[1])
                if(end[0] < len(board) and end[1] < len(board[0])):
                    num_p1 = 0
                    num_p2 = 0
                    position_zero = start
                    for i in range(4): # iters through directions

                        if(board[start[0] + i * vector[0]][start[1] + i * vector[1]] == 1): num_p1+=1
                        elif(board[start[0] + i * vector[0]][start[1] + i * vector[1]] == 2): num_p2+=1
                        else: position_zero = (start[0] + i*vector[0], start[1] + i*vector[1])

                    if num_p1 == 4: return 1001
                    if num_p2 == 4: return -1001

                    if num_p2 == 0:
                        if num_p1 == 3: 
                            if(position_zero[0] == len(board)-1 or board[position_zero[0]+1][position_zero[1]] != 0): 
                                return three_score * (2 if self.player_number == 2 else 1)
                            else: 
                                return three_score * (0.5 if self.player_number == 2 else 0.25)

                        if num_p1 == 2: return two_score * (1.2 if self.player_number == 2 else 1)
                        if num_p1 == 1: return one_score
                    
                    if num_p1 == 0:
                        if num_p2 == 3:
                            if(position_zero[0] == len(board)-1 or board[position_zero[0]+1][position_zero[1]] != 0): 
                                return -1 * three_score * (2 if self.player_number == 2 else 1)
                            else: 
                                return -1 * three_score * (0.5 if self.player_number == 2 else 0.25)
                        if num_p2 == 2: return -1 * two_score * (1.2 if self.player_number == 1 else 1)
                        if num_p2 == 1: return -1 * one_score
            return 0



        utility = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                res = scan_index((i,j))
                if(abs(res) > 1000): # terminal state
                    return res
                utility+=res
        return utility
            


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

