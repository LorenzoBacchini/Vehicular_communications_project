from trafficSimulator.core.vehicle import Vehicle

class Motorbike(Vehicle):
    def __init__(self, config={}):
        std_config = {
            "color": (255, 255, 0),
            "l": 2.1,
            "w": 0.9,
            "s0": 2.0,
            "T": 0.5,
            "v_max": 40.0,
            "a_max": 3.0,
            "b_max": 6.0,
        }
        # Merge standard config with provided config
        for key, value in config.items():
            std_config[key] = value

        super().__init__(config=std_config)