from .vehicle_generator import VehicleGenerator
from .geometry.quadratic_curve import QuadraticCurve
from .geometry.cubic_curve import CubicCurve
from .geometry.segment import Segment
from .vehicle import Vehicle
import numpy as np


class Simulation:
    def __init__(self, crashes_log=None):
        self.segments = []
        self.vehicles = {}
        self.vehicle_generator = []
        self.crash = False
        self.crashes = []
        self.crashes_log = crashes_log
        self.t = 0.0
        self.frame_count = 0
        self.dt = 1/60  


    def add_vehicle(self, veh):
        self.vehicles[veh.id] = veh
        if len(veh.path) > 0:
            self.segments[veh.path[0]].add_vehicle(veh)

    def add_segment(self, seg):
        self.segments.append(seg)

    def add_vehicle_generator(self, gen):
        self.vehicle_generator.append(gen)

    def create_vehicle(self, **kwargs):
        veh = Vehicle(kwargs)
        self.add_vehicle(veh)

    def create_segment(self, points, material=None, speed_limit=None):
        seg = Segment(points, material=material, speed_limit=speed_limit)
        self.add_segment(seg)

    def create_quadratic_bezier_curve(self, start, control, end):
        cur = QuadraticCurve(start, control, end)
        self.add_segment(cur)

    def create_cubic_bezier_curve(self, start, control_1, control_2, end):
        cur = CubicCurve(start, control_1, control_2, end)
        self.add_segment(cur)

    def create_vehicle_generator(self, **kwargs):
        gen = VehicleGenerator(kwargs)
        self.add_vehicle_generator(gen)

    def get_segment_index(self, segment):
        return self.segments.index(segment)

    def get_segment_index_by_identifier(self, identifier):
        for i, segment in enumerate(self.segments):
            if segment.identifier == identifier:
                return i
        return -1

    def run(self, steps):
        # Reset crash status for this run
        self.crash = False
        for _ in range(steps):
            self.update()

    '''
    2D Rectangle Vertices Computation Function
    Given the center (x, y), length, width, and rotation angle theta (in radians),
    compute the coordinates of the four vertices of the vehicle.
    '''
    def compute_vertices(self, x, y, length, width, theta):
        hl = length / 2
        hw = width / 2

        # Local vertices (relative to the center)
        local = np.array([
            [-hl, -hw],
            [ hl, -hw],
            [ hl,  hw],
            [-hl,  hw]
        ])

        # Rotation matrix
        c = np.cos(theta)
        s = np.sin(theta)
        R = np.array([
            [c, -s],
            [s,  c]
        ])

        # Rotate and translate vertices to global coordinates
        rotated = local @ R.T
        translated = rotated + np.array([x, y])

        return translated

    '''
    Collision Detection Function
    Separating Axis Theorem (SAT) for rectangle-rectangle collision detection
    Given a list of encumbrances (bounding boxes) for all vehicles,
    check for collisions and log crashes.
    '''
    def check_crashes(self, encumbrances=[]):
        for i in range(len(encumbrances)):
            x_min, x_max, y_min, y_max, id, x, y = encumbrances[i]
            for j in range(i+1, len(encumbrances)):
                '''
                found becomes true if a crash between the two vehicles has already been logged
                avoids duplicate logging of the same crash
                '''
                found = False
                x_min_1, x_max_1, y_min_1, y_max_1, id_1, x_1, y_1 = encumbrances[j]
                
                # Check for overlap using AABB method
                if (x_max < x_min_1) or (x_min > x_max_1):
                    # No overlap on x-axis, no possible crash
                    continue
                elif (y_max < y_min_1) or (y_min > y_max_1):
                    # No overlap on y-axis, no possible crash
                    continue
                else:
                    # A crash is detected
                    for crash in self.crashes:
                        # check if this crash has already been logged
                        crash_id, crash_id_1, _, _, _ = crash
                        if (crash_id == id and crash_id_1 == id_1) or (crash_id == id_1 and crash_id_1 == id):
                            found = True
                    # if found is true, skip logging
                    if found == True:
                        continue
                    else:
                        # Log the crash
                        # Compute average crash position (not accurate)
                        x = (x + x_1)/2
                        y = (y + y_1)/2
                        # Append crash to the recent crashes list
                        self.crashes.append((id, id_1, self.t, x, y))
                        # Write crash to log file if specified
                        if self.crashes_log is not None:
                            with open(self.crashes_log, "a") as f:
                                f.write(f"Crash detected between vehicle {id} and vehicle {id_1} at time {self.t:.2f}s and coordinates ({x:.2f}, {y:.2f})\n")
                        # Set crash flag to true
                        self.crash = True                

    '''
    Vehicle Encumbrance Computation Function
    For a given vehicle on a segment, compute its bounding box (encumbrance) and append it to the encumbrances list.
    The bounding box is represented as (x_min, x_max, y_min, y_max, vehicle_id, center_x, center_y).
    '''
    def compute_encumbrance(self, segment, vehicle, encumbrances=[]):
        x, y = segment.get_absolute_position(vehicle.x)
        length = vehicle.l
        width = vehicle.w
        progress = vehicle.x / segment.get_length()
        # Ensure progress is within [0, 1]
        clamp_progress = max(0, min(1, progress))
        heading = segment.get_heading(clamp_progress)
        
        # Compute the four corners of the vehicle
        corners = self.compute_vertices(x, y, length, width, heading)
        # Determine bounding box from corners
        x_min = min(corners[:, 0])
        x_max = max(corners[:, 0])
        y_min = min(corners[:, 1])
        y_max = max(corners[:, 1])

        # Append encumbrance to the list of current vehicle encumbrances
        encumbrances.append((x_min, x_max, y_min, y_max, str(vehicle.id), x, y))

    '''
    Recent Crashes Cleanup Function
    Remove crashes that occurred more than 1 second ago from the recent crashes list.
    This function is important because in the check_crashes function, crashes are only logged once if
    they are already in the recent crashes list. So to allow the registration of new crashes between the same vehicles
    after some time has passed, we need to clear out old crashes.
    '''
    def clear_crashes(self):
        for crash in self.crashes:
            _, _, t, _, _ = crash
            # If crash occurred more than 1 second ago, remove it from the list
            if self.t - t > 1.0:
                self.crashes.remove(crash)

    def update(self):
        # List to hold vehicle encumbrances for collision detection
        encumbrances = []
        # Update vehicles
        for segment in self.segments:
            if len(segment.vehicles) != 0:
                self.vehicles[segment.vehicles[0]].update(None, self.dt)
                # Compute encumbrance for the first vehicle
                self.compute_encumbrance(segment, self.vehicles[segment.vehicles[0]], encumbrances)

            for i in range(1, len(segment.vehicles)):
                self.vehicles[segment.vehicles[i]].update(self.vehicles[segment.vehicles[i-1]], self.dt)
                # Compute encumbrance for the following vehicles
                self.compute_encumbrance(segment, self.vehicles[segment.vehicles[i]], encumbrances)

        # Check roads for out of bounds vehicle
        for segment in self.segments:
            # If road has no vehicles, continue
            if len(segment.vehicles) == 0: continue
            # If not
            vehicle_id = segment.vehicles[0]
            vehicle = self.vehicles[vehicle_id]
            # If first vehicle is out of road bounds
            if vehicle.x >= segment.get_length():
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.segments[next_road_index].vehicles.append(vehicle_id)
                # Reset vehicle properties
                vehicle.x = 0
                # In all cases, remove it from its road
                segment.vehicles.popleft() 

        # Update vehicle generators
        for gen in self.vehicle_generator:
            gen.update(self)

        # Clear old crashes and check for new crashes
        self.clear_crashes()
        self.check_crashes(encumbrances)

        # Increment time
        self.t += self.dt
        self.frame_count += 1
