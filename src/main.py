from classes.Simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(51, 51, pass_allow_diagonal=True)
    sim.setup((0, 0), (10, 15), [(10, 1)])
    sim.run()