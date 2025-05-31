# Sudoku Generator and Solver

A Python implementation of a Sudoku puzzle generator and solver using the Dancing Links algorithm (Algorithm X).

## Features

- **Sudoku Solver**
  - Implements the Dancing Links algorithm (Algorithm X)
  - Efficiently solves any valid Sudoku puzzle
  - Guarantees finding a solution if one exists

- **Sudoku Generator**
  - Generates random Sudoku puzzles with unique solutions
  - Supports multiple difficulty levels (easy, medium, hard)
  - Maintains puzzle symmetry for better aesthetics
  - Ensures puzzles have unique solutions

## Requirements

- Python 3.7 or higher
- No external dependencies required

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sudoku-generator.git
cd sudoku-generator
```

2. No additional installation steps required as the project uses only Python standard library.

## Usage

### Solving a Sudoku Puzzle

```python
from sudoku_dlx import solve_sudoku, print_sudoku

# Example puzzle (0 represents empty cells)
puzzle = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

# Solve the puzzle
solution = solve_sudoku(puzzle)
if solution:
    print_sudoku(solution)
else:
    print("No solution exists")
```

### Generating a Sudoku Puzzle

```python
from sudoku_generator import generate_sudoku, print_sudoku_with_solution

# Generate a puzzle with specified difficulty
# Available difficulties: 'easy', 'medium', 'hard'
puzzle, solution = generate_sudoku(difficulty='medium')

if puzzle and solution:
    print_sudoku_with_solution(puzzle, solution)
else:
    print("Failed to generate puzzle")
```

## Difficulty Levels

- **Easy**: 30 cells removed
- **Medium**: 40 cells removed
- **Hard**: 50 cells removed

## How It Works

### Dancing Links Algorithm
The solver uses Donald Knuth's Dancing Links algorithm (Algorithm X) to efficiently solve the exact cover problem that Sudoku represents. This implementation:
- Represents the Sudoku constraints as a sparse matrix
- Uses a doubly-linked list structure for efficient operations
- Implements backtracking with constraint propagation

### Puzzle Generation
The generator:
1. Creates a complete solution by randomly filling the first row and solving the rest
2. Removes numbers symmetrically while maintaining puzzle validity
3. Verifies the uniqueness of the solution
4. Adjusts the number of removed cells based on the desired difficulty

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Donald Knuth for the Dancing Links algorithm
- The Sudoku community for puzzle generation techniques 
- [DLX C++ Implement](https://oi-wiki.org/search/dlx/)
