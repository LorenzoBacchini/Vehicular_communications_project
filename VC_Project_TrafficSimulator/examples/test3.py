from trafficSimulator import *

sim = Simulation()

lane_space = 3.5
intersection_size = 12
length = 100

# Order: SOUTH, EAST, NORTH, WEST
# Intersection in
south_in = Segment(points=((1, 150), (1, -150)), material="asphalt", speed_limit=15.5)
sim.add_segment(south_in)
north_in = Segment(points=((-1, -150), (-1, 150)), material="asphalt", speed_limit=15.5)
sim.add_segment(north_in)

vg = VehicleGenerator({
    'vehicle_rate': 20,
    'vehicles': [
        (1, "Car", {'path': [0]}),
        (1, "Truck", {'path': [1]}),
    ]
})

sim.add_vehicle_generator(vg)

win = Window(sim)
win.run()
win.show()