
from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.constraint import ConstrSense

from src.try_one.parameters.solar import SolarParameters
from src.try_one.asset import Asset

class Solar(Asset):
    def __init__(
        self,
        model: ISolver,
        asset_params: SolarParameters,
    ):
        
        super().__init__(
            model=model,
            asset_params=asset_params,
        )
        
        self.add_solar_power_balance_constraints()
        
    
    
    def add_solar_power_balance_constraints(self) -> None:
        for interval in self.asset_params.intervals:            
            self.model.add_lin_constraint(
                name=f"solar_{self.name}_P_out_t{interval.index}_power_balance",
                variables=[self.model.get_variable(f"asset_{self.name}_P_out_t{interval.index}")],
                coefficients=[1],
                rhs=self.asset_params.solar[interval.index],
                sense=ConstrSense.eq,
            )
            self.model.add_lin_constraint(
                name=f"solar_{self.name}_P_in_t{interval.index}_power_balance",
                variables=[self.model.get_variable(f"asset_{self.name}_P_in_t{interval.index}")],
                coefficients=[1],
                rhs=0,
                sense=ConstrSense.eq,
            )
    
    