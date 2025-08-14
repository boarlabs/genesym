from asset import Asset
from model import Model
from parameters.solar import SolarParameters

class Solar(Asset):
    def __init__(
        self,
        model: Model,
        asset_params: SolarParameters,
    ):
        
        super().__init__(
            model=model,
            asset_params=asset_params,
        )
        
        self.add_solar_power_balance_constraints()
        # self.add_solar_energy_power_bind_constraints()
        
        
        return
    
    
    
    def add_solar_power_balance_constraints(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_constraint(
                name=f"solar_{self.name}_P_out_t{interval.index}_power_balance",
                constraint=(
                    self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}")
                    ==  self.asset_params.solar[interval.index]
                ),
            )
            self.model.add_constraint(
                name=f"solar_{self.name}_P_in_t{interval.index}_power_balance",
                constraint=(
                    self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}")
                    ==  0
                ),
            )

    
    
    # def add_solar_energy_power_bind_constraints(self) -> None:
    #     for interval in self.asset_params.intervals:
    #         self.model.add_constraint(
    #             name=f"solar_{self.name}_E_out_t{interval.index}_power_bind",
    #             constraint=(
    #                 self.model.get_var(f"asset_{self.name}_E_out_t{interval.index}")
    #                 ==  self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}")
    #             ),
    #         )