from z3 import *
import numpy as np
import time

"""
Modules we are using:
Z3: We are using Z3 as our automated reasoner. 
    It handles all the logic behind the constraints and boolean expressions we set up
    
Numpy: We are using numpy to     
"""

class LightUpSolver:
    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.lights = None

    def print_grid(self, lights=None, show_beams=False):
        """
        Prints the grid at different stages
        lights: Optional solution grid showing light positions
        show_beams: Whether to show the beam paths
        """
        rows, cols = self.grid.shape
        
        # Set up display board
        display = []
        for i in range(rows):
            display.append([])
            for j in range(cols):
                display[i].append(" ")
        
        # Fill in basic symbols
        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] >= 0:  # Numbered black cell
                    display[i][j] = str(self.grid[i][j])
                elif self.grid[i][j] == -2:  # Black cell
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
                            if self.grid[i][k] >= -2 and self.grid[i][k] != -1:
                                break
                            if display[i][k] == '□':
                                display[i][k] = '·'
                        
                        # Beam left
                        for k in range(j - 1, -1, -1):
                            if self.grid[i][k] >= -2 and self.grid[i][k] != -1:
                                break
                            if display[i][k] == '□':
                                display[i][k] = '·'
                        
                        # Beam down
                        for k in range(i + 1, rows):
                            if self.grid[k][j] >= -2 and self.grid[k][j] != -1:
                                break
                            if display[k][j] == '□':
                                display[k][j] = '·'
                        
                        # Beam up
                        for k in range(i - 1, -1, -1):
                            if self.grid[k][j] >= -2 and self.grid[k][j] != -1:
                                break
                            if display[k][j] == '□':
                                display[k][j] = '·'
        
        # Print the display grid
        for row in display:
            print(' '.join(row))
    
    def solve(self):
        """
        Solves a lightup puzzle using Z3 SMT solver with step-by-step visualization
        """
        print("Initial puzzle:")
        self.print_grid()
        print("\nSolving...\n")
        time.sleep(1)  # Pause to let user see the step
        
        # Initialize the z3 solver (Automated Reasoning)
        solver = Solver()
        
        # Create boolean variables for each cell
        self.lights = []
        for i in range(self.rows):
            self.lights.append([])
            for j in range(self.cols):
                self.lights[i].append(Bool(f"light_{i}_{j}")) #light
        
        # Helper function to get valid adjacent cells
        def get_adjacent_cells(i, j):
            adjacent = []
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.rows and 0 <= nj < self.cols:
                    adjacent.append((ni, nj))
            return adjacent
        
        # Helper function to check if a cell is illuminated by a light at (li,lj)
        def is_illuminated_by(i, j, li, lj):
            if i == li and j == lj:
                return True
            if i == li:
                start, end = min(j, lj), max(j, lj)
                return all(self.grid[i][k] == -1 for k in range(start, end + 1))
            if j == lj:
                start, end = min(i, li), max(i, li)
                return all(self.grid[k][j] == -1 for k in range(start, end + 1))
            return False
        
        # Add constraints
        print("Adding constraints:")
        
        print("\n1. Adding illumination constraints for white cells...")
        time.sleep(1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == -1:
                    illumination_conditions = []
                    for li in range(self.rows):
                        for lj in range(self.cols):
                            if self.grid[li][lj] == -1 and is_illuminated_by(i, j, li, lj):
                                illumination_conditions.append(self.lights[li][lj])
                    solver.add(Or(illumination_conditions))
        
        print("2. Adding constraints for numbered cells...")
        time.sleep(1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] >= 0:
                    adjacent = get_adjacent_cells(i, j)
                    solver.add(PbEq([(self.lights[ni][nj], 1) for ni, nj in adjacent], self.grid[i][j]))
        
        print("3. Adding constraints for black cells...")
        time.sleep(1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == -2:
                    solver.add(Not(self.lights[i][j]))
        
        print("4. Adding constraints to prevent lights from seeing each other...")
        time.sleep(1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == -1:
                    for li in range(self.rows):
                        for lj in range(self.cols):
                            if (li != i or lj != j) and self.grid[li][lj] == -1 and is_illuminated_by(i, j, li, lj):
                                solver.add(Not(And(self.lights[i][j], self.lights[li][lj])))
        
        print("\nChecking for solution...")
        time.sleep(1)
        
        if solver.check() == sat:
            model = solver.model()
            solution = np.zeros((self.rows, self.cols), dtype=int)
            for i in range(self.rows):
                for j in range(self.cols):
                    if is_true(model[self.lights[i][j]]):
                        solution[i][j] = 1
            
            print("\nFound solution! First showing light placements:")
            self.print_grid(solution, show_beams=False)
            time.sleep(1)
            
            print("\nNow showing light beams:")
            self.print_grid(solution, show_beams=True)
            return solution
        
        print("\nNo solution exists!")
        return None

def main():
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

    solver = LightUpSolver(test_grid)
    solver.solve()

if __name__ == "__main__":
    main()