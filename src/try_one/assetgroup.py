from typing import List
from model import Model, VarType
from asset import Asset
from parameters.asset_group import AssetGroupParameters
from service import Service

class AssetGroup:
    def __init__(
        self,
        model: Model,
        assets: List[Asset],
        services: List[Service],
        asset_group_params: AssetGroupParameters,
    ):
        self.name = asset_group_params.name
        self.model = model
        self.assets = assets
        self.services = services
        self.asset_group_params = asset_group_params

        for interval in asset_group_params.intervals:
            # if asset_group_params.P_out_max[interval.index] != 0:
            model.add_var(
                name=f"asset_group_{self.name}_P_out_t{interval.index}",
                var_type=VarType.REAL,
                lb=asset_group_params.P_out_min[interval.index],
                ub=asset_group_params.P_out_max[interval.index],
            )
                # model.add_var(
                #     name=f"asset_group_{self.name}_E_out_t{interval.index}",
                #     var_type=VarType.REAL,
                #     lb=asset_group_params.P_out_min,
                #     ub=asset_group_params.P_out_max,
                # )
                
            # if asset_group_params.P_in_max[interval.index] != 0:
            model.add_var(
                name=f"asset_group_{self.name}_P_in_t{interval.index}",
                var_type=VarType.REAL,
                lb=asset_group_params.P_in_min[interval.index],
                ub=asset_group_params.P_in_max[interval.index],
            )
                # model.add_var(
                #     name=f"asset_group_{self.name}_E_in_t{interval.index}",
                #     var_type=VarType.REAL,
                #     lb=asset_group_params.P_in_min,
                #     ub=asset_group_params.P_in_max,
                # )
                
            model.add_var(
                name=f"asset_group_{self.name}_commit_out_t{interval.index}",
                var_type=VarType.BOOLEAN,
                lb=0,
                ub=1,
            )
        
        self.add_asset_group_asset_binding()
        self.add_asset_group_power_complementarity()
      

        for service in services:
            service.add_asset_group_coupling(self)
            # service.add_assets(assets)
        
      
    
    
    def add_asset_group_asset_binding(self):
        for interval in self.asset_group_params.intervals:
            # if self.model.get_var(f"asset_group_{self.name}_P_out_t{interval.index}") is not None:
            self.model.add_constraint(
                name=f"asset_group_{self.name}_P_net_t{interval.index}_asset_bind",
                constraint=(
                    self.model.get_var(f"asset_group_{self.name}_P_out_t{interval.index}")
                    - self.model.get_var(f"asset_group_{self.name}_P_in_t{interval.index}")
                    ==  self.model.sum_vars(
                        variables=[
                            self.model.get_var(f"asset_{asset.name}_P_out_t{interval.index}")
                            for asset in self.assets
                        ]
                    )
                    - self.model.sum_vars(
                        variables=[
                            self.model.get_var(f"asset_{asset.name}_P_in_t{interval.index}")
                            for asset in self.assets
                        ]
                    )
                ),
            )
            
      
    
    
    def add_asset_group_power_complementarity(self):
        for interval in self.asset_group_params.intervals:
            self.model.add_constraint(
                name=f"asset_group_{self.name}_P_out_complementarity_t{interval.index}",
                constraint=(
                    self.model.get_var(f"asset_group_{self.name}_P_out_t{interval.index}")
                    <= self.model.get_var(f"asset_group_{self.name}_commit_out_t{interval.index}") * self.asset_group_params.P_out_max[interval.index]
                ),
            )
           
            
            
            self.model.add_constraint(
                name=f"asset_group_{self.name}_P_in_complementarity_t{interval.index}",
                constraint=(
                    self.model.get_var(f"asset_group_{self.name}_P_in_t{interval.index}")
                    <= (1 - self.model.get_var(f"asset_group_{self.name}_commit_out_t{interval.index}")) * self.asset_group_params.P_in_max[interval.index]
                ),
            )
         
        return
            
        


        
    
    
   