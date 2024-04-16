from classes.Simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(51, 51)
    sim.setup((0, 0), (10, 15), [(10, 1)])
    sim.run()