from trafficSimulator import *

sim = Simulation("VC_Project_TrafficSimulator/examples/log_test.txt")

lane_space = 3.5
intersection_size = 12
length = 100

# Order: SOUTH, EAST, NORTH, WEST
# Intersection in
south_in = Segment(points=((lane_space/2, length+intersection_size/2), (lane_space/2, intersection_size/2)), material="asphalt", speed_limit=15.5)
sim.add_segment(south_in)
#sim.create_segment(points=((lane_space/2, length+intersection_size/2), (lane_space/2, intersection_size/2)), material="concrete", speed_limit=50)
sim.create_segment(points=((length+intersection_size/2, -lane_space/2), (intersection_size/2, -lane_space/2)))
sim.create_segment(points=((-lane_space/2, -length-intersection_size/2), (-lane_space/2, -intersection_size/2)))
sim.create_segment(points=((-length-intersection_size/2, lane_space/2), (-intersection_size/2, lane_space/2)))
# Intersection out
sim.create_segment(points=((-lane_space/2, intersection_size/2), (-lane_space/2, length+intersection_size/2)))
sim.create_segment(points=((intersection_size/2, lane_space/2), (length+intersection_size/2, lane_space/2)))
sim.create_segment(points=((lane_space/2, -intersection_size/2), (lane_space/2, -length-intersection_size/2)))
sim.create_segment(points=((-intersection_size/2, -lane_space/2), (-length-intersection_size/2, -lane_space/2)))
# Straight
sim.create_segment(points=((lane_space/2, intersection_size/2), (lane_space/2, -intersection_size/2)))
sim.create_segment(points=((intersection_size/2, -lane_space/2), (-intersection_size/2, -lane_space/2)))
sim.create_segment(points=((-lane_space/2, -intersection_size/2), (-lane_space/2, intersection_size/2)))
sim.create_segment(points=((-intersection_size/2, lane_space/2), (intersection_size/2, lane_space/2)))
# Right turn
sim.create_quadratic_bezier_curve((lane_space/2, intersection_size/2), (lane_space/2, lane_space/2), (intersection_size/2, lane_space/2))
sim.create_quadratic_bezier_curve((intersection_size/2, -lane_space/2), (lane_space/2, -lane_space/2), (lane_space/2, -intersection_size/2))
sim.create_quadratic_bezier_curve((-lane_space/2, -intersection_size/2), (-lane_space/2, -lane_space/2), (-intersection_size/2, -lane_space/2))
sim.create_quadratic_bezier_curve((-intersection_size/2, lane_space/2), (-lane_space/2, lane_space/2), (-lane_space/2, intersection_size/2))
# Left turn
sim.create_quadratic_bezier_curve((lane_space/2, intersection_size/2), (lane_space/2, -lane_space/2), (-intersection_size/2, -lane_space/2))
sim.create_quadratic_bezier_curve((intersection_size/2, -lane_space/2), (-lane_space/2, -lane_space/2), (-lane_space/2, intersection_size/2))
sim.create_quadratic_bezier_curve((-lane_space/2, -intersection_size/2), (-lane_space/2, lane_space/2), (intersection_size/2, lane_space/2))
sim.create_quadratic_bezier_curve((-intersection_size/2, lane_space/2), (lane_space/2, lane_space/2), (lane_space/2, -intersection_size/2))


vg = VehicleGenerator({
    'vehicle_rate': 20,
    'vehicles': [
        (1, "Car", {'path': [sim.get_segment_index(south_in), 16, 7]}),
        (1, "Truck", {'path': [3, 19, 6]}),
        (1, "Motorbike", {'path': [0, 8, 6]}),
        (2, "Truck", {'v': 12.5, 'path': [2, 18, 5]}),
    ]
})

sim.add_vehicle_generator(vg)

win = Window(sim)
win.run()
win.show()