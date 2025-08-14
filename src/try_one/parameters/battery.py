from dataclasses import dataclass
from typing import List
from .intervals import Interval 
from .asset import AssetParameters



@dataclass
class BatteryParameters(AssetParameters):
    initial_energy: float
    charge_efficiency: float
    discharge_efficiency: float
    energy_capacity: float
    min_soc: float
    
    
    @staticmethod
    def load_constant_battery_data(
        intervals: List[Interval],
        initial_energy: float,
        charge_efficiency: float,
        discharge_efficiency: float,
        energy_capacity: float,
        min_soc: float,
        nominal_power: float,
        
    ) -> "BatteryParameters":
        
        return BatteryParameters(
            name="basic_battery",
            intervals=intervals,
            P_in_max=[nominal_power for _ in intervals],
            P_out_max=[nominal_power for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
            initial_energy=initial_energy,
            charge_efficiency=charge_efficiency,
            discharge_efficiency=discharge_efficiency,
            energy_capacity=energy_capacity,
            min_soc=min_soc,
        )
        
        
    