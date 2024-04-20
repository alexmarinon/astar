from classes import sim

"""
Resources used:
https://www.geeksforgeeks.org/python-__lt__-magic-method/
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
https://www.pygame.org/docs/ref/event.html
https://www.redblobgames.com/pathfinding/a-star/implementation.html
https://peps.python.org/pep-0008/
"""


if __name__ == "__main__": # standard, doesnt run if used as part of a module or package
    # Removed tkinter popup because had compatiblity issues
    #show_popup("Important Info on How to Use", f"1. Change Metric switches between Chebyshev & Manhattan heuristic \n2. You can hold down left click to continuously draw obstacles.")
    sim.setup((0, 0), (49, 49), [(10, 1)]) # set up with start at 0,0, goal at 49,49, and a random obstacle at 10,1
    sim.run() # run simulation + visualizer