# Vehicular_communications_project
University project that aims to enhance an already existing traffic simulator.</br>
## Credits
The original traffic simulator can be found in this [repo](https://github.com/BilHim/trafficSimulator.git).
## How to run the simulatior?
To run the simulator you can simply run the files inside the examples folder.
> [!NOTE]
> The file `morciano.py` inside the examples/morciano folder is the main file I worked on for this project, so I suggest to run it to see all the new features implemented.
## Improvements
In this section I will describe the added features in chronological order, divided by scope.  
### Road
1. Displayed road direction.
2. Added the possibility to change the road material and speed limit.
3. Added string identifier to identify each road segment (the identifier is mainly used to retrieve the segment index in the simulation, no control on repeated identifier is performed).

### Vehicles
1. Added width attribute to vehicles.
2. Created Car, Truck and Motorbike vehicles with custom initial settings.
3. Added color attribute to vehicles: the color can be selected manually or set accordingly to the type of vehicle.
4. The vehicle generator has been updated to allow the creation of different kind of vehicles.
5. Added information to each vehicle: engine type, engine power, fuel consumption (l/100km), CO2 emissions, rain sensor.

### Simulation
1. When a vehicle exceeds the speed limits the simulation will show a red outline around it.
2. Vehicles can be added to the simulation via a JSON file.
3. The origin point of the vehicles has been moved from the tail to the center of the vehicle for greater and easier control of their movements.
4. Collision between vehicle are detected and displayed in the simulation with the image of an explosion, then the simulation is paused.
5. Collisions are logged into an external file if provided during simulation creation. The log will report the vehicle ids and the collision time and coordinates.
6. A new simulation has been designed, it is called `morciano.py` and its shape is a simplified version of the town of Morciano in Emilia Romagna, Italy.
> [!NOTE]
> The collision detection algorithm is based on AABB (Axis-Aligned-Bounding-Boxes), therefore, even if the outlines of two vehicles
> don't overlap perfectly a collision could be detected. This behaviour is due to the fact that the bounding boxes always form a rectangle aligned with the x-y axes.
