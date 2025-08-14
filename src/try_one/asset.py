from __future__ import annotations
from model import Model, VarType
from parameters.asset import AssetParameters
from typing import List

class Asset:
    
    def __init__(
        self,
        model: Model,
        asset_params: AssetParameters,
    ):
        
        self.name = asset_params.name
        self.asset_params = asset_params
        self.model = model
        self._services: List['service.Service'] = []
        for interval in asset_params.intervals:
            model.add_var(
                name=f"asset_{asset_params.name}_P_out_t{interval.index}",
                var_type=VarType.REAL,
                lb=asset_params.P_out_min[interval.index],
                ub=asset_params.P_out_max[interval.index],
            )
            
            # model.add_var(
            #     name=f"asset_{asset_params.name}_E_out_t{interval.index}",
            #     var_type=VarType.REAL,
            #     lb=asset_params.P_out_min[interval.index],
            #     ub=asset_params.P_out_max[interval.index],
            # )
                
            model.add_var(
                name=f"asset_{asset_params.name}_P_in_t{interval.index}",
                var_type=VarType.REAL,
                lb=asset_params.P_in_min[interval.index],
                ub=asset_params.P_in_max[interval.index],
            ) 
            # model.add_var(
            #     name=f"asset_{asset_params.name}_E_in_t{interval.index}",
            #     var_type=VarType.REAL,
            #     lb=asset_params.P_in_min[interval.index],
            #     ub=asset_params.P_in_max[interval.index],
            # )
        


