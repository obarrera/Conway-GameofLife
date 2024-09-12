import pygame
import numpy as np
import random
import time

# Initialize Pygame
pygame.init()

# Set colors
BLACK = (0, 0, 0)        # Dead cells
BLUE = (0, 0, 255)       # Male cells (starting color)
PINK = (255, 105, 180)   # Female cells
BROWN = (139, 69, 19)    # Continent/land cells (obstacle)
GRID_COLOR = (50, 50, 50)  # Grid lines

# Set the dimensions of each cell and the grid size
CELL_SIZE = 10  # Size of each cell
GRID_HEIGHT = 100  # Number of cells in height
GRID_WIDTH = 100  # Number of cells in width
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life with Continents")

# Initialize the game board (0 = dead, 1 = male, 2 = female, 3 = continent)
def initialize_board(width, height):
    board = np.random.choice([0, 1, 2, 3], size=(height, width), p=[0.6, 0.15, 0.15, 0.1])  # 60% dead, 15% male, 15% female, 10% continent
    lifespans = np.zeros((height, width), dtype=int)  # Lifespans tracking for each cell
    fight_counters = np.zeros((height, width), dtype=int)  # Tracks how long males have been next to each other near a female
    return board, lifespans, fight_counters

# Count male, female, and empty neighbors (ignore continent cells)
def count_neighbors(board, x, y):
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0),  (1, 1)
    ]
    male_neighbors = 0
    female_neighbors = 0
    empty_neighbors = []
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < board.shape[0] and 0 <= ny < board.shape[1]:
            if board[nx][ny] == 1:
                male_neighbors += 1
            elif board[nx][ny] == 2:
                female_neighbors += 1
            elif board[nx][ny] == 0:
                empty_neighbors.append((nx, ny))
    return male_neighbors, female_neighbors, empty_neighbors

# Migrate a male cell towards a female or away from other males, avoiding continents
def migrate_male(board, x, y):
    male_neighbors, female_neighbors, empty_neighbors = count_neighbors(board, x, y)

    # Try to migrate towards an empty spot near a female, avoiding continent cells (3)
    if female_neighbors > 0 and empty_neighbors:
        random.shuffle(empty_neighbors)
        for nx, ny in empty_neighbors:
            _, females_in_spot, _ = count_neighbors(board, nx, ny)
            if females_in_spot > 0 and board[nx][ny] != 3:  # Avoid continents
                board[nx][ny] = board[x][y]
                board[x][y] = 0
                return

    # If there are no females, migrate away from other males, avoiding continents
    if male_neighbors > 0 and empty_neighbors:
        random.shuffle(empty_neighbors)
        for nx, ny in empty_neighbors:
            males_in_spot, _, _ = count_neighbors(board, nx, ny)
            if males_in_spot == 0 and board[nx][ny] != 3:  # Avoid continents
                board[nx][ny] = board[x][y]
                board[x][y] = 0
                return

    # If migration is not possible, stay in place
    return

# Manage fighting behavior between males near a female
def handle_fight(board, fight_counters, x, y, current_generation):
    male_neighbors, female_neighbors, _ = count_neighbors(board, x, y)

    # If two males are next to each other and there's a nearby female, start counting fight time
    if male_neighbors >= 1 and female_neighbors >= 1:
        fight_counters[x][y] += 1
        if fight_counters[x][y] >= 10:  # After 10 generations, a fight occurs
            # One of the males dies
            board[x][y] = 0
            fight_counters[x][y] = 0
    else:
        fight_counters[x][y] = 0  # Reset fight counter if conditions no longer met

# Calculate male color based on how close they are to fighting
def get_male_color(fight_counter):
    max_fight_threshold = 10
    if fight_counter == 0:
        return BLUE
    else:
        # Gradually blend from blue to red based on the fight_counter
        r = int((fight_counter / max_fight_threshold) * 255)
        g = 0
        b = int(255 - (fight_counter / max_fight_threshold) * 255)
        return (r, g, b)

