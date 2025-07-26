from __future__ import annotations
from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.variable import Variable, VarType

from src.try_one.parameters.asset import AssetParameters
from typing import List
# from opt_types import ServiceT
# import service

class Asset:
    
    def __init__(
        self,
        model: ISolver,
        asset_params: AssetParameters,
    ):
        
        self.name = asset_params.name
        self.asset_params = asset_params
        self.model = model
        self._services: List['service.Service'] = []
        for interval in asset_params.intervals:
            model.add_variable(
                Variable(
                    name=f"asset_{asset_params.name}_P_out_t{interval.index}",
                    vtype=VarType.real,
                    lower_bound=asset_params.P_out_min[interval.index],
                    upper_bound=asset_params.P_out_max[interval.index],
                )
            )                
              
            model.add_variable(
                Variable(
                    name=f"asset_{asset_params.name}_P_in_t{interval.index}",
                    vtype=VarType.real,
                    lower_bound=asset_params.P_in_min[interval.index],
                    upper_bound=asset_params.P_in_max[interval.index],
                )
            ) 
               

