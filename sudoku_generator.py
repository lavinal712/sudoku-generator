import random
from sudoku_dlx import DLX, solve_sudoku, print_sudoku


def generate_solution():
    """generate a complete sudoku solution"""
    # create an empty sudoku grid
    grid = [[0] * 9 for _ in range(9)]
    
    # randomly fill the first row
    first_row = list(range(1, 10))
    random.shuffle(first_row)
    grid[0] = first_row
    
    # use the solver to complete the rest
    solution = solve_sudoku(grid)
    return solution

def is_unique_solution(grid):
    """check if the sudoku has a unique solution"""
    # try to solve
    solution = solve_sudoku(grid)
    if not solution:
        return False
    
    # find the first empty cell
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                # try to fill in different numbers
                for num in range(1, 10):
                    if num != solution[i][j]:
                        # save the original value
                        original = grid[i][j]
                        grid[i][j] = num
                        # check if there is another solution
                        if solve_sudoku(grid):
                            grid[i][j] = original
                            return False
                        grid[i][j] = original
                return True
    return True

def generate_sudoku(difficulty="medium"):
    """generate a random sudoku puzzle"""
    # generate a complete solution
    solution = generate_solution()
    if not solution:
        return None
    
    # create a puzzle copy
    puzzle = [row[:] for row in solution]
    
    # determine the number of cells to remove based on difficulty
    if difficulty == "easy":
        cells_to_remove = 30
    elif difficulty == "medium":
        cells_to_remove = 40
    elif difficulty == "hard":
        cells_to_remove = 50
    else:
        cells_to_remove = 45
    
    # get all positions
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    # remove cells symmetrically
    removed = 0
    for i, j in positions:
        if removed >= cells_to_remove:
            break
            
        # symmetric positions
        sym_i = 8 - i
        sym_j = 8 - j
        
        # remove the number
        puzzle[i][j] = 0
        puzzle[sym_i][sym_j] = 0
        removed += 2
        
        # check if there is still a unique solution
        if not is_unique_solution(puzzle):
            # if there is no unique solution, restore the number
            puzzle[i][j] = solution[i][j]
            puzzle[sym_i][sym_j] = solution[sym_i][sym_j]
            removed -= 2
    
    return puzzle, solution


def print_sudoku_with_solution(puzzle, solution):
    """print the sudoku puzzle and solution"""
    print("sudoku puzzle:")
    print_sudoku(puzzle)
    print("\nsolution:")
    print_sudoku(solution)


# example
if __name__ == "__main__":
    # generate a sudoku puzzle
    puzzle, solution = generate_sudoku(difficulty="easy")
    if puzzle and solution:
        print_sudoku_with_solution(puzzle, solution)
    else:
        print("generate sudoku failed")
