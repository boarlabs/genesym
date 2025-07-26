from __future__ import annotations
from abc import abstractmethod

from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.variable import Variable, VarType

from src.try_one.parameters.service import ServiceParameters

class Service:
    def __init__(
        self,
        model: ISolver,
        service_params: ServiceParameters,
    ):
        
        self.name = service_params.name
        self.service_params = service_params
        self.model = model
        
        for interval in service_params.intervals:
            model.add_variable(
                Variable(
                    name=f"service_{service_params.name}_P_out_t{interval.index}",
                    vtype=VarType.real,
                    lower_bound=service_params.P_out_min[interval.index],
                    upper_bound=service_params.P_out_max[interval.index],
                )
            )
             
            model.add_variable(
                Variable(
                    name=f"service_{service_params.name}_P_in_t{interval.index}",
                    vtype=VarType.real,
                    lower_bound=service_params.P_in_min[interval.index],
                    upper_bound=service_params.P_in_max[interval.index],
                )
            )
             


    # def add_assets(self, assets: List[Asset]) -> None:
        
    #     for asset in assets:
    #         for interval in self.service_params.intervals:
    #             if (self.model.get_var(f"asset_{asset.name}_P_out_t{interval.index}") is not None) \
    #                 and (self.model.get_var(f"service_{self.name}_P_out_t{interval.index}") is not None):
    #                     self.model.add_var(
    #                         name=f"asset_{asset.name}_service_{self.name}_P_out_t{interval.index}_var",
    #                         var_type=VarType.REAL,
    #                         lb=0,
    #                         ub=self.service_params.P_out_max[interval.index],
    #                         # this could be bound to either asset or service power caps, or maybe both?
    #                     )
                        
    #                     self.model.add_var(
    #                         name=f"asset_{asset.name}_service_{self.name}_E_out_t{interval.index}_var",
    #                         var_type=VarType.REAL,
    #                         lb=0,
    #                         ub=self.service_params.P_out_max[interval.index],
    #                         # this could be bound to either asset or service power caps, or maybe both?
    #                     )
                        
                        
    #             if (self.model.get_var(f"asset_{asset.name}_P_in_t{interval.index}") is not None) \
    #                 and (self.model.get_var(f"service_{self.name}_P_in_t{interval.index}") is not None):
    #                     self.model.add_var(
    #                         name=f"asset_{asset.name}_service_{self.name}_P_in_t{interval.index}_var",
    #                         var_type=VarType.REAL,
    #                         lb=0,
    #                         ub=self.service_params.P_in_max[interval.index],
    #                     )
                        
    #                     self.model.add_var(
    #                         name=f"asset_{asset.name}_service_{self.name}_E_in_t{interval.index}_var",
    #                         var_type=VarType.REAL,
    #                         lb=0,
    #                         ub=self.service_params.P_in_max[interval.index],
    #                     )
                
    #     for interval in self.service_params.intervals:
            
    #         if self.model.get_var(f"service_{self.name}_P_out_t{interval.index}") is not None:
    #             self.model.add_constraint(
    #                 name=f"service_{self.name}_P_out_t{interval.index}_asset_bind",
    #                 constraint=(
    #                     self.model.get_var(f"service_{self.name}_P_out_t{interval.index}")
    #                     ==  self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{asset.name}_service_{self.name}_P_out_t{interval.index}_var")
    #                             for asset in assets
    #                         ]
    #                     )
    #                 ),
    #             )
    #             self.model.add_constraint(
    #                 name=f"service_{self.name}_E_out_t{interval.index}_asset_bind",
    #                 constraint=(
    #                     self.model.get_var(f"service_{self.name}_E_out_t{interval.index}")
    #                     ==  self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{asset.name}_service_{self.name}_E_out_t{interval.index}_var")
    #                             for asset in assets
    #                         ]
    #                     )
    #                 ),
    #             )
            
    #         if self.model.get_var(f"service_{self.name}_P_in_t{interval.index}") is not None:
    #             self.model.add_constraint(
    #                 name=f"service_{self.name}_P_in_t{interval.index}_asset_bind",
    #                 constraint=(
    #                     self.model.get_var(f"service_{self.name}_P_in_t{interval.index}")
    #                     == self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{asset.name}_service_{self.name}_P_in_t{interval.index}_var")
    #                             for asset in assets
    #                         ]
    #                     )
    #                 ),
    #             )
                
    #             self.model.add_constraint(
    #                 name=f"service_{self.name}_E_in_t{interval.index}_asset_bind",
    #                 constraint=(
    #                     self.model.get_var(f"service_{self.name}_E_in_t{interval.index}")
    #                     == self.model.sum_vars(
    #                         vars=[
    #                             self.model.get_var(f"asset_{asset.name}_service_{self.name}_E_in_t{interval.index}_var")
    #                             for asset in assets
    #                         ]
    #                     )
    #                 ),
    #             )
            
    #     return
    
    
    
    @abstractmethod
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        # the assetgroups will call this method on each service
        # in case the service needs to add any constraints/ costs to the asset group vars
        raise NotImplementedError
        