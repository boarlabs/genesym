from __future__ import annotations
from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.constraint import ConstrSense
from optclient.solver_utils.expression import LinExpr

from service import Service
from parameters.tariff_charges import EnergyExportChargeParameters

class EnergyExportCharge(Service):
    def __init__(
        self,
        model: ISolver,
        service_params: EnergyExportChargeParameters,
    ):
        super().__init__(
            model=model,
            service_params=service_params,
        )
        self.add_objective_terms()
        
    
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        for interval in self.service_params.intervals:
            self.model.add_lin_constraint(
                name=f"energy_export_charge_{self.name}_P_out_t{interval.index}_asset_group_bind",
                variables=[
                    self.model.get_variable(f"service_{self.name}_P_out_t{interval.index}"),
                    self.model.get_variable(f"asset_group_{asset_group.name}_P_out_t{interval.index}")
                ],
                coefficients=[1, -1],
                rhs=0,
                sense=ConstrSense.eq,
            )

    def add_objective_terms(self) -> None:
        for interval in self.service_params.intervals:
            self.model.add_objective(
                term=LinExpr(
                    variables=[self.model.get_variable(f"service_{self.name}_P_out_t{interval.index}")],
                    coefs=[-1 * self.service_params.export_charge_rate * interval.length_in_hours],
                ),
                name=f"service_{self.name}_P_out_t_{interval.index}_export_revenue"
            )
            