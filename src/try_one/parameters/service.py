from dataclasses import dataclass
from typing import List, Optional
from .intervals import Interval
from .asset_group import AssetGroupParameters




# do I need power caps for services?
# energy is a service that can be positive or negative -10<=E<=10
# ancillary is a service that can only be positive 0<=A<=10
# do I wish to separate the power out/in for each service?
    
@dataclass
class ServiceParameters:
    name: str
    intervals: List[Interval]
    P_out_max: List[Optional[float]]
    P_in_max: List[Optional[float]]
    P_out_min: List[float]
    P_in_min: List[float]
    
    def __post_init__(self):
        AssetGroupParameters._validate(
            intervals=self.intervals,
            P_out_max=self.P_out_max,
            P_in_max=self.P_in_max,
            P_out_min=self.P_out_min,
            P_in_min=self.P_in_min,
        )