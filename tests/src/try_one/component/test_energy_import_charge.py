from datetime import datetime
import pytz

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_one.energy_import_charge import EnergyImportCharge
from src.try_one.parameters.service import ServiceParameters
from src.try_one.parameters.intervals import Interval
from src.try_one.parameters.tariff_charges import EnergyImportChargeParameters

def test_energy_import_charge_only():

    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    energy_import_params = EnergyImportChargeParameters.create_energy_import_charges(
        intervals, 1.5
    )
    
    assert energy_import_params.P_in_max == [None]
    assert energy_import_params.P_in_min == [0]
    assert energy_import_params.P_out_max == [0]
    assert energy_import_params.P_out_min == [0]

    energy_import_params.P_in_max = [20]
    energy_import_params.P_in_min  = [0]
    energy_import_params.P_out_max = [10]
    energy_import_params.P_out_min = [0]

    energy_import_model = EnergyImportCharge(
        model, energy_import_params
    )

    ortool_model = model._request.model

    vars = ortool_model.variable

    var_pout = vars[0]
    assert var_pout.upper_bound == 10
    assert var_pout.lower_bound == 0
    var_pin = vars[1]
    assert var_pin.upper_bound == 20
    assert var_pin.lower_bound == 0
    assert var_pin.objective_coefficient == 1.5
    ck=2


    
if __name__ == "__main__":
    test_energy_import_charge_only()