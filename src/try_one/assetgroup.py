from typing import List

from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.variable import Variable, VarType
from optclient.solver_utils.constraint import ConstrSense

from src.try_one.asset import Asset
from src.try_one.parameters.asset_group import AssetGroupParameters
from src.try_one.service import Service

class AssetGroup:
    def __init__(
        self,
        model: ISolver,
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
            model.add_variable(
                Variable(
                    name=f"asset_group_{self.name}_P_out_t{interval.index}",
                    vtype=VarType.real,
                    lower_bound=asset_group_params.P_out_min[interval.index],
                    upper_bound=asset_group_params.P_out_max[interval.index],
                )
            )
              
            model.add_variable(
                Variable(
                    name=f"asset_group_{self.name}_P_in_t{interval.index}",
                    vtype=VarType.real,
                    lower_bound=asset_group_params.P_in_min[interval.index],
                    upper_bound=asset_group_params.P_in_max[interval.index],
                )
            )
                        
            model.add_variable(
                Variable(
                    name=f"asset_group_{self.name}_commit_out_t{interval.index}",
                    vtype=VarType.boolean,
                    lower_bound=0,
                    upper_bound=1,
                )
            )
        
        self.add_asset_group_asset_binding()
        self.add_asset_group_power_complementarity()
      

        for service in services:
            service.add_asset_group_coupling(self)
            # service.add_assets(assets)
        
      
    
    
    def add_asset_group_asset_binding(self):
        for interval in self.asset_group_params.intervals:
            self.model.add_lin_constraint(
                variables=[
                    self.model.get_variable(f"asset_group_{self.name}_P_out_t{interval.index}"),
                    self.model.get_variable(f"asset_group_{self.name}_P_in_t{interval.index}"),
                ] + [
                    self.model.get_variable(f"asset_{asset.name}_P_out_t{interval.index}")
                    for asset in self.assets
                ] + [
                    self.model.get_variable(f"asset_{asset.name}_P_in_t{interval.index}")
                    for asset in self.assets
                ],
                coefficients=[1.0,-1.0] + [-1] * len(self.assets) + [1] * len(self.assets),
                rhs=0,
                sense=ConstrSense.eq,
                name=f"asset_group_{self.name}_P_net_t{interval.index}_asset_bind",
            )
    
    
    def add_asset_group_power_complementarity(self):
        for interval in self.asset_group_params.intervals:
            self.model.add_lin_constraint(
                variables=[
                    self.model.get_variable(f"asset_group_{self.name}_P_out_t{interval.index}"),
                    self.model.get_var(f"asset_group_{self.name}_commit_out_t{interval.index}"),
                ],
                coefficients=[1, -1* self.asset_group_params.P_out_max[interval.index]],
                rhs=0,
                sense=ConstrSense.leq,
                name=f"asset_group_{self.name}_P_out_complementarity_t{interval.index}",
            )

            self.model.add_lin_constraint(
                variables=[
                    self.model.get_variable(f"asset_group_{self.name}_P_in_t{interval.index}"),
                    self.model.get_var(f"asset_group_{self.name}_commit_out_t{interval.index}"),
                ],
                coefficients=[1, self.asset_group_params.P_in_max[interval.index]],
                rhs=self.asset_group_params.P_in_max[interval.index],
                sense=ConstrSense.leq,
                name=f"asset_group_{self.name}_P_in_complementarity_t{interval.index}",
            )       
             