# Apply rules, update the board, and manage lifespan
def update_board(board, lifespans, fight_counters, current_generation):
    new_board = board.copy()
    new_lifespans = lifespans.copy()
    new_fight_counters = fight_counters.copy()

    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 3:  # Continent cells don't interact
                continue

            male_neighbors, female_neighbors, _ = count_neighbors(board, i, j)

            # If the cell is alive (male or female)
            if board[i][j] == 1:  # Male cell
                # Handle fighting behavior
                handle_fight(board, new_fight_counters, i, j, current_generation)

                # Migrate males until reproduction or fighting
                if male_neighbors >= 2 and female_neighbors >= 1:
                    continue  # Males are near a female and another male; reproduction may occur
                else:
                    migrate_male(new_board, i, j)

                # Check if the cell has exceeded its lifespan
                if current_generation - lifespans[i][j] >= lifespans[i][j]:
                    new_board[i][j] = 0  # Cell dies
                    new_lifespans[i][j] = 0

            elif board[i][j] == 2:  # Female cell
                # Females remain stationary but now have a lifespan
                if current_generation - lifespans[i][j] >= lifespans[i][j]:
                    new_board[i][j] = 0  # Female dies after lifespan
                    new_lifespans[i][j] = 0

            # If the cell is dead
            elif board[i][j] == 0:
                # Reproduction rule: Allow reproduction with 1-4 neighbors (more flexible)
                if 1 <= male_neighbors + female_neighbors <= 4 and male_neighbors > 0 and female_neighbors > 0:
                    new_board[i][j] = random.choice([1, 2])  # New cell is male or female
                    new_lifespans[i][j] = random.randint(25, 35)  # Assign random lifespan between 25 and 35 generations

    return new_board, new_lifespans, new_fight_counters

# Draw the grid and cells with different colors for male, female, and continent cells
def draw_board(board, fight_counters):
    screen.fill(BLACK)  # Fill screen with black for dead cells
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row][col] == 1:  # Male cells
                male_color = get_male_color(fight_counters[row][col])
                pygame.draw.rect(screen, male_color, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])
            elif board[row][col] == 2:  # Female cells
                pygame.draw.rect(screen, PINK, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])
            elif board[row][col] == 3:  # Continent cells
                pygame.draw.rect(screen, BROWN, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])
    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
    pygame.display.flip()

# Display parameters and generation information
def display_information(generation, board):
    male_count = np.sum(board == 1)
    female_count = np.sum(board == 2)
    total_live = male_count + female_count
    print(f"Generation {generation} - Total Live Cells: {total_live} (Males: {male_count}, Females: {female_count})")

# Check if all cells are dead (to stop the game early)
def all_cells_dead(board):
    return np.sum(board) == 0

# Run the game with restart option
def run_game(width, height, generations=None):
    while True:
        board, lifespans, fight_counters = initialize_board(width, height)
        running = True
        generation_count = 0

        # Display initial parameters
        print(f"Starting Game of Life")
        print(f"Grid Size: {GRID_WIDTH} x {GRID_HEIGHT}, Cell Size: {CELL_SIZE}x{CELL_SIZE}")

        while running:
            # Check for exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update board and display it
            board, lifespans, fight_counters = update_board(board, lifespans, fight_counters, generation_count)
            draw_board(board, fight_counters)
            generation_count += 1

            # Display generation info every 10 generations
            if generation_count % 10 == 0:
                display_information(generation_count, board)

            # Stop the game early if all cells are dead
            if all_cells_dead(board):
                print("All cells are dead. Game over.")
                running = False

            # If the number of generations is limited
            if generations and generation_count >= generations:
                running = False

            time.sleep(0.1)  # Add delay for visualization

        print(f"Game ended after {generation_count} generations.")

        # Ask the user if they want to restart or quit
        choice = input("Do you want to restart the game? (y/n): ").lower()
        if choice != 'y':
            break

    pygame.quit()

# Set parameters and start the game
run_game(GRID_WIDTH, GRID_HEIGHT, generations=1000)  # Run for 1000 generations
