# Filename: l1.py

class YantraCollector:
    """
    YantraCollector class to solve the yantra collection puzzle.
    The player must collect all yantras sequentially and reach the exit.
    """
    
    def __init__(self, grid):
        """
        Initializes the game with the provided grid.

        Args:
            grid (list of list of str): The grid representing the puzzle.
        """
        self.grid = grid
        self.n = len(grid)
        self.start = self.find_position('P')
        self.exit = None
        self.yantras = self.find_all_yantras()
        self.revealed_yantra = self.find_position('Y1')
        self.collected_yantras = 0
        self.total_frontier_nodes = 0
        self.total_explored_nodes = 0
        
    def find_position(self, symbol):
        """
        Finds the position of a given symbol in the grid.

        Args:
            symbol (str): The symbol to locate.

        Returns:
            tuple or None: The position of the symbol, or None if not found.
        """
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == symbol:
                    return (i, j)
        return None

    def find_all_yantras(self):
        """
        Finds and stores the positions of all yantras in the grid.

        Returns:
            dict: A dictionary mapping yantra numbers to their positions.
        """
        positions = {}
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j].startswith('Y'):
                    positions[int(self.grid[i][j][1:])] = (i, j)
                elif self.grid[i][j] == 'E':
                    self.exit = (i, j)
        return positions

    def reveal_next_yantra_or_exit(self):
        """
        Reveals the next yantra in sequence or the exit when all yantras are collected.
        """
        self.collected_yantras += 1
        if self.collected_yantras + 1 in self.yantras:
            self.revealed_yantra = self.yantras[self.collected_yantras + 1]
        elif self.collected_yantras == len(self.yantras):
            self.revealed_yantra = self.exit
        else:
            self.revealed_yantra = None

    def goal_test(self, position):
        """
        Checks if the given position matches the currently revealed yantra or exit.

        Args:
            position (tuple): The current position to check.
        """
        # pass  # TO DO
        x1 = self.revealed_yantra[0]
        y1 = self.revealed_yantra[1]
        if self.grid[position[0]][position[1]] == self.grid[x1][y1]:
                return True
        else:
                return False

    def get_neighbors(self, position):
        """
        Generates valid neighboring positions for the given position.

        Args:
            position (tuple): The current position of the player.
        """
        # pass  # TO DO
        tup = []
        # north
        if position[0]-1 >= 0 and position[1] >= 0 and self.grid[position[0]-1][position[1]] != '#' and self.grid[position[0]-1][position[1]] != 'T':
                tup.append((position[0]-1, position[1]))
        #east
        if position[0] < self.n and position[1]+1 < self.n and self.grid[position[0]][position[1]+1] != '#' and self.grid[position[0]][position[1]+1] != 'T':
                tup.append((position[0], position[1]+1))
        #south
        if position[0]+1 < self.n and position[1] < self.n and self.grid[position[0]+1][position[1]] != '#' and self.grid[position[0]+1][position[1]] != 'T':
                tup.append((position[0]+1, position[1]))
        #west
        if position[0] >= 0 and position[1]-1 >= 0 and self.grid[position[0]][position[1]-1] != '#' and self.grid[position[0]][position[1]-1] != 'T':
                tup.append((position[0], position[1]-1))
        return tup

    def bfs(self, start, goal):
        """
        Performs Breadth-First Search (BFS) to find the path to the goal.

        Args:
            start (tuple): The starting position.
            goal (tuple): The goal position.
        """
        # pass  # TO DO
        i = 0
        Exp = [start]
        Front = []
        paths = [[start]]
        while(Exp[i] != self.revealed_yantra):
            S = self.get_neighbors(Exp[i])
            for j in S:
                if j not in Exp and j not in Front:
                    Front.append(j)
            for l in paths:
                if l[-1] == Exp[i]:
                    pte = l
            for k in S:
                temp = pte + [k]
                paths.append(temp)
            paths.remove(pte)
            Exp.append(Front[0])
            Front.pop(0)
            i += 1
        for i in paths:
            if i[-1] == self.revealed_yantra:
                path = i
        if path == []:
            return None, 0, 0
        self.total_frontier_nodes = len(Front)
        self.total_explored_nodes = len(Exp)
        self.reveal_next_yantra_or_exit()
        return path, self.total_frontier_nodes, self.total_explored_nodes
    
    def dfs(self, start, goal):
        """
        Performs Depth-First Search (DFS) to find the path to the goal.

        Args:
            start (tuple): The starting position.
            goal (tuple): The goal position.
        """
        # pass  # TO DO
        i = 0
        Exp=[start]
        Front = []
        paths = [[start]]
        A=[]
        while(Exp[i] != self.revealed_yantra):
            S = self.get_neighbors(Exp[i])
            for j in reversed(S):
                if j not in Exp and j not in Front:
                    Front.insert(0, j)
            for l in paths:
                if l[-1] == Exp[i]:
                    pte = l
            for k in S:
                temp = pte + [k]
                paths.append(temp)
            paths.remove(pte)
            Exp.append(Front[0])
            Front.pop(0)
            i += 1
        for i in paths:
            if i[-1] == self.revealed_yantra:
                path = i
        if path == []:
            return None, 0, 0
        self.total_frontier_nodes = len(Front)
        self.total_explored_nodes = len(Exp)
        self.reveal_next_yantra_or_exit()
        return path, self.total_frontier_nodes, self.total_explored_nodes

    def solve(self, strategy):
        """
        Solves the yantra collection puzzle using the specified strategy.

        Args:
            strategy (str): The search strategy (BFS or DFS).
        """
        # pass  # TO DO
        i=0
        front_nodes = 0
        exp_nodes = 0
        path = []
        Y = [self.start]
        S = self.find_all_yantras()
        for i in range(1, len(S)+1):
            Y.append(S[i])
        Y.append(self.find_position('E'))
        for i in range(0, len(Y)-1):
            if(strategy == 'BFS'):
                P, fron, exp = self.bfs(Y[i], Y[i+1])
            elif(strategy == 'DFS'):
                P, fron, exp = self.dfs(Y[i], Y[i+1])
            if(Y[-1] != P[-1]):
                P.remove(P[-1])
            path.extend(P)
            front_nodes += fron
            exp_nodes += exp
        return path, front_nodes, exp_nodes


if __name__ == "__main__":
    grid = [
        ['P', '.', '.', '#', 'Y2'],
        ['#', 'T', '.', '#', '.'],
        ['.', '.', 'Y1', '.', '.'],
        ['#', '.', '.', 'T', '.'],
        ['.', '.', '.', '.', 'E']
    ]

    game = YantraCollector(grid)
    strategy = "BFS" # or "DFS"
    solution, total_frontier, total_explored = game.solve(strategy)
    if solution:
        print("Solution Path:", solution)
        print("Total Frontier Nodes:", total_frontier)
        print("Total Explored Nodes:", total_explored)
    else:
        print("No solution found.")
