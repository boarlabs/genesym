from dataclasses import dataclass
from typing import List, Optional
from .intervals import Interval

@dataclass
class AssetGroupParameters:
    name: str
    intervals: List[Interval]
    P_out_max: List[Optional[float]]
    P_in_max: List[Optional[float]]
    P_out_min: List[float] 
    P_in_min: List[float]
    
    
    def _post_init__(self):
        self._validate(
            intervals=self.intervals,
            P_out_max=self.P_out_max,
            P_in_max=self.P_in_max,
            P_out_min=self.P_out_min,
            P_in_min=self.P_in_min,
        )
    
    
    def _validate(intervals, P_out_max, P_in_max, P_out_min, P_in_min):
        
        if len(intervals) != len(P_out_max):
            raise ValueError(
                "The number of intervals must be equal to the number of P_out_max values"
            )
        if len(intervals) != len(P_in_max):
            raise ValueError(
                "The number of intervals must be equal to the number of P_in_max values"
            )
        if len(intervals) != len(P_out_min):
            raise ValueError(
                "The number of intervals must be equal to the number of P_out_min values"
            )
        if len(intervals) != len(P_in_min):
            raise ValueError(
                "The number of intervals must be equal to the number of P_in_min values"
            )
        
        
        for i in range(len(intervals)):
            
            if P_out_max[i] is not None:
                if P_out_max[i] < 0:
                    raise ValueError(
                        "P_out_max must be greater than 0"
                    )
                if P_out_max[i] < P_out_min[i]:
                    raise ValueError(
                        "P_out_max must be greater than P_out_min"
                    )
            
            if P_in_max[i] is not None:
                if P_in_max[i] < 0:
                    raise ValueError(
                        "P_in_max must be greater than 0"
                    )
                if P_in_max[i] < P_in_min[i]:
                    raise ValueError(
                        "P_in_max must be greater than P_in_min"
                    )
            
            if P_out_min[i] < 0:
                raise ValueError(
                    "P_in_max must be greater than 0"
                )
            if P_in_min[i] < 0:
                raise ValueError(
                    "P_in_min must be greater than 0"
                )
            
            
            
                
                
                
     