[![forthebadge made-with-python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
<br>

# Maze-Generator-with-Randomized-DFS
A Pygame application which generates mazes using randomized DFS (Depth-First-Search)-(Iterative implementation).

Randomized-DFS: This algorithm, also known as the "recursive backtracker" algorithm, is a randomized version of the depth-first search algorithm. Frequently implemented with a stack, this approach is one of the simplest ways to generate a maze.

## Features:
* After the maze has been created, the user can play it and try to solve it if they want using the arrow keys.
* User can switch to easy mode or hard mode using the letters 'e' or 'h'. Easy mode will leave them with 25x25 maze while hardmode contains 50x50 maze.
* User can also let the program solve the maze with either DFS or BFS.

## How to Use:
<pre>
 To create the maze   - Press space bar <br>
 To play              - Use arrow keys ( ↑, ↓, →, ← ) <br>
 Switch to hard mode  - Press 'h' key <br>
 Switch back to easy
 Mode                 - Press 'e' key <br>
 To solve it with DFS - press the left control key <br>
 To solve it with BFS - press the right control key <br>
 To clear the visualisation part - press the 'c' key.
</pre>
* (note: If you want to see the process of creating the maze in a slower speed then feel free to change the speed - "time.sleep(0.05)" in line 228 ('dfs_maze_build' function).
* Choose the mode first (easy or hard) before pressing the space bar.(default is easy mode)

## Demo:
* 50x50 grid maze creation: <br>

![](images/maze_creation.png)

* User solving the 25x25 maze

![](images/user_solve_img.png)

* Solving the maze using DFS<br>

![](images/dfs_solve.png)

* Solving the maze using BFS<br>

![](images/bf_solve.png)
