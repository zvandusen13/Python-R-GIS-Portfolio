This Python project generates and solves mazes of varying sizes using multiple search algorithms. It demonstrates object-oriented programming, algorithm implementation, and visualization of search paths.

Highlights
- Generates mazes with randomly blocked cells and configurable start and goal locations.
- Implements depth-first search (DFS), breadth-first search (BFS), and A* search algorithms to solve mazes.
- Tracks path length, number of cells searched, and marks the solution path.
- Uses classes to encapsulate maze, cell, and position data, as well as stacks, queues, and priority queues for search management.

How It Was Made
- Maze Generation: The Maze class creates a 2D grid of Cell objects with an adjustable proportion of blocked cells. Start and goal positions are randomly assigned, and debug mazes can be loaded for testing.
- Data Structures: Custom Stack, Queue, and PriorityQueue classes manage the cells explored by each algorithm. Each Cell tracks its position, contents, and parent to reconstruct paths.
- Algorithm Implementation: DFS uses a stack to explore as far as possible along each branch. BFS uses a queue to explore breadth-wise, ensuring the shortest path in terms of steps. A* search uses a priority queue to efficiently reach the goal.
- Path Visualization: Once a solution is found, the path is marked on the maze from the start to the finish line.
- Object-Oriented Design: The Cell, Position, and Maze classes encapsulate the maze’s state and behaviors. It keeps the code organized and allows easy reutilization for future projects.
  
Usage
- Ensure all custom classes (Stack, Queue, PriorityQueue) are in the same directory as the script.
- Run the script to generate mazes, solve them using the desired algorithm, and visualize the solution paths.
- Modify maze dimensions, blocked-cell proportion, or random seed to test different scenarios. Comment and uncomment testing blocks of cells
