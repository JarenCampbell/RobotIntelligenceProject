from FieldObjects import FieldObject, Obstacle, Drone, Goal
from Drones import *
from RandomSearchDrone import RandomSearchDrone
from ProbabilityDensityDrone import ProbabilityDensityDrone
from RandomMovementDrone import RandomMovementDrone
from Sim import Sim
import time
from random import randint

def rand_pos(max_x, max_y):
    rand_pos = randint(0, max_x-1), randint(0, max_y-1)
    while rand_pos[0] == 0 and rand_pos[1] == 0:
        rand_pos = randint(0, max_x-1), randint(0, max_y-1)
    return rand_pos

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
    sim.setDelay(1)

    #add obstacles
    for _ in range(int(area / 20)):
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
    for i in range(100):
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
    print("Ran for {} iterations".format(i))
    if s:
        print("Congradulations the simulation was solved")
        return True
    return False

def roughDraftSims():
    size_x = 32
    size_y = 32
    area = size_x * size_y

    startX = 0
    startY = 0

    for i in range(3):
        all_num_iter = []
        for j in range(300):
            # Create sim
            sim = Sim(size_x, size_y)
            sim.setDelay(0)

            #add obstacles
            for _ in range(int(area / 10)):
                pos = rand_pos(size_x, size_y)
                sim.addFieldObject(Obstacle(pos[0], pos[1]))

            #add drones
            # for k in range(int(5)):
            #     if i == 0:
            #         sim.addFieldObject(RandomMovementDrone(startX, startY))
            #     elif i == 1:
            #         sim.addFieldObject(RandomSearchDrone(startX, startY, (size_x, size_y)))
            #     else:
            #         sim.addFieldObject(ProbabilityDensityDrone(startX, startY, (size_x, size_y)))

            num_drones = 5

            #add goals
            for _ in range(1):
                pos = rand_pos(size_x, size_y)
                sim.addFieldObject(Goal(pos[0], pos[1]))
            
            num_iter = 0
            for k in range(10000):
                if num_drones > 0:
                    if sim.field[startX][startY] == None:
                        if i == 0:
                            sim.addFieldObject(RandomMovementDrone(startX, startY))
                        elif i == 1:
                            sim.addFieldObject(RandomSearchDrone(startX, startY, (size_x, size_y)))
                        else:
                            sim.addFieldObject(ProbabilityDensityDrone(startX, startY, (size_x, size_y)))
                        num_drones -= 1
                
                # sim.print()
                # print("=== Simulation is on update {} ===".format(k))
                
                time.sleep(sim.getDelay())
                if sim.update():
                    num_iter = k
                    break
                num_iter = k
            all_num_iter.append(num_iter)
            
            # print("Number of iterations required:", num_iter)
        print("Average number of iterations required:", str(sum(all_num_iter) / len(all_num_iter)))

