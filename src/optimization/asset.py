from __future__ import annotations
from model import Model, VarType
from parameters.asset import AssetParameters
from typing import List
# from opt_types import ServiceT
# import service

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
            # if asset_params.P_out_max[interval.index] != 0:
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
                
            # if asset_params.P_in_max[interval.index] != 0:
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
        



    # def add_services(self, services: List['service.Service']) -> None:
    #     self._services += services
        
    # # Construct method
    # def add_service_constraints(self) -> None:
    #     for interval in self.asset_params.intervals:
    #         if self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}") is not None:
    #             self.model.add_constraint(
    #                 name=f"asset_{self.name}_P_out_t{interval.index}_services_requirement",
    #                 constraint=(
    #                     self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}")
    #                     == self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{self.name}_service_{service.name}_P_out_t{interval.index}_var")
    #                             for service in self._services
    #                         ]
    #                     )
    #                 ),
    #             )
                
    #             self.model.add_constraint(
    #                 name=f"asset_{self.name}_E_out_t{interval.index}_services_requirement",
    #                 constraint=(
    #                     self.model.get_var(f"asset_{self.name}_E_out_t{interval.index}")
    #                     == self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{self.name}_service_{service.name}_E_out_t{interval.index}_var")
    #                             for service in self._services
    #                         ]
    #                     )
    #                 ),
    #             )
            
    #         if self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}") is not None:
    #             self.model.add_constraint(
    #                 name=f"asset_{self.name}_P_in_t{interval.index}_services_requirement",
    #                 constraint=(
    #                     self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}")
    #                     == self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{self.name}_service_{service.name}_P_in_t{interval.index}_var")
    #                             for service in self._services
    #                         ]
    #                     )
    #                 ),
    #             )
                
    #             self.model.add_constraint(
    #                 name=f"asset_{self.name}_E_in_t{interval.index}_services_requirement",
    #                 constraint=(
    #                     self.model.get_var(f"asset_{self.name}_E_in_t{interval.index}")
    #                     == self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{self.name}_service_{service.name}_E_in_t{interval.index}_var")
    #                             for service in self._services
    #                         ]
    #                     )
    #                 ),
    #             )

    #     return
                      
    