from __future__ import annotations
from asset import Asset
from model import Model
from parameters.load import LoadParameters






class Load(Asset):
    
    def __init__(
        self,
        model: Model,
        asset_params: LoadParameters,
    ):
        super().__init__(
            model=model,
            asset_params=asset_params,
        )
        self.add_load_power_balance_constraints()
        # self.add_load_energy_power_bind_constraints()
        
        return
        
    
    
    
    
    def add_load_power_balance_constraints(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_constraint(
                name=f"load_{self.name}_P_in_t{interval.index}_power_balance",
                constraint=(
                    self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}")
                    ==  self.asset_params.load[interval.index]
                ),
            )

            self.model.add_constraint(
                name=f"load_{self.name}_P_out_t{interval.index}_power_balance",
                constraint=(
                    self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}")
                    ==  0
                ),
            )
    
    
    # def add_load_energy_power_bind_constraints(self) -> None:
    #     for interval in self.asset_params.intervals:
    #         self.model.add_constraint(
    #             name=f"load_{self.name}_E_in_t{interval.index}_power_bind",
    #             constraint=(
    #                 self.model.get_var(f"asset_{self.name}_E_in_t{interval.index}")
    #                 == self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}")
    #             ),
    #         )