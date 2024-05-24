# Pathfinding Simulation

## Overview

This project implements a pathfinding simulation using the A* algorithm. It visualizes the process of finding a path on a grid from a start node to a goal node, with obstacles placed in the grid. The visualization is done using Pygame, and the user can interact with the grid to add/remove obstacles and run the pathfinding algorithm.

## Files and Structure

- `Node.py`: Defines the `Node` class, representing each cell in the grid.
- `Map.py`: Defines the `Map` class, representing the grid of nodes and provides operations to manipulate it.
- `Path.py`: Defines the `Path` class, representing a path as a list of nodes.
- `PathFinder.py`: Defines the `PathFinder` class, implementing the A* algorithm.
- `Visualizer.py`: Defines the `Visualizer` class, using Pygame to visualize the grid and pathfinding process.
- `Simulation.py`: Defines the `Simulation` class, managing the overall simulation, including setting up the map and running the pathfinding and visualization.
- `main.py`: The main script that runs the simulation.

## Theory

### A* Algorithm

The A* algorithm is a popular pathfinding and graph traversal algorithm. It is widely used due to its performance and accuracy. A* efficiently finds the shortest path from a start node to a goal node using the following formula:

\[ f(n) = g(n) + h(n) \]

- \( f(n) \) is the total cost of the node.
- \( g(n) \) is the cost from the start node to the current node.
- \( h(n) \) is the heuristic estimate from the current node to the goal node.

### Heuristics

Two heuristics are used in this implementation:

- **Manhattan Distance**: Used when diagonal movements are not allowed.
  \[ h(n) = |x_1 - x_2| + |y_1 - y_2| \]
- **Chebyshev Distance**: Used when diagonal movements are allowed.
  \[ h(n) = \max(|x_1 - x_2|, |y_1 - y_2|) \]

### Classes and Their Roles

#### Node Class
- Represents each cell in the grid.
- Holds attributes like position, cost metrics (`g`, `h`, `f`), and state flags (e.g., `block`, `in_closed_set`).

#### Map Class
- Represents the grid of nodes.
- Provides methods to set the start and goal nodes, add obstacles, and access nodes.

#### Path Class
- Represents the path as a list of nodes.
- Provides methods to add nodes to the path and retrieve the path as coordinates.

#### PathFinder Class
- Implements the A* algorithm.
- Provides methods to calculate heuristics, get neighbors, and reconstruct the path.

#### Visualizer Class
- Uses Pygame to visualize the grid, path, and obstacles.
- Handles user interactions like adding/removing obstacles and running the pathfinding algorithm.

#### Simulation Class
- Manages the overall simulation.
- Sets up the map, runs the pathfinding algorithm, and visualizes the process.

## Installation and Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/pathfinding-simulation.git
   cd pathfinding-simulation
   ```

2. **Install the required libraries**:
   ```sh
   pip install pygame
   ```

3. **Run the simulation**:
   ```sh
   python main.py
   ```

## Usage

### Controls

- **Left Click**: Add/remove obstacles on the grid.
- **Pathfind Button**: Run the pathfinding algorithm.
- **Reset Button**: Reset the grid and clear the path.
- **Toggle Metric Button**: Toggle between Manhattan and Chebyshev distance.
- **Clear Path Button**: Clear the path while retaining obstacles.
- **Clear Obstacles Button**: Remove all obstacles from the grid.

### Visual Representation

- **Grid**: Represents the map with cells.
- **Green Cell**: Start node.
- **Red Cell**: Goal node.
- **Grey Cell**: Obstacle.
- **Blue Cells**: Path from the start to the goal.

## Example

Below is an example of how to set up and run the simulation:

```python
from Simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(width=50, height=50, pass_allow_diagonal=False)
    sim.setup(start=(0, 0), goal=(49, 49), obstacles=[(10, 1)])
    sim.run()
```

## Resources

- [GeeksforGeeks: Python `__lt__` magic method](https://www.geeksforgeeks.org/python-__lt__-magic-method/)
- [Medium: Easy A* Pathfinding](https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2)
- [Pygame Documentation](https://www.pygame.org/docs/ref/event.html)
- [Red Blob Games: A* Pathfinding Implementation](https://www.redblobgames.com/pathfinding/a-star/implementation.html)
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README provides a comprehensive guide to understanding, setting up, and running the pathfinding simulation. It includes an overview of the theory behind the A* algorithm, detailed explanations of the classes and their roles, and instructions for installation and usage.
