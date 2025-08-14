from datetime import timedelta, datetime, time

from optclient.solver_utils.isolver import ISolver
from optclient.solver_utils.variable import  Variable, VarType
from optclient.solver_utils.expression import LinExpr
from optclient.solver_utils.constraint import ConstrSense


from src.try_two.service import Service
from src.try_two.parameters.tariff_charges import DemandChargeParameters



class DemandImportCharge(Service):
    
    def __init__(
        self,
        model: ISolver,
        service_params: DemandChargeParameters,
    ):
        super().__init__(
            model=model,
            service_params=service_params,
        )
        self.model.add_variable(
            Variable(
                name=f"demand_import_charge_{service_params.name}_P_in_max",
                vtype=VarType.real,
                lower_bound=0,
            )
        )
        self.add_max_demand_constraint()
        self.add_objective_terms()

            
    def add_max_demand_constraint(self) -> None:
        for interval in self.service_params.intervals:        
            interval_start = interval.interval_end - interval.interval_duration
            if (
                (interval_start.time() < self.service_params.demand_charge_period_end)
                and
                (interval_start.time() >= self.service_params.demand_charge_period_start)
               
            ):
                self.model.add_lin_constraint(
                    name=f"demand_import_charge_{self.name}_P_in_t{interval.index}_max_demand",
                    variables=[
                        self.model.get_variable(f"service_{self.name}_P_in_t{interval.index}"),
                        self.model.get_variable(f"demand_import_charge_{self.name}_P_in_max")
                    ],
                    coefficients=[1, -1],
                    rhs=0,
                    sense=ConstrSense.leq
                )
    
    def add_asset_group_coupling(self, asset_group: "assetgroup.AssetGroup") -> None:
        for interval in self.service_params.intervals:
            self.model.add_lin_constraint(
                name=f"demand_import_charge_{self.name}_P_in_t{interval.index}_asset_group_bind",
                variables=[
                    self.model.get_variable(f"service_{self.name}_P_in_t{interval.index}"),
                    self.model.get_variable(f"asset_group_{asset_group.name}_P_in_t{interval.index}")
                ],
                coefficients=[1, -1],
                rhs=0,
                sense=ConstrSense.eq,
            )
    
    def add_objective_terms(self) -> None:
        self.model.add_objective(
            term=LinExpr(
                variables=[self.model.get_variable(f"demand_import_charge_{self.name}_P_in_max")],
                coefs=[self.service_params.demand_charge_rate],
            ),
            name=f"service_{self.name}_P_in_demand_charge",
        )


