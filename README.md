# STILL ONGOING, CURRENTLY THE PROGRAM WILL FAIL TO EXECUTE PROPERLY 
I tried to use MVC model to improve the readability and reusability of the code.<br>

# Interactive Color Segmentation with Linear Programming
Implementation of the paper [Interactive color image segmentation with linear programming](https://link.springer.com/article/10.1007/s00138-008-0171-x) 

## prerequisite
### List of packages
- Gurobi: The Gurobi Optimizer is a commercial optimization solver for linear programming, quadratic programming, quadratically constrained programming, mixed integer linear programming, etc. <br>
How to install gurobi in Anaconda environment [here](https://www.gurobi.com/get-anaconda/)
- tkinter: GUI helper<br>
- cv2: image <br>
- numpy: essential for python users learning data science <br>
- scipy:  <br>
- sklearn: <br>
- skimage: <br>

## How to start
Currently, there is a single program called 'main.py'.<br>
Go to the folder and launch a commandline environment where python3 is installed and execute `python main.py`.<br>
If this fails, see if you have any package missing. (listed above) <br>

You can change the sample image to explore more. <br>

*fyi. program contains lots of spaghetti code that requires lots of refactoring*

## To finalize
This is program is based on a paper published in 2008. <br>
It is less likely that you will get the optimal solution from this program. <br>

I would love to know algorithms that have flexibility and low time-complexity as the algorithm mentioned in the paper.
