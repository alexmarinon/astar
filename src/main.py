from classes.Simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(50, 50, pass_allow_diagonal=True)
    sim.setup((0, 0), (49, 49), [(10, 1)])
    sim.run()