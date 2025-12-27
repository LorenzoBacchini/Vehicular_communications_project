from trafficSimulator.core.vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, config={}):
        std_config = {
            "color": (0, 255, 255),
            "l": 12.0,
            "w": 2.5,
            "s0": 6.0,
            "T": 2.0,
            "v_max": 25.0,
            "a_max": 1.2,
            "b_max": 4.0,
        }
        # Merge standard config with provided config
        for key, value in config.items():
            std_config[key] = value

        super().__init__(config=std_config)
