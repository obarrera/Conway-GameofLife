# Conway's Game of Life with Continents

<img width="994" alt="Screenshot 2024-09-12 at 4 51 22 PM" src="https://github.com/user-attachments/assets/9bd930f4-e9fa-4f02-9c01-79a9601e01a8">
*Screenshot of the simulation showing cells interacting with geographical constraints.*


## Description
This is an advanced version of Conway's Game of Life, incorporating male and female cell dynamics, as well as random geographical "continents" that act as migration barriers. The simulation creates a rich environment where cells interact and evolve over time, influenced by reproduction, lifespans, fighting behavior, and geographical constraints.

## Features
- **Male and Female Cells**: Cells are randomly assigned male or female at birth and must interact with both genders to reproduce.
- **Dynamic Coloring**: Males change color gradually from blue to red as they approach fighting scenarios.
- **Fighting Mechanism**: Males that are close to each other and near a female will engage in fights after a certain period, reducing the population.
- **Continents**: Randomly generated "continents" on the grid act as obstacles, limiting migration and creating isolated regions where cells evolve differently.
- **Customizable Lifespan and Behavior**: Cells have random lifespans and follow specific rules for migration and reproduction based on their surroundings.

## Installation
 Clone the repository:
   
   ```bash
   git clone https://github.com/yourusername/conways-game-of-life-continents.git
   ```

## Install the required dependencies:

  bash
  ```
  pip3 install requirements.txt
  ```
## Usage
To run the simulation, execute the game_of_life.py file:

  bash
  ```
  python3 game_of_life.py
  ```
Running the Simulation
Once started, the simulation will continue running for 1000 generations by default, unless all cells die off beforehand.

## Controls
Exit the Simulation: Press the close button on the window or `Ctrl+C` in the terminal to stop the simulation.

## Simulation Behavior
- Reproduction: Male and female cells can reproduce if they are adjacent to each other and the conditions are right (1-4 neighbors).
- Migration: Male cells migrate in search of females or to avoid fighting. However, they cannot migrate through continents.
- Fighting: If two male cells are near a female for too long, they will engage in a fight, turning red before one male dies.
- Continents: Random continents create obstacles that influence migration patterns, creating "islands" of isolated cell populations.

## Future Improvements
- Add GUI controls to adjust simulation speed and parameters such as population density, lifespan, and grid size.
- Implement more complex geographic features such as lakes or mountain ranges.
- Enable saving and loading of simulation states to continue observing population evolution.
- Allow for customizable rulesets (e.g., different reproduction rates, migration preferences, or fight thresholds).

