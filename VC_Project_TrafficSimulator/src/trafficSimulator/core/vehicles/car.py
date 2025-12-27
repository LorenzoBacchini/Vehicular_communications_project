from trafficSimulator.core.vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, config={}):
        std_config = {
            "color": (0, 0, 255),
            "l": 4.5,
            "w": 1.8,
            "s0": 4,
            "T": 1,
            "v_max": 33.3,
            "a_max": 2.5,
            "b_max": 5.5,
        }
        # Merge standard config with provided config
        for key, value in config.items():
            std_config[key] = value

        super().__init__(config=std_config)