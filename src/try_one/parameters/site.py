from dataclasses import dataclass
from typing import List
from .asset_group import AssetGroupParameters
from .intervals import Interval



@dataclass
class SiteParameters(AssetGroupParameters):
    pass


    @staticmethod
    def create_constant_limit_site(
        intervals: List[Interval], 
        P_in_limit: float,
        P_out_limit: float,
    ) -> "SiteParameters":
        return SiteParameters(
            name="constant_limit_site",
            intervals=intervals,
            P_in_max=[P_in_limit for _ in intervals],
            P_out_max=[P_out_limit for _ in intervals],
            P_in_min=[0 for _ in intervals],
            P_out_min=[0 for _ in intervals],
        )
            