import copy
import re
from typing import Dict, List, Optional, Tuple


class Solver:
    def __init__(self):
        pass

    def solve(self):
        raise NotImplementedError


class BacktrackingSolver(Solver):
    def solve(self, puzzle: List[List[int]]):
        puzzle = copy.deepcopy(puzzle)
        if self._solve(puzzle):
            return puzzle
        else:
            return None

    def _solve(self, puzzle: List[List[int]]):
        empty_cell = self._find_empty_cell(puzzle)
        if empty_cell is None:
            return True

        row, col = empty_cell

        for num in range(1, 10):
            if self._is_valid(puzzle, row, col, num):
                puzzle[row][col] = num
                if self._solve(puzzle):
                    return True
                puzzle[row][col] = 0

        return False

    # def _find_empty_cell(self, puzzle: List[List[int]]):
    #     min_candidates = 10
    #     best_pos = None

    #     for i in range(9):
    #         for j in range(9):
    #             if puzzle[i][j] == 0:
    #                 candidates = 0
    #                 for num in range(1, 10):
    #                     if self._is_valid(puzzle, i, j, num):
    #                         candidates += 1
    #                 if candidates == 1:
    #                     return (i, j)
    #                 if candidates < min_candidates:
    #                     min_candidates = candidates
    #                     best_pos = (i, j)

    #     return best_pos

    def _find_empty_cell(self, puzzle: List[List[int]]):
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    return (i, j)
        return None

    def _is_valid(self, puzzle: List[List[int]], row: int, col: int, num: int):
        for i in range(9):
            if puzzle[row][i] == num:
                return False

        for i in range(9):
            if puzzle[i][col] == num:
                return False

        row_start = row // 3 * 3
        col_start = col // 3 * 3
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if puzzle[i][j] == num:
                    return False

        return True


def cross(A, B):
    "Cross product of strings in A and strings in B."
    return tuple(a + b for a in A for b in B)