def increasingSizeSims():
    sizes = [(20, 20), (40, 40), (60, 60), (80, 80), (100,100)]

    startX = 0
    startY = 0

    
    for size_x, size_y in sizes:
        with open("output.txt", "a") as output:
            area = size_x * size_y
            print()
            print("MAP SIZE: " + str(size_x) + "x" + str(size_y))
            output.write("\nMAP SIZE: " + str(size_x) + "x" + str(size_y) + "\n")
            for i in range(3):
                all_num_iter = []
                for j in range(300):
                    # Create sim
                    sim = Sim(size_x, size_y)
                    sim.setDelay(0)

                    #add obstacles
                    for _ in range(int(area / 10)):
                        pos = rand_pos(size_x, size_y)
                        sim.addFieldObject(Obstacle(pos[0], pos[1]))

                    #add drones
                    # for k in range(int(5)):
                    #     if i == 0:
                    #         sim.addFieldObject(RandomMovementDrone(startX, startY))
                    #     elif i == 1:
                    #         sim.addFieldObject(RandomSearchDrone(startX, startY, (size_x, size_y)))
                    #     else:
                    #         sim.addFieldObject(ProbabilityDensityDrone(startX, startY, (size_x, size_y)))

                    num_drones = 5

                    #add goals
                    for _ in range(1):
                        pos = rand_pos(size_x, size_y)
                        sim.addFieldObject(Goal(pos[0], pos[1]))
                    
                    num_iter = 0
                    for k in range(200 * size_x):
                        if num_drones > 0:
                            if sim.field[startX][startY] == None:
                                if i == 0:
                                    sim.addFieldObject(RandomMovementDrone(startX, startY))
                                elif i == 1:
                                    sim.addFieldObject(RandomSearchDrone(startX, startY, (size_x, size_y)))
                                else:
                                    sim.addFieldObject(ProbabilityDensityDrone(startX, startY, (size_x, size_y)))
                                num_drones -= 1
                        
                        # sim.print()
                        # print("=== Simulation is on update {} ===".format(k))
                        
                        time.sleep(sim.getDelay())
                        if sim.update():
                            num_iter = k
                            break
                        num_iter = k
                    all_num_iter.append(num_iter)
                    
                    # print("Number of iterations required:", num_iter)
                print("Average number of iterations required: " + str(sum(all_num_iter) / len(all_num_iter)))
                output.write("Average number of iterations required: " + str(sum(all_num_iter) / len(all_num_iter)) + "\n")

            # size_x *= 2
            # size_y *= 2

def increasingDroneSims():
    size_x = 40
    size_y = 40
    area = size_x * size_y
    drones = [24, 26, 28, 30, 32, 34, 36, 38, 40]
    # drones = [32]

    startX = 0
    startY = 0

    
    for num_drones in drones:
        with open("output3.txt", "a") as output:
            print()
            print("NUM DRONES: " + str(num_drones))
            output.write("\nNUM DRONES: " + str(num_drones) + "\n")
            for i in range(3):
                all_num_iter = []
                for j in range(100):
                    # Create sim
                    sim = Sim(size_x, size_y)
                    sim.setDelay(0)

                    #add obstacles
                    for _ in range(int(area / 10)):
                        pos = rand_pos(size_x, size_y)
                        sim.addFieldObject(Obstacle(pos[0], pos[1]))

                    #add drones
                    # for k in range(int(5)):
                    #     if i == 0:
                    #         sim.addFieldObject(RandomMovementDrone(startX, startY))
                    #     elif i == 1:
                    #         sim.addFieldObject(RandomSearchDrone(startX, startY, (size_x, size_y)))
                    #     else:
                    #         sim.addFieldObject(ProbabilityDensityDrone(startX, startY, (size_x, size_y)))

                    num_drones_iter = num_drones

                    #add goals
                    for _ in range(1):
                        pos = rand_pos(size_x, size_y)
                        sim.addFieldObject(Goal(pos[0], pos[1]))
                    
                    num_iter = 0
                    for k in range(200 * size_x):
                        if num_drones_iter > 0:
                            if sim.field[startX][startY] == None:
                                if i == 0:
                                    sim.addFieldObject(RandomMovementDrone(startX, startY))
                                elif i == 1:
                                    sim.addFieldObject(RandomSearchDrone(startX, startY, (size_x, size_y)))
                                else:
                                    sim.addFieldObject(ProbabilityDensityDrone(startX, startY, (size_x, size_y)))
                                num_drones_iter -= 1
                        
                        # sim.print()
                        # print("=== Simulation is on update {} ===".format(k))
                        
                        time.sleep(sim.getDelay())
                        num_iter = k
                        if sim.update():
                            break
                    all_num_iter.append(num_iter)
                    
                    # print("Number of iterations required:", num_iter)
                print("Average number of iterations required: " + str(sum(all_num_iter) / len(all_num_iter)))
                output.write("Average number of iterations required: " + str(sum(all_num_iter) / len(all_num_iter)) + "\n")

            # size_x *= 2
            # size_y *= 2

if __name__ == "__main__":
    # good()
    # randomMovement()
    # randomSearchTest()
    probabilityDensityTest()

    # roughDraftSims()
    # increasingSizeSims()
    # increasingDroneSims()