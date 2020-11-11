FieldObjects.py holds the base classes and some child classes for all objects in the simulation environment
Sim.py holds the class that that runs the simulation. 

To impliment algorithms, create a new class that is a child of Drone and overrides the update method.
put your algorithm in this update method.
TestDrone1 and TestDrone2 are basic example implimentations at the bottom of FieldObjects.py

Feel free to make new files to hold your implimentaton classes and feel free to change driver.py however you need.