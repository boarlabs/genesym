from __future__ import annotations
from abc import abstractmethod
from model import Model, VarType   
from parameters.service import ServiceParameters

class Service:
    def __init__(
        self,
        model: Model,
        service_params: ServiceParameters,
    ):
        
        self.name = service_params.name
        self.service_params = service_params
        self.model = model
        
        for interval in service_params.intervals:
            model.add_var(
                name=f"service_{service_params.name}_P_out_t{interval.index}",
                var_type=VarType.REAL,
                lb=service_params.P_out_min[interval.index],
                ub=service_params.P_out_max[interval.index],
            )
              
            
            model.add_var(
                name=f"service_{service_params.name}_P_in_t{interval.index}",
                var_type=VarType.REAL,
                lb=service_params.P_in_min[interval.index],
                ub=service_params.P_in_max[interval.index],
            )
             
        return

    
    
    @abstractmethod
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        # the assetgroups will call this method on each service
        # in case the service needs to add any constraints/ costs to the asset group vars
        raise NotImplementedError
        