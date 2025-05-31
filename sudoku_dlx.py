class DLX:
    def __init__(self):
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

    def build(self, r, c):
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

    def insert(self, r, c):
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

    def remove(self, c):
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

    def recover(self, c):
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

    def dance(self, dep, stk, ans):
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


def get_id(row, col, num):
    """get the id of the node"""
    return (row - 1) * 9 * 9 + (col - 1) * 9 + num


def insert(solver, row, col, num):
    """insert the constraints of the sudoku"""
    dx = (row - 1) // 3 + 1
    dy = (col - 1) // 3 + 1
    room = (dx - 1) * 3 + dy
    id = get_id(row, col, num)
    
    # four constraints
    f1 = (row - 1) * 9 + num  # row constraint
    f2 = 81 + (col - 1) * 9 + num  # column constraint
    f3 = 81 * 2 + (room - 1) * 9 + num  # box constraint
    f4 = 81 * 3 + (row - 1) * 9 + col  # cell constraint
    
    solver.insert(id, f1)
    solver.insert(id, f2)
    solver.insert(id, f3)
    solver.insert(id, f4)


def solve_sudoku(grid):
    """solve the sudoku"""
    solver = DLX()
    solver.build(729, 324)  # 729 possible positions, 324 constraints
    
    # build the constraint matrix
    for i in range(1, 10):
        for j in range(1, 10):
            for v in range(1, 10):
                if grid[i-1][j-1] and grid[i-1][j-1] != v:
                    continue
                insert(solver, i, j, v)
    
    # solve
    stk = [0] * 1000  # stack
    ans = [[0] * 9 for _ in range(9)]  # answer array
    
    # copy the original sudoku to the answer array
    for i in range(9):
        for j in range(9):
            ans[i][j] = grid[i][j]
    
    if solver.dance(1, stk, ans):
        return ans
    return None


def print_sudoku(grid):
    """print the sudoku"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")


# example
if __name__ == "__main__":
    # example sudoku (0 means empty)
    grid = [
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
    
    print("original sudoku:")
    print_sudoku(grid)

    solution = solve_sudoku(grid)
    if solution:
        print("\nsolution:")
        print_sudoku(solution)
    else:
        print("\nno solution") 
