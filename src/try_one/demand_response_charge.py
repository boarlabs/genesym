from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.constraint import ConstrSense
from optclient.solver_utils.expression import LinExpr

from service import Service
from parameters.tariff_charges import DemandResponseChargeParameters


class DemandResponseCharge(Service):
    def __init__(
        self,
        model: ISolver,
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
                self.model.add_objective(
                    term=LinExpr(
                        variables=[self.model.get_var(f"service_{self.name}_P_out_t{interval.index}")],
                        coefs=[- self.service_params.demand_response_charge_rate * interval.length_in_hours],
                    ),
                    name=f"service_{self.name}_P_out_t_{interval.index}_export_revenue"
                )
    
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        for interval in self.service_params.intervals:
            self.model.add_lin_constraint(
                name=f"demand_response_charge_{self.name}_P_out_t{interval.index}_asset_group_bind",
                variables=[
                    self.model.get_variable(f"service_{self.name}_P_out_t{interval.index}"),
                    self.model.get_variable(f"asset_group_{asset_group.name}_P_out_t{interval.index}")
                ],
                coefficients=[1, -1],
                rhs=0,
                sense=ConstrSense.eq,
            )
