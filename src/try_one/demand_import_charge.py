from datetime import timedelta, datetime, time
from service import Service
from model import Model, VarType
from parameters.tariff_charges import DemandChargeParameters



class DemandImportCharge(Service):
    
    def __init__(
        self,
        model: Model,
        service_params: DemandChargeParameters,
    ):
        super().__init__(
            model=model,
            service_params=service_params,
        )
        
        
        self.model.add_var(
            name=f"demand_import_charge_{service_params.name}_P_in_max",
            var_type=VarType.REAL,
            lb=0,
        )
        
        self.add_max_demand_constraint()
        self.add_objective_terms()
        
        return
    
    def add_max_demand_constraint(self) -> None:
        for interval in self.service_params.intervals:        
            interval_start = interval.interval_end - interval.interval_duration
            if (
                (interval_start.time() < self.service_params.demand_charge_period_end)
                and
                (interval_start.time() >= self.service_params.demand_charge_period_start)
               
            ):
                self.model.add_constraint(
                    name=f"demand_import_charge_{self.name}_P_in_t{interval.index}_max_demand",
                    constraint=(
                        self.model.get_var(f"service_{self.name}_P_in_t{interval.index}")
                        <= self.model.get_var(f"demand_import_charge_{self.name}_P_in_max")
                    ),
                )
        
    
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        for interval in self.service_params.intervals:
            self.model.add_constraint(
                name=f"demand_import_charge_{self.name}_P_in_t{interval.index}_asset_group_bind",
                constraint=(
                    self.model.get_var(f"service_{self.name}_P_in_t{interval.index}")
                    ==  self.model.get_var(f"asset_group_{asset_group.name}_P_in_t{interval.index}"
                    )
                ),
            )
        return
    
    def add_objective_terms(self) -> None:
        self.model.add_objective_terms(
            objective_terms= (
                self.model.get_var(f"demand_import_charge_{self.name}_P_in_max")
                * self.service_params.demand_charge_rate
            )
        )
           
        return



