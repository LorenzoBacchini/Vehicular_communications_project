from .segment import Segment

CURVE_RESOLUTION = 50

class CubicCurve(Segment):
    def __init__(self, start, control_1, control_2, end, material=None, speed_limit=None, identifier=None):
        # Store characteristic points
        self.start = start
        self.control_1 = control_1
        self.control_2 = control_2
        self.end = end

        # Generate path
        path = []
        for i in range(CURVE_RESOLUTION):
            t = i/CURVE_RESOLUTION
            x = t**3*self.end[0] + 3*t**2*(1-t)*self.control_2[0] + 3*(1-t)**2*t*self.control_1[0] + (1-t)**3*self.start[0]
            y = t**3*self.end[1] + 3*t**2*(1-t)*self.control_2[1] + 3*(1-t)**2*t*self.control_1[1] + (1-t)**3*self.start[1]
            path.append((x, y))

        super().__init__(path, material=material, speed_limit=speed_limit, identifier=identifier)
        # Arc-length parametrization
        normalized_path = self.find_normalized_path(CURVE_RESOLUTION)
        super().__init__(normalized_path, material=material, speed_limit=speed_limit, identifier=identifier)

    def get_absolute_position(self, progress):
        """
        Compute the absolute position (x, y) of a vehicle in the global simulation.
        The input `progress` is the distance along the cubic curve.
        """
        progress = progress/self.get_length() # Normalize progress to [0, 1]
        clamp_progress = max(0, min(1, progress)) # Clamp to [0, 1]
        return [self.compute_x(clamp_progress), self.compute_y(clamp_progress)] # Interpolated 2D point
    
    def compute_x(self, t):
        return t**3*self.end[0] + 3*t**2*(1-t)*self.control_2[0] + 3*(1-t)**2*t*self.control_1[0] + (1-t)**3*self.start[0]
    
    def compute_y(self, t):
        return t**3*self.end[1] + 3*t**2*(1-t)*self.control_2[1] + 3*(1-t)**2*t*self.control_1[1] + (1-t)**3*self.start[1]
    
    def compute_dx(self, t):
        return 3*t**2*(self.end[0]-3*self.control_2[0]+3*self.control_1[0]-self.start[0]) + 6*t*(self.control_2[0]-2*self.control_1[0]+self.start[0]) + 3*(self.control_1[0]-self.start[0])
    
    def compute_dy(self, t):
        return 3*t**2*(self.end[1]-3*self.control_2[1]+3*self.control_1[1]-self.start[1]) + 6*t*(self.control_2[1]-2*self.control_1[1]+self.start[1]) + 3*(self.control_1[1]-self.start[1])
