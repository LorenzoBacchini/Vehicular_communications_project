import json
from trafficSimulator import *

def load_vehicles(json_path, sim):
    with open(json_path, "r") as f:
        data = json.load(f)

    vehicle_rate = data.get("vehicle_rate", 10)
    vehicles = []

    for v in data["vehicles"]:
        vehicle_weight = v["weight"]
        vehicle_type = v["type"]

        # Optional dictionaries
        additional_properties = v.get("additional_properties", {})

        # Convert path names → segment indices
        path_indices = [
            sim.get_segment_index_by_identifier(name)
            for name in v["path"]
        ]

        vehicles.append(
            (
                vehicle_weight,
                vehicle_type,
                {
                    **additional_properties,
                    "path": path_indices
                }
            )
        )

    return vehicle_rate, vehicles
