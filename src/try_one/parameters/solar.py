from dataclasses import dataclass
from typing import List
from .asset import AssetParameters
from .intervals import Interval

@dataclass
class SolarParameters(AssetParameters):
    solar: List[float] 
    
    
    
    
    
    @staticmethod
    def read_solar_data(intervals: List[Interval], solar_vals: List[float]) -> "SolarParameters":
        
        return SolarParameters(
            name="uncontrollable_solar",
            intervals=intervals,
            P_in_max=[0 for _ in intervals],
            P_out_max=[max(solar_vals) for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
            solar=solar_vals,
        )
        