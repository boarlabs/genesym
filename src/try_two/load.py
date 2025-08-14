from __future__ import annotations

from  optclient.solver_utils.isolver import ISolver
from  optclient.solver_utils.constraint import ConstrSense

from src.try_two.asset import Asset
from src.try_two.parameters.load import LoadParameters



class Load(Asset):
    
    def __init__(
        self,
        model: ISolver,
        asset_params: LoadParameters,
    ):
        super().__init__(
            model=model,
            asset_params=asset_params,
        )
        self.add_load_power_balance_constraints()
       
    
    
    
    def add_load_power_balance_constraints(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_lin_constraint(
                name=f"load_{self.name}_P_in_t{interval.index}_power_balance",
                variables=[self.model.get_variable(f"asset_{self.name}_P_in_t{interval.index}")],
                coefficients=[1],
                rhs=self.asset_params.load[interval.index],
                sense=ConstrSense.eq,                
            )
            self.model.add_lin_constraint(
                name=f"load_{self.name}_P_out_t{interval.index}_power_balance",
                variables=[self.model.get_variable(f"asset_{self.name}_P_out_t{interval.index}")],
                coefficients=[1],
                rhs=0,
                sense=ConstrSense.eq,                
            )    
    
    