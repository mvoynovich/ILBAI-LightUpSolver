from z3 import *
import numpy as np
import time

"""
Modules we are using:
Z3: We are using Z3 as our automated reasoner. 
    It handles all the logic behind the constraints and boolean expressions we set up.

Numpy: We are using numpy to create our square test grids using arrays

Time: We are just using this module to print the output in a prettier fashion and giving 
      a sense of satisfaction to each step being completed.
"""

"""
General Rules/Info:
  Rules to the lightup/akari game can be found here: 
    https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/lightup.html#lightup

  All test grids setup before hand are available to be tested here (using the seed and game id links provided in the txt files):
    https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html 

  The grid is a 2D numpy array where:
      -1 = white cell (empty)
      -2 = black cell (no number)
      0-4 = black cell with number indicating adjacent lights

  The printed output of the grid has symbols representing the following:
      □ = white cell (empty)
      ■ = Black cell (no number)
      0-4 = black cell with number indicating adjacent lights
      ★ = Light 
      · = Light beam (representing the beams that come from the lights)
      
  In the Light array we have values representing the following:
    0 = no light at [i][j]
    1 = there is a light at [i][j]
"""

class LightUpSolver:
    """
    Class that performs all functions needed to solve the grid problem light up/akari/laser grids
    """
    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.lights = None

    def print_grid(self, lights=None, show_beams=False):
        """
        Prints the grid at different stages 
        (has different parameters to print it in different ways)

        lights: Parameter that stores the locations of lights in the solution grid

        show_beams: Optional parameter that allows for the display of beams of light
                    coming from the original lights
        """
        rows, cols = self.grid.shape
        
        # Set up display board
        display = []
        for i in range(rows):
            display.append([])
            for j in range(cols):
                display[i].append(" ")
        
        # Fill in basic symbols following the key from above
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
        
        # Add beams if requested (Show light coming out from the lights)
        # For each location if there is a light, light up all empty cells in the 4 cardinal directions before we hit a black cell
        if show_beams and lights is not None:
            for i in range(rows):
                for j in range(cols):
                    if lights[i][j] == 1:  # If this is a light
                        # Beam right
                        for k in range(j + 1, cols):
                            # If hit black cell stop replacing
                            if self.grid[i][k] >= -2 and self.grid[i][k] != -1:
                                break
                            # Replace empty cell with a light beam
                            if display[i][k] == '□':
                                display[i][k] = '·'
                        
                        # Beam left
                        for k in range(j - 1, -1, -1):
                            # If hit black cell stop replacing
                            if self.grid[i][k] >= -2 and self.grid[i][k] != -1:
                                break
                            # Replace empty cell with a light beam
                            if display[i][k] == '□':
                                display[i][k] = '·'
                        
                        # Beam down
                        for k in range(i + 1, rows):
                            # If hit black cell stop replacing
                            if self.grid[k][j] >= -2 and self.grid[k][j] != -1:
                                break
                            # Replace empty cell with a light beam
                            if display[k][j] == '□':
                                display[k][j] = '·'
                        
                        # Beam up
                        for k in range(i - 1, -1, -1):
                            # If hit black cell stop replacing
                            if self.grid[k][j] >= -2 and self.grid[k][j] != -1:
                                break
                            # Replace empty cell with a light beam
                            if display[k][j] == '□':
                                display[k][j] = '·'
        
        # Print the display grid
        for row in display:
            print(' '.join(row))
    
    def solve(self):
        """
        Solves a lightup puzzle using Z3 SMT solver (Automated Reasoning) with step-by-step visualization
        Messages are printed at each step for debugging purposes and to let the user know whats going on
        Performs the solving by creating a bunch of constraints using boolean statements 
        """
        print("Initial puzzle:")
        self.print_grid()
        print("\nSolving...\n")
        time.sleep(1)  # Pause to let user see the step
        
        # Initialize the z3 solver (Automated Reasoning)
        solver = Solver()
        
        # Create a symbolic boolean variable for each cell 
        # (evaluated later by solver and is not assigned a concrete value at the start)
        self.lights = []
        for i in range(self.rows):
            self.lights.append([])
            for j in range(self.cols):
                self.lights[i].append(Bool(f"light_{i}_{j}")) #light
        
        # Helper function to check for lights next to the numbered cells 
        def get_adjacent_cells(i, j):
            adjacent = []
            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.rows and 0 <= nj < self.cols and self.grid[ni][nj] == -1:
                    adjacent.append((ni, nj))
            return adjacent
        
        # Helper function to check if a cell is illuminated by a light at (li,lj)
        def is_illuminated_by(i, j, li, lj):
            # If we are at a light we are illuminated
            if i == li and j == lj:
                return True
            # Check the row for no barriers (black cell) inbetween cell and light
            if i == li:
                start, end = min(j, lj), max(j, lj)
                return all(self.grid[i][k] == -1 for k in range(start, end + 1))
            # Check the col for no barriers (black cell) inbetween cell and light
            if j == lj:
                start, end = min(i, li), max(i, li)
                return all(self.grid[k][j] == -1 for k in range(start, end + 1))
            return False
        
        # Add constraints
        print("Adding constraints:")
        
        print("\n1. Adding illumination constraints for white cells...")
        time.sleep(1)
        # All white cells must be illuminated
        for i in range(self.rows):
            for j in range(self.cols):
                # Check all grid locations for if they are an empty cell
                if self.grid[i][j] == -1:
                    illumination_conditions = []
                    # Add all possible locations that a light can be placed to light up that cell
                    for li in range(self.rows):
                        for lj in range(self.cols):
                            if self.grid[li][lj] == -1 and is_illuminated_by(i, j, li, lj):
                                illumination_conditions.append(self.lights[li][lj])
                    solver.add(Or(illumination_conditions))
        
        print("2. Adding constraints for numbered cells...")
        time.sleep(1)
        # All numbered cells must have exactly that many lights adjacent
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] >= 0:
                    # Adds a Pseudo-Boolean Equality to each numbered cell
                    # Requires that there must be exactly that many lights for this constraint to be true
                    # Requires that self.grid[i][j] is equal to the number of self.lights[ni][nj] that are 1/true
                    # self.grid[i][j] should be a positive number representing the numbered black cell and how many lights need to be adjacent
                    adjacent = get_adjacent_cells(i, j)
                    solver.add(PbEq([(self.lights[ni][nj], 1) for ni, nj in adjacent], self.grid[i][j]))
        
        print("3. Adding constraints for black cells...")
        time.sleep(1)
        # Requires that black cells cannot have a light placed on them
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == -2 or self.grid[i][j] >= 0:
                    # Light must be false (cannot be on the same location) at any location that has a black cell
                    solver.add(Not(self.lights[i][j]))
        
        print("4. Adding constraints to prevent lights from seeing each other...")
        time.sleep(1)
        # Make sure that any light is not touched by the light beams of another 
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == -1:
                    # For all empty locations that a light could be on
                    for li in range(self.rows):
                        for lj in range(self.cols):
                            # Check all locations in its row and all locations in its col
                            if (li != i or lj != j) and self.grid[li][lj] == -1 and is_illuminated_by(i, j, li, lj):
                                # And assert that if a light is placed at [i][j] there cannot be a a light at [li][lj] such that it lights up [i][j]
                                # Does this by adding more symbolic boolean expressions to the constraints in the solver
                                solver.add(Not(And(self.lights[i][j], self.lights[li][lj])))
        
        print("\nChecking for solution...")
        time.sleep(1)
        
        # Check if there is a valid solution that satisfies the constraints
        if solver.check() == sat:
            model = solver.model()
            # Create the solution array that will be used to print out our results
            solution = np.zeros((self.rows, self.cols), dtype=int)
            for i in range(self.rows):
                for j in range(self.cols):
                    if is_true(model[self.lights[i][j]]):
                        solution[i][j] = 1
            
            # Print the solution without light beams to show placement of all special objects/cells
            print("\nFound solution! First showing light placements:")
            self.print_grid(solution, show_beams=False)
            time.sleep(1)
            
            # Print the solution with light beams to show that placement of the lights light up all empty cells
            print("\nNow showing light beams:")
            self.print_grid(solution, show_beams=True)
            return solution
        
        # If we cannot meet all the constraints the problem does not have a solution
        print("\nNo solution exists!")
        return None