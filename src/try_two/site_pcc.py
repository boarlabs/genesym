from typing import List

from optclient.solver_utils.isolver import ISolver

from src.try_two.assetgroup import AssetGroup
from src.try_two.asset import Asset
from src.try_two.service import Service
from src.try_two.parameters.site import SiteParameters



class SitePCC(AssetGroup):
    
    def __init__(
        self,
        model: ISolver,
        assets: List[Asset],
        services: List[Service],
        asset_group_params: SiteParameters,
    ):
        super().__init__(
            model=model,
            assets=assets,
            services=services,
            asset_group_params=asset_group_params,
        )
    
    # After Solve method
    def get_site_ac_power_vars(self) -> List[float]:
        P_out_vars = [
            self.model.get_variable(f"asset_group_{self.name}_P_out_t{interval.index}")
            for interval in self.asset_group_params.intervals
        ]
        
        P_in_vars = [
            self.model.get_variable(f"asset_group_{self.name}_P_in_t{interval.index}")
            for interval in self.asset_group_params.intervals
        ]
        
        
        return[
            self.model.get_variable_value(P_out_var) - self.model.get_variable_value(P_in_var)
            for P_out_var, P_in_var in zip(P_out_vars, P_in_vars)
        ]
    
