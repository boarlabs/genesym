from typing import List

from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.variable import VarType, Variable
from optclient.solver_utils.constraint import ConstrSense

from src.try_one.asset import Asset

from src.try_one.parameters.battery import BatteryParameters



class Battery(Asset):
    def __init__(
        self,
        model: ISolver,
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
        
         
    def add_battery_soc_vars(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_variable(
                Variable(
                    name=f"battery_{self.name}_soc_t{interval.index}",
                    vtype=VarType.real,
                    lower_bound=self.asset_params.min_soc,
                    upper_bound=self.asset_params.energy_capacity,
                )
            )
        
    
    def add_battery_power_complementarity_vars(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_variable(
                Variable(
                    name=f"battery_{self.name}_commit_out_t{interval.index}",
                    vtype=VarType.boolean,
                    lower_bound=0,
                    upper_bound=1,
                )
            )
    
    
    def set_battery_soc_dynamic_constraints(self) -> None:
        
        for interval in self.asset_params.intervals:
            if interval.index == 0:
                self.model.add_lin_constraint(
                    name=f"battery_{self.name}_soc_t{interval.index}_dynamic",
                    variables=[
                        self.model.get_variable(f"battery_{self.name}_soc_t{interval.index}"),
                        self.model.get_variable(f"asset_{self.name}_P_in_t{interval.index}"),
                        self.model.get_variable(f"asset_{self.name}_P_out_t{interval.index}")
                    ],
                    coefficients=[1, - self.asset_params.charge_efficiency, (1 / self.asset_params.discharge_efficiency)],
                    rhs=self.asset_params.initial_energy,
                    sense=ConstrSense.eq,
                )            
            else:             
                self.model.add_lin_constraint(
                    name=f"battery_{self.name}_soc_t{interval.index}_dynamic",
                    variables=[
                        self.model.get_variable(f"battery_{self.name}_soc_t{interval.index}"),
                        self.model.get_variable(f"battery_{self.name}_soc_t{interval.index - 1}"),
                        self.model.get_variable(f"asset_{self.name}_P_in_t{interval.index}"),
                        self.model.get_variable(f"asset_{self.name}_P_out_t{interval.index}")
                    ],
                    coefficients=[1, -1, - self.asset_params.charge_efficiency, (1 / self.asset_params.discharge_efficiency)],
                    rhs=0,
                    sense=ConstrSense.eq,
                )
    
    def set_battery_power_complementarity(self) -> None:
        for interval in self.asset_params.intervals:
            self.model.add_lin_constraint(
                name=f"battery_{self.name}_P_out_complementarity_t{interval.index}",
                variables=[
                    self.model.get_variable(f"asset_{self.name}_P_out_t{interval.index}"),
                    self.model.get_variable(f"battery_{self.name}_commit_out_t{interval.index}")
                ],
                coefficients=[1, -self.asset_params.P_out_max[interval.index]],
                rhs=0,
                sense=ConstrSense.leq,
            )
           
            self.model.add_lin_constraint(
                name=f"battery_{self.name}_P_in_complementarity_t{interval.index}",
                variables=[
                    self.model.get_variable(f"asset_{self.name}_P_in_t{interval.index}"),
                    self.model.get_variable(f"battery_{self.name}_commit_out_t{interval.index}")
                ],
                coefficients=[1, self.asset_params.P_in_max[interval.index]],
                rhs=self.asset_params.P_in_max[interval.index],
                sense=ConstrSense.leq,
            )


    # After Solve method
    def get_battery_ac_power_vars(self) -> List[float]:
        P_out_vars = [
            self.model.get_variable(f"asset_{self.name}_P_out_t{interval.index}")
            for interval in self.asset_params.intervals
        ]
        
        P_in_vars = [
            self.model.get_variable(f"asset_{self.name}_P_in_t{interval.index}")
            for interval in self.asset_params.intervals
        ]
        
        
        return[
            self.model.get_variable_value(P_out_var) - self.model.get_variable_value(P_in_var)
            for P_out_var, P_in_var in zip(P_out_vars, P_in_vars)
        ]
        
    