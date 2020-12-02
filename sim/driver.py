from FieldObjects import FieldObject, Obstacle, Drone, Goal
from Drones import *
from RandomSearchDrone import RandomSearchDrone
from ProbabilityDensityDrone import ProbabilityDensityDrone
from Sim import Sim
import time
from random import randint

def rand_pos(max_x, max_y):
    return randint(0, max_x-1), randint(0, max_y-1)

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

def randomMovement():
    field_size = (12,15)
    startX, startY = 0, 0
    sim = Sim(field_size[0], field_size[1])
    sim.setDelay(.2)
    sim.addFieldObject(Obstacle(2, 3))
    sim.addFieldObject(Obstacle(2, 2))
    sim.addFieldObject(Obstacle(2, 1))
    sim.addFieldObject(Obstacle(9, 5))
    sim.addFieldObject(Goal(5, 5))
    # sim.addFieldObject(SimpleDrone(initial_drone_pos, 0, 2, field_size))
    # sim.addFieldObject(SimpleDrone(initial_drone_pos, 1, 2, field_size))
    drones = []
    for i in range(5):
        sim.addFieldObject(RandomMovementDrone(startX, startY + i))

    for i in range(100):
        # sim.print()
        sim.clear_screen()
        print(sim)
        print("=== Simulation is on update {} ===".format(i))
        time.sleep(sim.getDelay())
        if sim.update():        # ADDED THIS
            break
        # if len(drones) > 0:
        #     sim.addFieldObject(drones.pop())
    sim.print()


def randomSearchTest():
    size_x = 10
    size_y = 10
    area = size_x * size_y
    sim = Sim(size_x, size_y)

    #add obstacles
    for _ in range(int(area * 0)):
        pos = rand_pos(size_x, size_y)
        sim.addFieldObject(Obstacle(pos[0], pos[1]))

    #add drones
    for _ in range(int(5)):
        pos = rand_pos(size_x, size_y)
        sim.addFieldObject(RandomSearchDrone(pos[0], pos[1], (size_x, size_y)))

    #add goals
    for _ in range(1):
        pos = rand_pos(size_x, size_y)
        sim.addFieldObject(Goal(pos[0], pos[1]))
    
    #run sim
    s = False
    for i in range(300):
        sim.print()
        # sim.clear_screen()
        # print(sim)
        print("=== Simulation is on update {} ===".format(i))
        time.sleep(sim.getDelay())
        if sim.update():
            break
        if sim.solved:
            s = True
            break
        # if len(drones) > 0:
        #     sim.addFieldObject(drones.pop())
    sim.print() 
    print("Ran for {} itereations".format(i))
    if s:
        print("Congradulations the simulation was solved")
        return True
    return False


def probabilityDensityTest():
    size_x = 20
    size_y = 20
    area = size_x * size_y
    num_drones = 5
    d_start_x = 0
    d_start_y = 0
    sim = Sim(size_x, size_y)

    #add obstacles
    for _ in range(int(10)):
        pos = rand_pos(size_x, size_y)
        if pos == (d_start_x, d_start_y):
            continue
        sim.addFieldObject(Obstacle(pos[0], pos[1]))

    # #add drones in random locations
    # for _ in range(int(5)):
    #     pos = rand_pos(size_x, size_y)
    #     sim.addFieldObject(ProbabilityDensityDrone(pos[0], pos[1], (size_x, size_y)))

    #add goals
    for _ in range(1):
        pos = rand_pos(size_x, size_y)
        sim.addFieldObject(Goal(pos[0], pos[1]))
    
    #run sim
    s = False
    for i in range(50):
        if num_drones > 0:
            if sim.field[d_start_x][d_start_y] == None:
                sim.addFieldObject(ProbabilityDensityDrone(d_start_x, d_start_y, (size_x, size_y)))
                num_drones -= 1

        sim.print()
        # sim.clear_screen()
        # print(sim)
        print("=== Simulation is on update {} ===".format(i))
        time.sleep(sim.getDelay())
        if sim.update():
            break
        if sim.solved:
            s = True
            break
        # if len(drones) > 0:
        #     sim.addFieldObject(drones.pop())
    sim.print() 
    print("Ran for {} itereations".format(i))
    if s:
        print("Congradulations the simulation was solved")
        return True
    return False


if __name__ == "__main__":
    # good()
    # randomMovement()
    # randomSearchTest()
    probabilityDensityTest()