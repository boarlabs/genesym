from typing import List
from assetgroup import AssetGroup
from asset import Asset
from model import Model, VarType
from service import Service
from parameters.site import SiteParameters



class SitePCC(AssetGroup):
    
    def __init__(
        self,
        model: Model,
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
        
        # self.add_site_soc_vars()
        # self.set_site_soc_dynamic_constraints()
        
        return
    
    
    
    # After Solve method
    def get_site_ac_power_vars(self) -> List[float]:
        P_out_vars = [
            self.model.get_var(f"asset_group_{self.name}_P_out_t{interval.index}")
            for interval in self.asset_group_params.intervals
        ]
        
        P_in_vars = [
            self.model.get_var(f"asset_group_{self.name}_P_in_t{interval.index}")
            for interval in self.asset_group_params.intervals
        ]
        
        
        return[
            self.model.get_var_value(P_out_var) - self.model.get_var_value(P_in_var)
            for P_out_var, P_in_var in zip(P_out_vars, P_in_vars)
        ]
    
