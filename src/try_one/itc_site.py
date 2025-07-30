from typing import List

from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.constraint import ConstrSense

from src.try_one.site_pcc import SitePCC
from src.try_one.parameters.site import SiteParameters
from src.try_one.asset import Asset
from src.try_one.battery import Battery
from src.try_one.solar import Solar
from src.try_one.service import Service

class ITCSite(SitePCC):
    
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
        self.add_itc_constraints()    
    
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
            self.model.add_lin_constraint(
                name=f"itc_{self.name}_battery_charge_t{interval.index}",
                variables=[
                    self.model.get_variable(f"asset_{battery_asset.name}_P_in_t{interval.index}"),
                    self.model.get_variable(f"asset_{solar_asset.name}_P_out_t{interval.index}")
                ],
                coefficients=[1, -1],
                rhs=0,
                sense=ConstrSense.leq,
            )
