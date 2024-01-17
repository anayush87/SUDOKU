import tkinter as tk
from tkinter import messagebox
import random
N = 9               #size of suduko grid
root = tk.Tk()          # Create a Tkinter window
root.title("Sudoku")
CELL_SIZE = 80              # Constants for grid and window
WINDOW_SIZE = CELL_SIZE * (N+1)
# Initialize grid
grid = [[0 for _ in range(N)] for _ in range(N)]
# Create a list to hold the Entry widgets
entries = [[None for _ in range(N)] for _ in range(N)]
# Function to draw the Sudoku grid
def draw_grid():
    global entries
    for i in range(N):
        for j in range(N):
            cell_value = grid[i][j]
            if cell_value != 0:
                label = tk.Label(root, text=str(cell_value), width=1, font=('Arial', 40),)
                label.grid(row=i, column=j)
            else:
                entry = tk.Entry(root, width=3, font=('Arial', 40))
                entry.grid(row=i, column=j)
                entry.bind('<Key>', make_validate_input(i, j))
                entries[i][j] = entry

     # Highlight 3x3 subgrids
    for i in range(0, N, 3):  # Iterate over subgrid rows
        for j in range(0, N, 3):  # Iterate over subgrid columns
            for m in range(3):  # Highlight cells within each 3x3 subgrid
                for n in range(3):
                    cell = entries[i + m][j + n]
                    cell.config(highlightbackground="black")  # Set highlight color


# Function to check if a number is valid in a specific position
def isValid(grid, row, col, num):
    for x in range(N):
        if grid[x][col] == num and x != row:
            return False
    for y in range(N):
        if grid[row][y] == num and y != col:
            return False
    subgrid_row = (row // 3) * 3
    subgrid_col = (col // 3) * 3
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if grid[i][j] == num and (i != row or j != col):
                return False
    return True
# Function to solve the Sudoku puzzle
def solveSudoku(grid):
    for row in range(N):
        for col in range(N):                                #naviagte each qand every cell 
            if grid[row][col] == 0:
                for num in range(1, N + 1):                 #
                    if isValid(grid, row, col, num):        #check for valid
                        grid[row][col] = num
                        if solveSudoku(grid):               # reutrn ture if all gird is solved
                            return True
                        grid[row][col] = 0
                return False                                #false if a gird doesnt conatin a value
    return True
# Function to generate a random Sudoku puzzle
def generateSudoku():
    grid = [[0 for _ in range(N)] for _ in range(N)]
    # Fill a few cells to ensure a unique solution
    for i in range(N):
        for j in range(N):
            if random.random() > 0.7:
                num = random.randint(1, N)
                while not isValid(grid, i, j, num):
                    num = random.randint(1, N)
                grid[i][j] = num
    # Remove some numbers to create the puzzle
    removed_numbers = int(0.4 * N**2)
    for _ in range(removed_numbers):
        row = random.randint(0, N - 1)
        col = random.randint(0, N - 1)
        if grid[row][col] != 0:
            grid[row][col] = 0
    return grid
initial_grid = generateSudoku()

# Function to create a function that validates input and updates the grid for a specific cell
def make_validate_input(row, col):
    def validate_input(event):
        global grid
        value = event.char
        if value.isdigit() and 1 <= int(value) <= 9:
            num = int(value)
            prev_value = entries[row][col].get()  # Get previous value in the Entry box
            grid[row][col] = num
            if not isValid(grid, row, col, num):
                entries[row][col].delete(0, tk.END)  # Clear the entry box
                entries[row][col].insert(tk.END, num)  # Reinsert the previous value
                entries[row][col].config(background="red")
            else:
                entries[row][col].delete(0, tk.END)  # Clear the entry box
                entries[row][col].insert(tk.END, num)  # Update with the entered digit
                entries[row][col].config(background="white")
                entries[row][col].config(justify='center')
            return "break"  # Prevents the default behavior of inserting the character

    return validate_input
# Function to solve the Sudoku puzzle
def solve():
    global grid
    solveSudoku(grid)
    draw_grid()

    
def isGridFilled(grid):
    for row in grid:
        for cell in row:
            if cell == 0:
                return False
    return True

# Function to check if the current grid is solved
def isSolved(grid):
    # Check if the grid is completely filled and valid
    return isGridFilled(grid) and solveSudoku(grid)

# Function to compare two grids
def compareGrids(grid1, grid2):
    for i in range(N):
        for j in range(N):
            if grid1[i][j] != grid2[i][j]:
                return False
    return True

# Function to display the congratulations message when the puzzle is solved
def checkSolved():
    global grid, initial_grid, check_id
    if isGridFilled(grid) and compareGrids(grid, initial_grid):
        messagebox.showinfo("Congratulations!", "You've solved the Sudoku puzzle!")
        root.after_cancel(check_id)  # Stop further checking once the puzzle is solved
    else:
        check_id = root.after(1000, checkSolved)  # Check again after 1 second

def reset():
    global grid, initial_grid
    initial_grid=grid
    grid = [row[:] for row in initial_grid]  # Restore the grid to initial state
    draw_grid()

def new_game():
    global grid
    grid = generateSudoku()
    draw_grid()


pady_space = 19   # Adding space between buttons
def create_buttons():
    quit_button = tk.Button(root, text="QUIT", command=root.quit, bg='skyblue', fg='black',font='anton')
    reset_button = tk.Button(root, text="RESET", command=reset,bg='skyblue', fg='black',font='anton')
    solve_button = tk.Button(root, text="SOLVE", command=solve, bg='skyblue', fg='black',font='anton')
    new_game_button = tk.Button(root,font='anton', text="NEW", command=new_game, bg='skyblue', fg='black')

    quit_button.grid(row=N + 1, column=7, pady=pady_space)
    reset_button.grid(row=N + 1, column=3, pady=pady_space)
    solve_button.grid(row=N + 1, column=5, pady=pady_space)
    new_game_button.grid(row=N + 1, column=1, pady=pady_space)


def main():
    root.configure(bg='grey')
    global grid, initial_grid, check_id
    draw_grid()
    grid = generateSudoku()
    initial_grid = [row[:] for row in grid]  # Store the initial grid
    create_buttons()
    check_id = root.after(1000, checkSolved)  # Start the periodic check for solving
    root.mainloop()

if __name__ == "__main__":
    main()