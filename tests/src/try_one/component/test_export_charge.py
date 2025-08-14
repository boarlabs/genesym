from datetime import datetime
import pytz
import pytest

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_two.energy_export_charge import EnergyExportCharge
from src.try_two.parameters.intervals import Interval
from src.try_two.parameters.tariff_charges import EnergyExportChargeParameters



def test_energy_export_only():
    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    energy_export_params = EnergyExportChargeParameters.create_energy_export_charges(
        intervals, 1.2
    )
    
    assert energy_export_params.P_in_max == [0]
    assert energy_export_params.P_in_min == [0]
    assert energy_export_params.P_out_max == [None]
    assert energy_export_params.P_out_min == [0]

    energy_export_params.P_in_max = [20]
    energy_export_params.P_in_min  = [0]
    energy_export_params.P_out_max = [10]
    energy_export_params.P_out_min = [0]

    energy_import_model = EnergyExportCharge(
        model, energy_export_params
    )

    ortool_model = model._request.model

    vars = ortool_model.variable

    var_pout = vars[0]
    assert var_pout.upper_bound == 10
    assert var_pout.lower_bound == 0
    assert var_pout.objective_coefficient == -1.2
    var_pin = vars[1]
    assert var_pin.upper_bound == 20
    assert var_pin.lower_bound == 0
    var_pin.objective_coefficient = 0.000001
    model.solve_model(OptSense.minimize, {})

    ort_response = model._model_response
    assert ort_response.variable_value == [10,0]
    assert ort_response.objective_value == pytest.approx(-12)
    ck=1


if __name__ == "__main__":
    test_energy_export_only()