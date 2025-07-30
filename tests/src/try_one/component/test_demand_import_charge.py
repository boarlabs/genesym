
from datetime import datetime, timedelta
import pytz
import pytest

from optclient.solver_utils.ortools.solver import Solver
from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.isolver import OptSense

from src.try_one.demand_import_charge import DemandImportCharge
from src.try_one.parameters.intervals import Interval
from src.try_one.parameters.tariff_charges import DemandChargeParameters



def test_demand_import_only():
    model = Solver(client=Client(target="localhost:50051"))
    intervals = [
        Interval(index=0, interval_end=datetime(2024,1,1,4,0, tzinfo=pytz.utc))
    ]
    demand_import_charge_params = DemandChargeParameters.create_demand_charges(
        intervals, 4.2, (intervals[0].interval_end - timedelta(hours=1)).time(), intervals[0].interval_end.time()
    )

    assert demand_import_charge_params.P_in_max == [None]
    assert demand_import_charge_params.P_in_min == [0]
    assert demand_import_charge_params.P_out_max == [0]
    assert demand_import_charge_params.P_out_min == [0]

    demand_import_charge_params.P_in_max = [20]
    demand_import_charge_params.P_in_min  = [2]
    demand_import_charge_params.P_out_max = [10]
    demand_import_charge_params.P_out_min = [0]

    energy_import_model = DemandImportCharge(
        model, demand_import_charge_params
    )

    ortool_model = model._request.model

    vars = ortool_model.variable

    var_pout = vars[0]
    assert var_pout.upper_bound == 10
    assert var_pout.lower_bound == 0
    # assert var_pout.objective_coefficient == -1.2
    var_pin = vars[1]
    assert var_pin.upper_bound == 20
    assert var_pin.lower_bound == 2
    var_pmax = vars[2]
    assert var_pmax.objective_coefficient == 4.2

    var_pout.objective_coefficient = 0.000001
    model.solve_model(OptSense.minimize, {})

    ort_response = model._model_response
    assert ort_response.variable_value == [0,2,2]
    assert ort_response.objective_value == pytest.approx(2*4.2)


if __name__ == "__main__":
    test_demand_import_only()