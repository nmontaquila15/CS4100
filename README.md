# CS4100

This repository is used to store the programming assignments for CS4100 - Artificial Intelligence

## Programming Assignment 1 - Search Agents
### 1. To see breadth first search, use the any of the following terminal commands:
python pacman.py -l tinyMaze -p SearchAgent  
python pacman.py -l mediumMaze -p SearchAgent  
python pacman.py -l bigMaze -z .5 -p SearchAgent  

### 2. To see depth-first search, use any of the following commands:
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs  
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5  

### 3. To see uniform cost search, use the following command:
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs  

### 4. To see A* search use the following command:
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic  

### 5. To see pacman find the four corners of the maze using breadth-first search, use the following commands:
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem  
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem  

### 6. To see pacman find the four corners of the maze using A* search, use the following commands:
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5  

### 7. To see pacman eat all the food in the maze using A* search, use any of the following commands:
python pacman.py -l testSearch -p AStarFoodSearchAgent  
python pacman.py -l trickySearch -p AStarFoodSearchAgent  

Note: these may take a minute or two to run.  

### 8. To see pacman eat all the food in the maze using greedy search, use the following command:
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5  
