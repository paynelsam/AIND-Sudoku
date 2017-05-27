# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: The Naked Twins strategy recognizes that if two boxes each have an identical
set of two possible values (A and B), then those boxes can be considered "twins."
One of these twins must hold either the value A or B, and the other twin will hold
the other value. For example, if Twin1 holds A, Twin2 must hold B.
Therefore, other boxes in the unit that contains both twins cannot take on the value
of either A or B. Therefore, we can update the constraints on other boxes in the
unit holding the pair of twins to narrow the list of possible values.

This could also be applied to Tripplets (though it is not as common) and could be
generalized to N boxes in the same unit if they share identical possible value
sets of length N.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: The diagnal Sudoku problem is solvable by the same method as the original Sudoku
problem, but with two additional units added when considering constraints on the
value of boxes.
In the original Sudoku problem, once a value has been found for Box_1 (either
a given known value, or found through "Only Choice") then other boxes in the same
unit can be updated to eliminate the value of Box_1 from their possible values.
This can be done because no two boxes in the same unit share a value.
In the updated Diagnal Sudoku problem, diagnal units can be used to apply this
constraint as well.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

