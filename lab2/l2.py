# Filename: l2.py

# Constant costs for yantra and exit cells
YANTRA_COST = 0
EXIT_COST = 0
TRAP_COST = 99999

class YantraCollector:
    """
    YantraCollector class to solve the yantra collection puzzle with cost-based movement.
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
        ## use these variables if needed
        self.collected_yantras = 0
        self.total_frontier_nodes = 0
        self.total_explored_nodes = 0
        self.total_cost = 0
        self.cost_map = self.initialize_cost_map()
        
    def initialize_cost_map(self):
        """
        Initializes a dictionary mapping each position to its movement cost.
        """
        cost_map = {}
        for i in range(self.n):
            for j in range(self.n):
                cell_value = self.grid[i][j]
                if isinstance(cell_value, int):  
                    cost_map[(i, j)] = cell_value
                elif cell_value == 'P':
                    cost_map[(i, j)] = 0
                elif cell_value.startswith('Y'):  
                    cost_map[(i, j)] = YANTRA_COST
                elif cell_value == 'E':  
                    cost_map[(i, j)] = EXIT_COST
                elif cell_value == 'T':
                    cost_map[(i, j)] = TRAP_COST 
                # Walls ('#') are ignored, no need to assign them a cost.
        return cost_map
    
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
                if isinstance(self.grid[i][j], str) and self.grid[i][j].startswith('Y'):
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

        return self.revealed_yantra

    def goal_test(self, position):
        """
        Checks if the given position matches the currently revealed yantra or exit.

        Args:
            position (tuple): The current position to check.

        Returns:
            bool: True if position matches revealed_yantra, False otherwise.
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
        Each move has an associated movement cost, with yantras and exit having a fixed cost.

        Args:
            position (tuple): The current position (row, col).

        Returns:
            list: A list of neighboring positions [(row, col), ...]. 
                  should include all valid neighbors in the expected order.
        """
        # pass  # TO DO 
        tup = []
        # north
        if position[0]-1 >= 0 and position[1] >= 0 and self.grid[position[0]-1][position[1]] != '#':
                tup.append((position[0]-1, position[1]))
        #east
        if position[0] < self.n and position[1]+1 < self.n and self.grid[position[0]][position[1]+1] != '#':
                tup.append((position[0], position[1]+1))
        #south
        if position[0]+1 < self.n and position[1] < self.n and self.grid[position[0]+1][position[1]] != '#':
                tup.append((position[0]+1, position[1]))
        #west
        if position[0] >= 0 and position[1]-1 >= 0 and self.grid[position[0]][position[1]-1] != '#':
                tup.append((position[0], position[1]-1))
        return tup
    
    def sort_to_priority(self, Front):
        for i in range(0,len(Front)):
            for j in range(0,len(Front)-i-1):
                if Front[j][0] > Front[j+1][0]:
                    temp = Front[j+1]
                    Front[j+1] = Front[j]
                    Front[j] = temp
        return Front
            

    def ucs(self, start, goal):
        """
        Performs Uniform Cost Search (UCS) to find the path to the goal.
        Args:''
            start (tuple): The starting position.
            goal (tuple): The goal position.
        Returns:
            tuple: (path, frontier_count, explored_count, path_cost)
                   - path: List of tuples representing the path from start to goal.
                   - frontier_count: Number of nodes in the frontier list at the time of exiting the function.
                   - explored_count: Number of nodes in the explored list at the time of exiting the function.
                   - path_cost: Total cost of the path.
    # pass  # TO DO 
        """
        i = 0
        Exp = []
        Front = [(0, start, [start])]
        explored_set = set()
        cost = 0
        while(Front):
            self.sort_to_priority(Front);
            cum_cost, node, path = Front.pop(0)
            if self.goal_test(node):
                Exp.append(node)
                self.total_frontier_nodes = len(Front)
                self.total_explored_nodes = len(Exp)
                self.reveal_next_yantra_or_exit()
                return path, self.total_frontier_nodes, self.total_explored_nodes, cum_cost
            Exp.append(node)
            explored_set.add(node)
            for neighbor in self.get_neighbors(node):
                infront = 0
                if neighbor not in explored_set:
                    for n in Front:
                        if neighbor == n[1]:
                            infront = 1
                    if infront == 0:
                        new_cost = cum_cost + self.cost_map[neighbor]
                        Front.append((new_cost, neighbor, path + [neighbor]))

        return None, 0, 0

    def heuristic(self, position, goal):
        """
        Defines a heuristic function to estimate the cost from the current position to the goal-not necessarily admissible.

        Args:
            position (tuple): The current position.
            goal (tuple): The goal position.
        Returns:
            int: The estimated cost to the goal.
        """
        # pass  # TO DO
        import math
        x =  position[0] + goal[0]
        y = goal[1] + position[1]
        x = x//2
        y = y//2
        px = position[0]
        py = position[1]
        gx = goal[0]
        gy = goal[1]
        rx = math.sin(x)**2+math.cos(px)**2 - gx
        ry = math.sin(y)**2+math.cos(py)**2 - gy
         
        return x**2 + y**2

    def gbfs(self, start, goal):
        """
        Performs Greedy Best-First Search (GBFS) to find the path to the goal.

        Returns:
            tuple: (path, frontier_count, explored_count, path_cost)
                   - path: List of tuples representing the path from start to goal.
                   - frontier_count: Number of nodes in the frontier list at the time of exiting the function.
                   - explored_count: Number of nodes in the explored list at the time of exiting the function.
                   - path_cost: Total cost of the path.
        """
        Exp = []
        Front = [(self.heuristic(start, goal), start, [start], 0)]
        explored_set = set()
        while(Front):
            self.sort_to_priority(Front);
            heu_cost, node, path, curr_cost = Front.pop(0)
            if self.goal_test(node):
                Exp.append(node)
                self.total_frontier_nodes = len(Front)
                self.total_explored_nodes = len(Exp)
                self.reveal_next_yantra_or_exit()
                return path, self.total_frontier_nodes, self.total_explored_nodes, curr_cost
            Exp.append(node)
            explored_set.add(node)
            for neighbor in self.get_neighbors(node):
                infront = 0
                if neighbor not in explored_set:
                    for n in Front:
                        if neighbor == n[1]:
                            infront = 1
                    if infront == 0:
                        new_heu_cost = self.heuristic(neighbor, goal)
                        new_curr_cost = curr_cost + self.cost_map[neighbor]
                        Front.append((new_heu_cost, neighbor, path + [neighbor], new_curr_cost))

        return None, 0, 0, 0

    def a_star(self, start, goal):
        """
        Performs A* Search to find the optimal path to the goal.

        Returns:
            tuple: (path, frontier_count, explored_count, path_cost)
                   - path: List of tuples representing the path from start to goal.
                   - frontier_count: Number of nodes in the frontier list at the time of exiting the function.
                   - explored_count: Number of nodes in the explored list at the time of exiting the function.
                   - path_cost: Total cost of the path.
        """
        # pass  # TO DO 
        i = 0
        Exp = []
        Front = [(0+self.heuristic(start, goal), start, [start], 0)]
        explored_set = set()
        cost = 0
        while(Front):
            self.sort_to_priority(Front);
            heu_cost, node, path, curr_cost = Front.pop(0)
            if self.goal_test(node):
                Exp.append(node)
                self.total_frontier_nodes = len(Front)
                self.total_explored_nodes = len(Exp)
                self.reveal_next_yantra_or_exit()
                return path, self.total_frontier_nodes, self.total_explored_nodes, curr_cost
            Exp.append(node)
            explored_set.add(node)
            for neighbor in self.get_neighbors(node):
                infront = 0
                if neighbor not in explored_set:
                    for n in Front:
                        if neighbor == n[1]:
                            infront = 1
                    if infront == 0:
                        new_curr_cost = curr_cost + self.cost_map[neighbor]
                        new_heu_cost = new_curr_cost + self.heuristic(neighbor, goal)
                        Front.append((new_heu_cost, neighbor, path + [neighbor], new_curr_cost))

        return None, 0, 0, 0

    def solve(self, strategy):
        """
        Solves the yantra collection puzzle using the specified strategy.

        Args:
            strategy (str): The search strategy to use ("UCS", "GBFS", "A*").

        Returns:
            tuple: (full_path, total_frontier_nodes, total_explored_nodes, total_cost)
                   - full_path: List of tuples representing the full path to collect all yantras and exit.
                   - total_frontier_nodes: Sum of frontier_count across all searches.
                   - total_explored_nodes: Sum of explored_count across all searches.
                   - total_cost: Total cost of the path.
        """
        # pass  # TO DO 
        i=0
        front_nodes = 0
        exp_nodes = 0
        tot_cost = 0
        path = []
        Y = [self.start]
        S = self.find_all_yantras()
        for i in range(1, len(S)+1):
            Y.append(S[i])
        Y.append(self.find_position('E'))
        for i in range(0, len(Y)-1):
            if(strategy == 'UCS'):
                P, fron, exp, cost = self.ucs(Y[i], Y[i+1])
            elif(strategy == 'GBFS'):
                P, fron, exp, cost = self.gbfs(Y[i], Y[i+1])
            elif(strategy == 'A*'):
                P, fron, exp, cost = self.a_star(Y[i], Y[i+1])
            if(Y[-1] != P[-1]):
                P.remove(P[-1])
            path.extend(P)
            front_nodes += fron
            exp_nodes += exp
            tot_cost += cost
        return path, front_nodes, exp_nodes, tot_cost

if __name__ == "__main__":
    grid = [
        ['P', 2, '#', 5, 'Y2'],
        ['T', 2, 3, '#', 1],
        [0, 7, 'Y1', 4, 2],
        ['#', 'T', 2, 1, 3],
        [1, 3, 0, 2, 'E']
    ]

    game = YantraCollector(grid)
    strategy = "UCS"  # or "A*" or "GBFS"
    result = game.solve(strategy)
    
    if result:
        full_path, total_frontier_nodes, total_explored_nodes, total_cost = result
        print("Path:", full_path)
        print("Total Frontier Nodes:", total_frontier_nodes)
        print("Total Explored Nodes:", total_explored_nodes)
        print("Total Cost:", total_cost)
    else:
        print("No solution found.")
