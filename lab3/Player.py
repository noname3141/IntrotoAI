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
            self.make_mov(next_state, valid_cols[i])
            score = self.min_val(next_state, depth - 1, alpha, beta)
            if(score > best):
                result = valid_cols[i]
                best = score
                best_board = next_state
        
        #debugging
        for i in range(board.shape[0]):
            s = ""
            for j in range(board.shape[1]):
                s += str(best_board[i][j]) + " "
            print(s)
            print()
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
            self.make_mov(next_state, valid_cols[i])
            score = self.chance(next_state, depth - 1)
            if(score > best):
                result = valid_cols[i]
                best = score
                best_board = next_state
        #debugging
        for i in range(board.shape[0]):
            s = ""
            for j in range(board.shape[1]):
                s += str(best_board[i][j]) + " "
            print(s)
            print()
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
        utility = 0

        num_ones_1 = 0
        num_twos_1 = 0
        num_threes_1 = 0

        num_ones_2 = 0
        num_twos_2 = 0
        num_threes_2 = 0

        one_val = 1
        two_val = 10
        three_val = 100
        three_one_val = 10
        two_one_val = 2
        three_two_val = 5
        to_str = lambda a: ''.join(a.astype(str))

        player1_win_str = '1111'
        player2_win_str = '2222'

        player1_3_str = ['0111', '1011', '1101', '1110']
        player1_2_str = ['1100', '0110', '0011', '1010', '0101', '1001']
        player1_1_str = ['1000', '0100', '0010', '0001']
       
        player2_3_str = ['0222', '2022', '2202', '2220']
        player2_2_str = ['2200', '0220', '0022', '2020', '0202', '2002']
        player2_1_str = ['2000', '0200', '0020', '0002']

        '''
        HORIZONTAL CHECKS
        '''
        for row in board:
            strrow = to_str(row)
            if strrow == '0000000':
                continue
            if player1_win_str in strrow:
                #print("1 win state horiz")
                return 1001
            if player2_win_str in strrow:
                #print("2 win state horiz")
                return -1001
            for arrangement in player1_1_str:
                if arrangement in strrow:
                    num_ones_1+=1
            for arrangement in player2_1_str:
                if arrangement in strrow:
                    num_ones_2-=1
            for arrangement in player1_2_str:
                if arrangement in strrow:
                    num_twos_1+=1
            for arrangement in player2_2_str:
                if arrangement in strrow:
                    num_twos_2+=1
            for arrangement in player1_3_str:
                if arrangement in strrow:
                    num_threes_1+=1
            for arrangement in player2_3_str:
                if arrangement in strrow:
                    num_threes_2+=1

        '''
        VERTICAL CHECKS
        '''
        for row in board.T:
            strrow = to_str(row)
            if player1_win_str in strrow:
                #print("1 win state vert")
                return 1001
            if player2_win_str in strrow:
                #print("2 win state vert")
                return -1001
            if '0111' in strrow:
                num_threes_1+=1
                continue
            if '0222' in strrow:
                num_threes_2+=1
                continue
            if '0011' in strrow:
                num_twos_1+=1
                continue
            if '0022' in strrow:
                num_twos_2+=1
                continue
            if '0001' in strrow:
                num_ones_1+=1
                continue
            if '0002' in strrow:
                num_ones_2-=1
                continue

        '''
        DIAGONAL CHECKS
        '''

        for op in [None, np.fliplr]:
            op_board = op(board) if op else board
            
            root_diag = np.diagonal(op_board, offset=0).astype(int)
            strrow = to_str(root_diag)


            if player1_win_str in strrow:
                #print("1 win state diag")
                return 1001
            if player2_win_str in strrow:
                #print("2 win state diag")
                return -1001
            for arrangement in player1_1_str:
                if arrangement in strrow:
                    num_ones_1+=1
            for arrangement in player2_1_str:
                if arrangement in strrow:
                    num_ones_2-=1
            for arrangement in player1_2_str:
                if arrangement in strrow:
                    num_twos_1+=1
            for arrangement in player2_2_str:
                if arrangement in strrow:
                    num_twos_2+=1
            for arrangement in player1_3_str:
                if arrangement in strrow:
                    num_threes_1+=1
            for arrangement in player2_3_str:
                if arrangement in strrow:
                    num_threes_2+=1

            for i in range(1, board.shape[1]-3):
                for offset in [i, -i]:
                    diag = np.diagonal(op_board, offset=offset)
                    diag = to_str(diag.astype(int))
                    if player1_win_str in diag:
                        return 1001
                    if player2_win_str in strrow:
                        return -1001
                        #for arrangement in player1_1_str:
                        #    if arrangement in strrow:
                        #        num_ones_1+=1
                        #for arrangement in player2_1_str:
                        #    if arrangement in strrow:
                        #        num_ones_2-=1
                        #for arrangement in player1_2_str:
                        #    if arrangement in strrow:
                        #        num_twos_1+=1
                        #for arrangement in player2_2_str:
                        #    if arrangement in strrow:
                        #        num_twos_2+=1
                    for arrangement in player1_3_str:
                        if arrangement in strrow:
                            num_threes_1+=1
                    for arrangement in player2_3_str:
                        if arrangement in strrow:
                            num_threes_2+=1


        utility =   (num_ones_1 * one_val) + \
                    (num_twos_1 * two_val) + \
                    (num_threes_1 * three_val) + \
                    ((num_threes_1 * num_twos_2) * three_two_val) + \
                    ((num_twos_1 * num_ones_2) * two_one_val) + \
                    ((num_threes_1 * num_ones_2) * three_one_val)
        utility -=   (num_ones_2 * one_val) + \
                    (num_twos_2 * two_val) + \
                    (num_threes_2 * three_val) + \
                    ((num_threes_2 * num_twos_1) * three_two_val) + \
                    ((num_twos_2 * num_ones_1) * two_one_val) + \
                    ((num_threes_2 * num_ones_1) * three_one_val)

        #print(utility)
        return utility
        #return 0


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

