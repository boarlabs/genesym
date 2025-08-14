from service import Service
from model import Model
from parameters.tariff_charges import DemandResponseChargeParameters


class DemandResponseCharge(Service):
    def __init__(
        self,
        model: Model,
        service_params: DemandResponseChargeParameters,
    ):
        super().__init__(
            model=model,
            service_params=service_params,
        )
        self.add_objective_terms()
        return
    
    
    def add_objective_terms(self) -> None:
        for interval in self.service_params.intervals:
            interval_start = interval.interval_end - interval.interval_duration
            if (
                (interval_start.time() < self.service_params.demand_response_period_end)
                and
                (interval_start.time() >= self.service_params.demand_response_period_start)
               
            ):
                self.model.add_objective_terms(
                    objective_terms= (
                        - self.model.get_var(f"service_{self.name}_P_out_t{interval.index}")
                        * self.service_params.demand_response_charge_rate * interval.length_in_hours
                    )
                )
        return
    
    
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        for interval in self.service_params.intervals:
            self.model.add_constraint(
                name=f"demand_response_charge_{self.name}_P_out_t{interval.index}_asset_group_bind",
                constraint=(
                    self.model.get_var(f"service_{self.name}_P_out_t{interval.index}")
                    ==  self.model.get_var(f"asset_group_{asset_group.name}_P_out_t{interval.index}"
                    )
                ),
            )
        return