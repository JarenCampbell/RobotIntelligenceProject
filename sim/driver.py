from FieldObjects import *
from Sim import Sim
import time

def example_main():
    sim = Sim(10, 25)
    sim.setDelay(1.5)
    sim.addFieldObject(Obstacle(2, 3))
    sim.addFieldObject(Obstacle(2, 2))
    sim.addFieldObject(Obstacle(2, 1))
    sim.addFieldObject(Obstacle(9, 5))
    sim.addFieldObject(Goal(8, 12))
    sim.addFieldObject(TestDrone1(4, 5))
    sim.addFieldObject(TestDrone2(2, 11))

    for i in range(9):
        sim.print()
        print("=== Simulation is on update {} ===".format(i))
        time.sleep(sim.getDelay())
        sim.update()
    sim.print()

example_main()