from z3 import *
import numpy as np
import time

"""
Modules we are using:
Z3: We are using Z3 as our automated reasoner. 
    It handles all the logic behind the constraints and boolean expressions we set up
    
Numpy: We are using numpy to     
"""



def print_grid(grid, lights=None, show_beams=False):
    """
    Prints the grid at different stages
    lights: Optional solution grid showing light positions
    show_beams: Whether to show the beam paths
    """
    rows, cols = grid.shape
    
    # Set up display board
    display = []
    for i in range(rows):
        display.append([])
        for j in range(cols):
            display[i].append(" ")
    
    # Fill in basic symbols
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] >= 0:  # Numbered black cell
                display[i][j] = str(grid[i][j])
            elif grid[i][j] == -2:  # Black cell
                display[i][j] = '■'
            elif lights is not None and lights[i][j] == 1:  # Light
                display[i][j] = '★'
            else:  # Empty cell
                display[i][j] = '□'
    
    # Add beams if requested
    if show_beams and lights is not None:
        for i in range(rows):
            for j in range(cols):
                if lights[i][j] == 1:  # If this is a light
                    # Beam right
                    for k in range(j + 1, cols):
                        if grid[i][k] >= -2 and grid[i][k] != -1:
                            break
                        if display[i][k] == '□':
                            display[i][k] = '·'
                    
                    # Beam left
                    for k in range(j - 1, -1, -1):
                        if grid[i][k] >= -2 and grid[i][k] != -1:
                            break
                        if display[i][k] == '□':
                            display[i][k] = '·'
                    
                    # Beam down
                    for k in range(i + 1, rows):
                        if grid[k][j] >= -2 and grid[k][j] != -1:
                            break
                        if display[k][j] == '□':
                            display[k][j] = '·'
                    
                    # Beam up
                    for k in range(i - 1, -1, -1):
                        if grid[k][j] >= -2 and grid[k][j] != -1:
                            break
                        if display[k][j] == '□':
                            display[k][j] = '·'
    
    # Print the display grid
    for row in display:
        print(' '.join(row))

def solve_lightup(grid):
    """
    Solves an lightup puzzle using Z3 SMT solver with step-by-step visualization
    """
    rows, cols = grid.shape
    
    print("Initial puzzle:")
    print_grid(grid)
    print("\nSolving...\n")
    time.sleep(1)  # Pause to let user see the step
    
    # Initialize the z3 solver (Automated Reasoning)
    solver = Solver()
    
    # Create boolean variables for each cell
    lights = []
    for i in range(rows):
        lights.append([])
        for j in range(cols):
            lights[i].append(Bool(f"light_{i}_{j}")) #light
    
    # Helper function to get valid adjacent cells
    def get_adjacent_cells(i, j):
        adjacent = []
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                adjacent.append((ni, nj))
        return adjacent
    
    # Helper function to check if a cell is illuminated by a light at (li,lj)
    def is_illuminated_by(i, j, li, lj):
        if i == li and j == lj:
            return True
        if i == li:
            start, end = min(j, lj), max(j, lj)
            return all(grid[i][k] == -1 for k in range(start, end + 1))
        if j == lj:
            start, end = min(i, li), max(i, li)
            return all(grid[k][j] == -1 for k in range(start, end + 1))
        return False
    
    # Add constraints
    print("Adding constraints:")
    
    print("\n1. Adding illumination constraints for white cells...")
    time.sleep(1)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -1:
                illumination_conditions = []
                for li in range(rows):
                    for lj in range(cols):
                        if grid[li][lj] == -1 and is_illuminated_by(i, j, li, lj):
                            illumination_conditions.append(lights[li][lj])
                solver.add(Or(illumination_conditions))
    
    print("2. Adding constraints for numbered cells...")
    time.sleep(1)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] >= 0:
                adjacent = get_adjacent_cells(i, j)
                solver.add(PbEq([(lights[ni][nj], 1) for ni, nj in adjacent], grid[i][j]))
    
    print("3. Adding constraints for black cells...")
    time.sleep(1)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -2:
                solver.add(Not(lights[i][j]))
    
    print("4. Adding constraints to prevent lights from seeing each other...")
    time.sleep(1)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -1:
                for li in range(rows):
                    for lj in range(cols):
                        if (li != i or lj != j) and grid[li][lj] == -1 and is_illuminated_by(i, j, li, lj):
                            solver.add(Not(And(lights[i][j], lights[li][lj])))
    
    print("\nChecking for solution...")
    time.sleep(1)
    
    if solver.check() == sat:
        model = solver.model()
        solution = np.zeros((rows, cols), dtype=int)
        for i in range(rows):
            for j in range(cols):
                if is_true(model[lights[i][j]]):
                    solution[i][j] = 1
        
        print("\nFound solution! First showing light placements:")
        print_grid(grid, solution, show_beams=False)
        time.sleep(1)
        
        print("\nNow showing light beams:")
        print_grid(grid, solution, show_beams=True)
        return solution
    
    print("\nNo solution exists!")
    return None

# Test with a simple puzzle
test_grid = np.array([
    [-1, -1, -1, -1, -1, 3, -1, -1, -1, -1],
    [-1, -1, -1, -1, 2, -1, 2, -1, -2, 1],
    [-1, -1, -1, -1, -2, -1, -1, -1, -1, -1],
    [0, -1, -1, 3, -1, -2, -1, -1, -1, 2],
    [-2, -1, -1, -1, -1, -1, -1, -2, -1, -1],
    [-1, -1, 0, -1, -1, -1, -1, -1, -1, -2],
    [1, -1, -1, -1, 1, -1, 3, -1, -1, 1],
    [-1, -1, -1, -1, -1, 1, -1, -1, -1, -1],
    [-2, 0, -1, 1, -1, 2, -1, -1, -1, -1],
    [-1, -1, -1, -1, 2, -1, -1, -1, -1, -1]
])

print("Starting Light Up puzzle solver...")
time.sleep(1)
solution = solve_lightup(test_grid)