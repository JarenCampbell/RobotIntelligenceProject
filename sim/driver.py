from FieldObjects import *
from Sim import Sim
import time

def good():
    field_size = (12,15)
    initial_drone_pos = (0,0)
    sim = Sim(field_size[0], field_size[1])
    sim.setDelay(.2)
    sim.addFieldObject(Obstacle(2, 3))
    sim.addFieldObject(Obstacle(2, 2))
    sim.addFieldObject(Obstacle(2, 1))
    sim.addFieldObject(Obstacle(9, 5))
    sim.addFieldObject(Goal(8, 12))
    sim.addFieldObject(SimpleDrone(initial_drone_pos, 0, 2, field_size))
    sim.addFieldObject(SimpleDrone(initial_drone_pos, 1, 2, field_size))
    drones = [SimpleDrone(initial_drone_pos, 0, 3, field_size), SimpleDrone(initial_drone_pos, 1, 3, field_size), SimpleDrone(initial_drone_pos, 2, 3, field_size)]

    for i in range(100):
        # sim.print()
        sim.clear_screen()
        print(sim)
        print("=== Simulation is on update {} ===".format(i))
        time.sleep(sim.getDelay())
        sim.update()
        if len(drones) > 0:
            sim.addFieldObject(drones.pop())
    sim.print()

good()

