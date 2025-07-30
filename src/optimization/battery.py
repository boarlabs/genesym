from typing import List
from asset import Asset
from model import Model, VarType
from parameters.battery import BatteryParameters



class Battery(Asset):
    def __init__(
        self,
        model: Model,
        asset_params: BatteryParameters,
    ):
        super().__init__(
            model=model,
            asset_params=asset_params,
        )
        
        self.add_battery_soc_vars()
        self.add_battery_power_complementarity_vars()
        self.set_battery_soc_dynamic_constraints()
        self.set_battery_power_complementarity()
        # self.add_battery_energy_power_bind_constraints()
        
                
        return
    
    
    def add_battery_soc_vars(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_var(
                name=f"battery_{self.name}_soc_t{interval.index}",
                var_type=VarType.REAL,
                lb=self.asset_params.min_soc,
                ub=self.asset_params.energy_capacity,
            )
        return
    
    def add_battery_power_complementarity_vars(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_var(
                name=f"battery_{self.name}_commit_out_t{interval.index}",
                var_type=VarType.BOOLEAN,
                lb=0,
                ub=1,
            )
    
    
    def set_battery_soc_dynamic_constraints(self) -> None:
        
        for interval in self.asset_params.intervals:
            if interval.index == 0:
                self.model.add_constraint(
                    name=f"battery_{self.name}_soc_t{interval.index}_dynamic",
                    constraint=(
                        self.model.get_var(f"battery_{self.name}_soc_t{interval.index}")
                        ==  self.asset_params.initial_energy
                        + (
                            (self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}") * self.asset_params.charge_efficiency)
                            - (self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}") * (1 / self.asset_params.discharge_efficiency))
                        ) 
                    ),
                )
            
            else:
                self.model.add_constraint(
                    name=f"battery_{self.name}_soc_t{interval.index}_dynamic",
                    constraint=(
                        self.model.get_var(f"battery_{self.name}_soc_t{interval.index}")
                        ==  self.model.get_var(f"battery_{self.name}_soc_t{interval.index - 1}")
                        + (
                            (self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}") * self.asset_params.charge_efficiency)
                        - (self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}") * (1 / self.asset_params.discharge_efficiency))
                        )
                    ),
                )
        return
    
    def set_battery_power_complementarity(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_constraint(
                name=f"battery_{self.name}_P_out_complementarity_t{interval.index}",
                constraint=(
                    self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}")
                    <=  self.model.get_var(f"battery_{self.name}_commit_out_t{interval.index}")
                    * self.asset_params.P_out_max[interval.index]
                ),
            )
            self.model.add_constraint(
                name=f"battery_{self.name}_P_in_complementarity_t{interval.index}",
                constraint=(
                    self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}")
                    <= (1- self.model.get_var(f"battery_{self.name}_commit_out_t{interval.index}"))
                    * self.asset_params.P_in_max[interval.index]
                ),
            )
        return


    # def add_battery_energy_power_bind_constraints(self) -> None:
        
    #     for interval in self.asset_params.intervals:
    #         self.model.add_constraint(
    #             name=f"battery_{self.name}_E_out_t{interval.index}_power_bind",
    #             constraint=(
    #                 self.model.get_var(f"asset_{self.name}_E_out_t{interval.index}")
    #                 == self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}") * interval.length_in_hours
    #             ),
    #         )
    #         self.model.add_constraint(
    #             name=f"battery_{self.name}_E_in_t{interval.index}_power_bind",
    #             constraint=(
    #                 self.model.get_var(f"asset_{self.name}_E_in_t{interval.index}")
    #                 == self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}") * interval.length_in_hours
    #             ),
    #         )
        
        # return     
        
    # After Solve method
    def get_battery_ac_power_vars(self) -> List[float]:
        P_out_vars = [
            self.model.get_var(f"asset_{self.name}_P_out_t{interval.index}")
            for interval in self.asset_params.intervals
        ]
        
        P_in_vars = [
            self.model.get_var(f"asset_{self.name}_P_in_t{interval.index}")
            for interval in self.asset_params.intervals
        ]
        
        
        return[
            self.model.get_var_value(P_out_var) - self.model.get_var_value(P_in_var)
            for P_out_var, P_in_var in zip(P_out_vars, P_in_vars)
        ]
        
    