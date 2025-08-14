from typing import List
from site_pcc import SitePCC
from parameters.site import SiteParameters
from model import Model
from asset import Asset
from battery import Battery
from solar import Solar
from service import Service

class ITCSite(SitePCC):
    
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
        
        self.add_itc_constraints()
                
        return
    
    
    def add_itc_constraints(self) -> None:
        battery_asset = next(
            asset for asset in self.assets 
                if isinstance(asset, Battery)
        )
        solar_asset = next(
            asset for asset in self.assets 
                if isinstance(asset, Solar)
        )
        
        for interval in self.asset_group_params.intervals:
            self.model.add_constraint(
                name=f"itc_{self.name}_battery_charge_t{interval.index}",
                constraint=(
                    self.model.get_var(f"asset_{battery_asset.name}_P_in_t{interval.index}")
                    <= self.model.get_var(f"asset_{solar_asset.name}_P_out_t{interval.index}")
                ),
            )
        return