Digit     = str  # e.g. '1'
digits    = '123456789'
DigitSet  = str  # e.g. '123'
rows      = 'ABCDEFGHI'
cols      = digits
Square    = str  # e.g. 'A9'
squares   = cross(rows, cols)
Grid      = Dict[Square, DigitSet] # E.g. {'A9': '123', ...}
all_boxes = [cross(rs, cs)  for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
all_units = [cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + all_boxes
units     = {s: tuple(u for u in all_units if s in u) for s in squares}
peers     = {s: set().union(*units[s]) - {s} for s in squares}
Picture   = str 


class ConstraintPropagationSolver(Solver):
    def solve(self, puzzle: List[List[int]]):
        puzzle = copy.deepcopy(puzzle)
        picture = ''.join(str(num) for row in puzzle for num in row).replace('0', '.')
        grid = self._parse(picture)
        solution = self._search(grid)
        if solution is not None and self._is_solution(solution, grid):
            return self._grid_to_array(solution)
        else:
            return None

    def _parse(self, picture: str) -> Grid:
        """Convert a Picture to a Grid."""
        vals = re.findall(r"[.1-9]|[{][1-9]+[}]", picture)
        assert len(vals) == 81
        return {s: digits if v == '.' else re.sub(r"[{}]", '', v) 
                for s, v in zip(squares, vals)}
    
    def _is_solution(self, solution: Optional[Grid], puzzle: Grid) -> bool:
        "Is this proposed solution to the puzzle actually valid?"
        return (solution is not None and
                all(solution[s] in puzzle[s] for s in squares) and
                all({solution[s] for s in unit} == set(digits) for unit in all_units))

    def _constrain(self, grid: Grid) -> Grid:
        "Propagate constraints on a copy of grid to yield a new constrained Grid."
        result: Grid = {s: digits for s in squares}
        for s in grid:
            if len(grid[s]) == 1:
                self._fill(result, s,  grid[s])
        return result

    def _fill(self, grid: Grid, s: Square, d: Digit) -> Optional[Grid]:
        """Eliminate all the digits except d from grid[s]."""
        if grid[s] == d or all(self._eliminate(grid, s, d2) for d2 in grid[s] if d2 != d):
            return grid
        else:
            return None

    def _eliminate(self, grid: Grid, s: Square, d: Digit) -> Optional[Grid]:
        """Eliminate d from grid[s]; implement the two constraint propagation strategies."""
        if d not in grid[s]:
            return grid        ## Already eliminated
        grid[s] = grid[s].replace(d, '')
        if not grid[s]:
            return None        ## None: no legal digit left
        elif len(grid[s]) == 1:
            # 1. If a square has only one possible digit, then eliminate that digit as a possibility for each of the square's peers.
            d2 = grid[s]
            if not all(self._eliminate(grid, s2, d2) for s2 in peers[s]):
                return None    ## None: can't eliminate d2 from some square
        for u in units[s]:
            dplaces = [s for s in u if d in grid[s]]
            # 2. If a unit has only one possible square that can hold a digit, then fill the square with the digit.
            if not dplaces or (len(dplaces) == 1 and not self._fill(grid, dplaces[0], d)):
                return None    ## None: no place in u for d
        return grid
    
    def _search(self, grid: Optional[Grid]) -> Optional[Grid]:
        "Depth-first search with constraint propagation to find a solution."
        if grid is None: 
            return None
        s = min((s for s in squares if len(grid[s]) > 1), 
                default=None, key=lambda s: len(grid[s]))
        if s is None: # No squares with multiple possibilities; the search has succeeded
            return grid
        for d in grid[s]:
            solution = self._search(self._fill(grid.copy(), s, d))
            if solution:
                return solution
        return None

    def _grid_to_array(self, grid: Grid) -> List[List[int]]:
        """Convert a grid dictionary to 2D array format."""
        result = []
        for row in rows:
            current_row = []
            for col in cols:
                current_row.append(int(grid[row + col]))
            result.append(current_row)
        return result


class DancingLinksSolver(Solver):
    def __init__(self):
        super().__init__()
        self.MAXSIZE = 100010
        self.n = 0  # number of rows
        self.m = 0  # number of columns
        self.tot = 0  # number of nodes
        self.first = [0] * (self.MAXSIZE + 10)  # the first node in each row
        self.siz = [0] * (self.MAXSIZE + 10)  # the number of nodes in each column
        self.L = [0] * (self.MAXSIZE + 10)  # left pointer
        self.R = [0] * (self.MAXSIZE + 10)  # right pointer
        self.U = [0] * (self.MAXSIZE + 10)  # up pointer
        self.D = [0] * (self.MAXSIZE + 10)  # down pointer
        self.col = [0] * (self.MAXSIZE + 10)  # the column of the node
        self.row = [0] * (self.MAXSIZE + 10)  # the row of the node

    def build(self, r: int, c: int):
        """initialize DLX"""
        self.n = r
        self.m = c
        for i in range(c + 1):
            self.L[i] = i - 1
            self.R[i] = i + 1
            self.U[i] = self.D[i] = i
        self.L[0] = c
        self.R[c] = 0
        self.tot = c
        self.first = [0] * (self.MAXSIZE + 10)
        self.siz = [0] * (self.MAXSIZE + 10)

    def insert(self, r: int, c: int):
        """insert a node"""
        self.tot += 1
        self.col[self.tot] = c
        self.row[self.tot] = r
        self.siz[c] += 1
        
        self.D[self.tot] = self.D[c]
        self.U[self.D[c]] = self.tot
        self.U[self.tot] = c
        self.D[c] = self.tot
        
        if not self.first[r]:
            self.first[r] = self.L[self.tot] = self.R[self.tot] = self.tot
        else:
            self.R[self.tot] = self.R[self.first[r]]
            self.L[self.R[self.first[r]]] = self.tot
            self.L[self.tot] = self.first[r]
            self.R[self.first[r]] = self.tot

    def remove(self, c: int):
        """remove the column c and its related rows"""
        self.L[self.R[c]] = self.L[c]
        self.R[self.L[c]] = self.R[c]
        i = self.D[c]
        while i != c:
            j = self.R[i]
            while j != i:
                self.U[self.D[j]] = self.U[j]
                self.D[self.U[j]] = self.D[j]
                self.siz[self.col[j]] -= 1
                j = self.R[j]
            i = self.D[i]

    def recover(self, c: int):
        """recover the column c and its related rows"""
        i = self.U[c]
        while i != c:
            j = self.L[i]
            while j != i:
                self.U[self.D[j]] = self.D[self.U[j]] = j
                self.siz[self.col[j]] += 1
                j = self.L[j]
            i = self.U[i]
        self.L[self.R[c]] = self.R[self.L[c]] = c

    def dance(self, dep: int, stk: List[int], ans: List[List[int]]) -> bool:
        """Dancing Links algorithm main process"""
        if not self.R[0]:
            for i in range(1, dep):
                x = (stk[i] - 1) // 9 // 9
                y = (stk[i] - 1) // 9 % 9
                v = (stk[i] - 1) % 9 + 1
                ans[x][y] = v
            return True

        c = self.R[0]
        i = self.R[0]
        while i != 0:
            if self.siz[i] < self.siz[c]:
                c = i
            i = self.R[i]

        self.remove(c)
        i = self.D[c]
        while i != c:
            stk[dep] = self.row[i]
            j = self.R[i]
            while j != i:
                self.remove(self.col[j])
                j = self.R[j]
            if self.dance(dep + 1, stk, ans):
                return True
            j = self.L[i]
            while j != i:
                self.recover(self.col[j])
                j = self.L[j]
            i = self.D[i]
        self.recover(c)
        return False

    def _get_id(self, row: int, col: int, num: int) -> int:
        """get the id of the node"""
        return (row - 1) * 9 * 9 + (col - 1) * 9 + num

    def _insert_constraints(self, row: int, col: int, num: int):
        """insert the constraints of the sudoku"""
        dx = (row - 1) // 3 + 1
        dy = (col - 1) // 3 + 1
        room = (dx - 1) * 3 + dy
        id = self._get_id(row, col, num)
        
        # four constraints
        f1 = (row - 1) * 9 + num  # row constraint
        f2 = 81 + (col - 1) * 9 + num  # column constraint
        f3 = 81 * 2 + (room - 1) * 9 + num  # box constraint
        f4 = 81 * 3 + (row - 1) * 9 + col  # cell constraint
        
        self.insert(id, f1)
        self.insert(id, f2)
        self.insert(id, f3)
        self.insert(id, f4)

    def solve(self, puzzle: List[List[int]]) -> Optional[List[List[int]]]:
        """solve the sudoku using Dancing Links algorithm"""
        # Initialize DLX
        self.build(729, 324)  # 729 possible positions, 324 constraints
        
        # Build the constraint matrix
        for i in range(1, 10):
            for j in range(1, 10):
                for v in range(1, 10):
                    if puzzle[i-1][j-1] and puzzle[i-1][j-1] != v:
                        continue
                    self._insert_constraints(i, j, v)
        
        # Solve
        stk = [0] * 1000  # stack
        ans = [[0] * 9 for _ in range(9)]  # answer array
        
        # Copy the original sudoku to the answer array
        for i in range(9):
            for j in range(9):
                ans[i][j] = puzzle[i][j]
        
        if self.dance(1, stk, ans):
            return ans
        return None


if __name__ == "__main__":
    solver = DancingLinksSolver()
    puzzle = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]
    import time
    start_time = time.time()
    solved = solver.solve(puzzle)
    end_time = time.time()
    print(f"time: {end_time - start_time} seconds")
    if solved:
        print(solved)
    else:
        print("No solution found")
