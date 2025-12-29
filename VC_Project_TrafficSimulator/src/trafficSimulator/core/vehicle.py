import uuid
import numpy as np

class Vehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()
        
    def set_default_config(self):    
        self.id = uuid.uuid4()

        # visual propertie
        self.color = (0, 0, 255)
        # length of the vehicle
        self.l = 4
        # width of the vehicle
        self.w = 1.76
        # safety distance from the vehicle in front
        self.s0 = 4
        # desired time headway (s)
        self.T = 1
        # maximum velocity (m/s)        
        self.v_max = 16.6
        # maximum acceleration (m/s^2)
        self.a_max = 1.44
        # comfortable deceleration (m/s^2)
        self.b_max = 4.61
        # engine type: "combustion", "electric", "hybrid"
        self.engine_type = "combustion"
        # engine power (kW)
        self.engine_power = 100
        # fuel consumption (l/100km)
        self.fuel_consumption = 6.5
        # co2 emissions (g/km)
        self.CO2_emissions = 180
        # rain detection sensor
        self.rain_sensor = False

        # path as list of segment indices
        self.path = []
        '''
         Index of the current road in the path list.
         For example, if path = [0, 3, 5] and current_road_index = 1,
         the vehicle is currently on road 3 and will go to road 5 next.
        '''
        self.current_road_index = 0

        # dynamic states
        self.x = 0
        # velocity
        self.v = 0
        # acceleration
        self.a = 0
        self.stopped = False

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max
        