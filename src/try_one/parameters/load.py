from dataclasses import dataclass
from typing import List
from .asset import AssetParameters
from .intervals import Interval

@dataclass
class LoadParameters(AssetParameters):
    load: List[float] 
    
    
    
    
    
    @staticmethod
    def read_load_data(intervals: List[Interval], load_vals: List[float]) -> "LoadParameters":
        
        return LoadParameters(
            name="uncontrollable_load",
            intervals=intervals,
            P_in_max=[max(load_vals) for _ in intervals],
            P_out_max=[0 for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
            load=load_vals,
        )
