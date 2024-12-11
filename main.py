from LightUpSolver import *

def print_available_grids():
    """
    Prints all available grid files in the 'grids' folder and lets the user select one.
    """
    grids_folder = 'grids'  # Folder where grid files are stored
    
    # List all files in the 'grids' directory
    grid_files = [f for f in os.listdir(grids_folder) if os.path.isfile(os.path.join(grids_folder, f))]
    
    if not grid_files:
        print("No grid files found in the 'grids' folder.")
        return None
    
    print("Available grid files:")
    for idx, filename in enumerate(grid_files, start=1):
        print(f"{idx}. {filename}")
    
    # Let the user select a file
    selected_index = int(input("\nSelect a grid file by number: ")) - 1
    
    if selected_index < 0 or selected_index >= len(grid_files):
        print("Invalid selection. Exiting...")
        return None
    
    selected_file = grid_files[selected_index]
    print(f"Selected file: {selected_file}")
    
    return selected_file


def load_grid_from_file(filename):
    """
    Loads a grid from a file. The file is expected to have the format:
    seed
    game_id
    grid values (each row separated by a newline)
    """
    grid = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Store the lines that contain the grid
        solver_link = lines[0][6:]
        lines = lines[3:-1]
       
        for line in lines:
            # Convert each line to a list of integers
            row = list(map(int, line.strip().split(',')))
            grid.append(row)
    
    # Convert grid to a numpy array
    return np.array(grid), solver_link

def main():
    selected_file = print_available_grids()
    
    if selected_file is None:
        return "Error: Make sure you input a valid filename"
    
    grid_file_path = os.path.join('grids', selected_file)
    grid, solver_link = load_grid_from_file(grid_file_path)
    
    print(f"\nGrid loaded from {selected_file}:")
    print(grid)


    print("\nStarting Light Up puzzle solver...")
    time.sleep(1)

    solver = LightUpSolver(grid)
    solver.solve()

    print("\nVisit the following link to review solution with Tatham's solver:")
    print(solver_link)


if __name__ == "__main__":
    main()