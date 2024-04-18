from classes.Simulation import Simulation
from tkinter import messagebox

def show_popup():
    messagebox.showinfo("Important Info on How to Use", f"1. Change Metric switches between Chebyshev & Manhattan heuristic \n2. You can hold down left click to continuously draw obstacles.")

if __name__ == "__main__": # standard, doesnt run if used as part of a module or package
    show_popup()
    sim = Simulation(50, 50, pass_allow_diagonal=True) # create simulation object with grid 50x50 and using chevyshev distance
    sim.setup((0, 0), (49, 49), [(10, 1)]) # set up with start at 0,0, goal at 49,49, and a random obstacle at 10,1
    sim.run() # run simulation + visualizer