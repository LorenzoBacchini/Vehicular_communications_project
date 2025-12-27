from trafficSimulator import *

sim = Simulation()

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
    'vehicles': [
        (1, "Car", {'path': [sim.get_segment_index(south_in), 12, 5]}),
        (1, "Truck", {'path': [0, 16, 7]}),
        (1, "Motorbike", {'path': [0, 8, 6]}),
    ]
})

sim.add_vehicle_generator(vg)

win = Window(sim)
win.run()
win.show()