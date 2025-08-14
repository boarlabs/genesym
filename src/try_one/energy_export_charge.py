from __future__ import annotations
from service import Service
from model import Model
from parameters.tariff_charges import EnergyExportChargeParameters

class EnergyExportCharge(Service):
    def __init__(
        self,
        model: Model,
        service_params: EnergyExportChargeParameters,
    ):
        super().__init__(
            model=model,
            service_params=service_params,
        )
        self.add_objective_terms()
    
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        for interval in self.service_params.intervals:
            self.model.add_constraint(
                name=f"energy_export_charge_{self.name}_P_out_t{interval.index}_asset_group_bind",
                constraint=(
                    self.model.get_var(f"service_{self.name}_P_out_t{interval.index}")
                    ==  self.model.get_var(f"asset_group_{asset_group.name}_P_out_t{interval.index}"
                    )
                ),
            )
        return
         

      
    def add_objective_terms(self) -> None:
        for interval in self.service_params.intervals:
            # if self.model.get_var(f"service_{self.name}_P_out_t{interval.index}") is not None:
            self.model.add_objective_terms(
                objective_terms= (
                    - self.model.get_var(f"service_{self.name}_P_out_t{interval.index}")
                    * self.service_params.export_charge_rate * interval.length_in_hours
                )
            )
        return